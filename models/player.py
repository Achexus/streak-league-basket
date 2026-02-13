import random
from datetime import date, timedelta
from models.stats import StatsManager
from models.tasks import TaskManager
from systems.event_system import EventManager

class Player:
    def __init__(self, name, number, position):
        self.name = name
        self.number = number
        self.position = position
        
        self.team_obj = None 
        self.league_id = None # Hangi ligde oynadığını bilmeli
        
        # Oyun 15 Eylül'de başlasın
        self.current_date = date(date.today().year, 9, 15)
        self.days_passed = 0
        
        # Alt Sistemler
        self.stats = StatsManager(position)
        self.tasks = TaskManager()
        self.events = EventManager() # Event sistemi
        
        # Kariyer İstatistikleri
        self.games_played = 0
        self.career_pts = 0
        self.career_ast = 0
        self.career_reb = 0
        self.career_stl = 0
        self.career_blk = 0
        
        # Gelişim
        self.level = 1
        self.xp_pool = 0 
        self.total_lifetime_xp = 0

    def apply_daily_score(self, score):
        """Günü bitirince XP ve Event durumunu günceller"""
        messages = []
        
        # XP Kazanımı
        if score > 0:
            self.xp_pool += score
            self.total_lifetime_xp += score
            new_level = 1 + (self.total_lifetime_xp // 1000)
            
            if new_level > self.level:
                messages.append(f"🎉 LEVEL UP! {self.level} -> {new_level}")
                for key in self.stats.attributes:
                    self.stats.upgrade_stat(key, 1)
                self.level = new_level
        
        # Event Kontrolü
        event_msg = self.events.daily_reset(score)
        if event_msg:
            messages.append(event_msg)
            
        self.events.check_for_new_event()
        
        # Tarihi İlerlet
        self.current_date += timedelta(days=1)
        self.days_passed += 1
        
        return messages

    def get_match_bonus(self):
        bonus = 0
        if self.events.perfect_streak > 0:
            bonus += self.events.perfect_streak * 2
        return bonus

    def update_match_stats(self, pts, ast, reb, stl, blk):
        self.games_played += 1
        self.career_pts += pts
        self.career_ast += ast
        self.career_reb += reb
        self.career_stl += stl
        self.career_blk += blk

    def get_date_str(self):
        return self.current_date.strftime("%d %B %Y")
    
    def check_agenda_alerts(self):
        # O günkü takvim notlarını bul
        return [i.content for i in self.tasks.agenda if i.event_date.date() == self.current_date]
    
    def import_agenda_to_task(self):
        alerts = self.check_agenda_alerts()
        count = 0
        for note in alerts:
            # Aynı notu tekrar ekleme
            if not any(t.task == f"[AGENDA] {note}" for t in self.tasks.daily_tasks):
                self.tasks.add_task(f"[AGENDA] {note}", 'M')
                count += 1
        return count