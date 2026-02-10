import random
from datetime import date
from stats import StatsManager
from tasks import TaskManager

class Player:
    def __init__(self, name, number, position):
        self.name = name
        self.number = number
        self.position = position
        
        # Takım Bilgisi (Ligden atanacak)
        self.team_obj = None 
        self.city = ""
        
        # Modüller
        self.stats = StatsManager() # Hayaller & Gelişimler
        self.tasks = TaskManager()  # Görevler & Rutinler
        
        # Kariyer İstatistikleri
        self.games_played = 0
        self.career_pts = 0
        self.career_ast = 0
        self.career_reb = 0
        
        # Seviye Sistemi
        self.level = 1
        self.xp_pool = 0 
        self.total_lifetime_xp = 0 # Toplam kazanılan XP

    def assign_team(self, league_obj):
        self.team_obj = random.choice(league_obj.teams)
        self.city = league_obj.city_name

    def apply_daily_score(self, score):
        """Gün sonu skorunu işler."""
        if score > 0:
            self.xp_pool += score
            self.total_lifetime_xp += score
            # Her 500 XP = 1 Level
            self.level = 1 + (self.total_lifetime_xp // 500)

    def update_match_stats(self, pts, ast, reb):
        self.games_played += 1
        self.career_pts += pts
        self.career_ast += ast
        self.career_reb += reb

    def get_averages(self):
        if self.games_played == 0: return "0.0 PPG | 0.0 APG | 0.0 RPG"
        p = round(self.career_pts / self.games_played, 1)
        a = round(self.career_ast / self.games_played, 1)
        r = round(self.career_reb / self.games_played, 1)
        return f"{p} PPG | {a} APG | {r} RPG"

    # --- EKSİK OLAN TARİH VE AJANDA FONKSİYONLARI ---
    
    def get_today_str(self):
        """Bugünün tarihini string olarak döndürür (Örn: 10 Feb 2026)"""
        return date.today().strftime("%d %B %Y")

    def check_agenda_alerts(self):
        """Bugüne ait ajanda notlarını TaskManager'dan çeker"""
        return self.tasks.check_agenda()

    def import_agenda_to_task(self):
        """Ajandadaki bugünün işlerini Günlük Görevlere ekler"""
        alerts = self.check_agenda_alerts()
        count = 0
        for note in alerts:
            # Aynı isimde görev yoksa ekle
            if not any(t.task == f"[AGENDA] {note}" for t in self.tasks.daily_tasks):
                self.tasks.add_task(f"[AGENDA] {note}", 'M') # Varsayılan: Medium Zorluk
                count += 1
        return count