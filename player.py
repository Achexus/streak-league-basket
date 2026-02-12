import random
from datetime import date
from stats import StatsManager
from tasks import TaskManager
from events import EventManager
from config import MONTHLY_EVENTS

class Player:
    def __init__(self, name, number, position):
        self.name = name
        self.number = number
        self.position = position
        
        self.team_obj = None 
        self.city = ""
        
        # --- MODÜLLER ---
        self.stats = StatsManager(position) # Statlar (SHT, FIN, MEN...)
        self.tasks = TaskManager()          # Günlük Görevler
        self.events = EventManager()        # YENİ: Etkinlik Yöneticisi
        
        # --- KARİYER İSTATİSTİKLERİ ---
        self.games_played = 0
        self.career_pts = 0
        self.career_ast = 0
        self.career_reb = 0
        self.career_stl = 0
        self.career_blk = 0
        
        # --- LEVEL & XP ---
        self.level = 1
        self.xp_pool = 0 
        self.total_lifetime_xp = 0
        self.days_passed = 0

    def assign_team(self, league_obj):
        self.team_obj = random.choice(league_obj.teams)
        self.city = league_obj.city_name

    def apply_daily_score(self, score):
        """
        Gün sonu (End Day) tetiklendiğinde çalışır.
        Hem Level XP'sini işler hem de Etkinlik ilerlemesini kontrol eder.
        """
        messages = []
        
        # 1. Level ve XP İşlemleri
        if score > 0:
            self.xp_pool += score
            self.total_lifetime_xp += score
            
            # Level Formülü: Her 1000 XP = 1 Level
            new_level = 1 + (self.total_lifetime_xp // 1000)
            
            if new_level > self.level:
                messages.append(f"🎉 LEVEL UP! {self.level} -> {new_level}")
                messages.append("   All stats increased by +1")
                for key in self.stats.attributes:
                    self.stats.upgrade_stat(key, 1)
                self.level = new_level
        
        # 2. Etkinlik Güncellemesi (Streak ve Event Sonu Kontrolü)
        event_msg = self.events.daily_reset(score)
        if event_msg:
            messages.append(event_msg)
            
        # 3. Yeni Etkinlik Kontrolü (Tarihe göre)
        self.events.check_for_new_event()
        
        self.days_passed += 1
        return messages

    def get_match_bonus(self):
        """
        Maç içinde kullanılacak bonusları hesaplar.
        Eğer kusursuz seri (Perfect Streak) varsa stat bonusu verir.
        """
        bonus = 0
        
        # Kusursuz Gün Serisi Bonusu (Etkinlikten gelir)
        if self.events.perfect_streak > 0:
            # Her kusursuz gün için +2 Genel Güç
            bonus += self.events.perfect_streak * 2
            
        # Aktif Event Kartlarının Etkisi (Opsiyonel: İleride koleksiyondan seçilebilir)
        # Şimdilik sadece streak bonusu aktif.
        return bonus

    def update_match_stats(self, pts, ast, reb, stl, blk):
        self.games_played += 1
        self.career_pts += pts
        self.career_ast += ast
        self.career_reb += reb
        self.career_stl += stl
        self.career_blk += blk

    def get_averages(self):
        if self.games_played == 0: return "0.0 PPG | 0.0 APG | 0.0 RPG"
        p = round(self.career_pts / self.games_played, 1)
        a = round(self.career_ast / self.games_played, 1)
        r = round(self.career_reb / self.games_played, 1)
        return f"{p} PPG | {a} APG | {r} RPG"

    def get_today_str(self):
        return date.today().strftime("%d %B %Y")
    
    def check_agenda_alerts(self):
        return self.tasks.check_agenda()
    
    def import_agenda_to_task(self):
        alerts = self.check_agenda_alerts()
        count = 0
        for note in alerts:
            if not any(t.task == f"[AGENDA] {note}" for t in self.tasks.daily_tasks):
                self.tasks.add_task(f"[AGENDA] {note}", 'M')
                count += 1
        return count