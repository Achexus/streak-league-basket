import random
from datetime import date
from config import SEASON_SCHEDULE, XP_VALUES, STAT_NAMES, EVENT_TYPE_BOSS, EVENT_TYPE_CLIMB, EVENT_TYPE_BOARD, EVENT_TYPE_BINGO, EVENT_TYPE_COLLECT, EVENT_TYPE_STORY, EVENT_TYPE_SURVIVAL, EVENT_TYPE_TOURNEY, EVENT_TYPE_CRAFT, EVENT_TYPE_TIME, EVENT_TYPE_PUZZLE, EVENT_TYPE_TRAIN

class EventCard:
    """Etkinlik Sonunda Kazanılan Özel Kart"""
    def __init__(self, name, event_type, player_ovr, is_perfect_run):
        self.name = name
        self.type = event_type
        self.date_earned = date.today().strftime("%d %B %Y")
        self.is_perfect = is_perfect_run # Kusursuz tamamlandı mı?
        
        # Kartın Gücü Oyuncunun OVR'sine göre scale olur
        base_boost = int(player_ovr * 0.1) # %10 Boost
        if is_perfect_run:
            base_boost += 2 # Kusursuzsa ekstra bonus
            self.rarity = "LEGENDARY"
        else:
            self.rarity = "RARE"
            
        self.stats = {
            "OFF": base_boost + random.randint(0, 2),
            "DEF": base_boost + random.randint(0, 2),
            "MEN": base_boost + 5 # Event kartları mental güç verir
        }

class ActiveEvent:
    """Şu an aktif olan etkinliğin durumunu yönetir"""
    def __init__(self, event_data, current_day):
        self.data = event_data
        self.name = event_data['name']
        self.type = event_data['type']
        self.emoji = event_data['emoji']
        self.desc = event_data['desc']
        
        # Etkinlik İlerleme Durumu (Moda göre değişir)
        self.progress = 0
        self.goal = 100 # Varsayılan hedef
        self.boss_hp = 1000
        self.current_floor = 1
        self.bingo_grid = [False] * 9 # 3x3 Bingo
        
        # Kilit Durumu
        # Eğer oyun ayın ortasında başladıysa ve event başlamışsa kilitli gelir
        start_day = 1 if event_data['cycle'] == 1 else 16
        if current_day > start_day + 2: # 2 gün tolerans
            self.is_locked = True
            self.lock_reason = "Event started before you joined. Wait for next cycle."
        else:
            self.is_locked = False
            self.lock_reason = ""
            
        self.tasks = []
        self.generate_daily_event_tasks()

    def generate_daily_event_tasks(self):
        """Etkinlik tipine göre özel görevler üretir"""
        self.tasks = []
        # Her gün 3 tane event görevi gelir
        base_tasks = [
            {"desc": "Complete 3 Daily Habits", "xp": 50, "dmg": 100},
            {"desc": "Win 1 League Match", "xp": 100, "dmg": 200},
            {"desc": "Don't skip any habit today", "xp": 150, "dmg": 300}
        ]
        
        # Moda göre görev metnini süsle
        for t in base_tasks:
            if self.type == EVENT_TYPE_BOSS:
                t['desc'] += f" (Deal {t['dmg']} DMG to Boss)"
            elif self.type == EVENT_TYPE_CLIMB:
                t['desc'] += " (Climb 1 Floor)"
            elif self.type == EVENT_TYPE_COLLECT:
                t['desc'] += " (Find 1 Token)"
            
            self.tasks.append({
                "task": t['desc'],
                "xp": t['xp'],
                "done": False,
                "val": t['dmg'] # Boss hasarı veya ilerleme puanı
            })

    def complete_task(self, index):
        if 0 <= index < len(self.tasks) and not self.tasks[index]['done']:
            task = self.tasks[index]
            task['done'] = True
            
            # İlerlemeyi işle
            if self.type == EVENT_TYPE_BOSS:
                self.boss_hp -= task['val']
                if self.boss_hp < 0: self.boss_hp = 0
            
            elif self.type == EVENT_TYPE_CLIMB:
                self.current_floor += 1
                
            elif self.type == EVENT_TYPE_BINGO:
                # Rastgele bir kutuyu aç
                empty_slots = [i for i, x in enumerate(self.bingo_grid) if not x]
                if empty_slots:
                    slot = random.choice(empty_slots)
                    self.bingo_grid[slot] = True
            
            else:
                self.progress += 10 # Standart ilerleme

            return task['xp']
        return 0

    def get_status_str(self):
        """Etkinlik durumunu görsel string olarak döner"""
        if self.is_locked:
            return f"🔒 LOCKED ({self.lock_reason})"
            
        if self.type == EVENT_TYPE_BOSS:
            hp_bar = "█" * (self.boss_hp // 100)
            return f"BOSS HP: {self.boss_hp}/1000 [{hp_bar}]"
            
        elif self.type == EVENT_TYPE_CLIMB:
            return f"CURRENT FLOOR: {self.current_floor} 🏢"
            
        elif self.type == EVENT_TYPE_BINGO:
            checked = sum(1 for x in self.bingo_grid if x)
            return f"BINGO GRID: {checked}/9 Cells Unlocked"
            
        return f"PROGRESS: {self.progress}%"

class EventManager:
    """Tüm etkinlik sistemini yöneten ana sınıf"""
    def __init__(self):
        self.current_event = None
        self.collected_cards = [] # Geçmiş etkinlik kartları (Anı defteri)
        self.perfect_streak = 0 # Kaç gündür kusursuz gidiyor?
        self.check_for_new_event()

    def check_for_new_event(self):
        today = date.today()
        day = today.day
        month = today.month
        
        # 1-15 arası Cycle 1, 16-31 arası Cycle 2
        current_cycle = 1 if day <= 15 else 2
        
        # Config'den uygun eventi bul
        event_data = None
        for ev in SEASON_SCHEDULE:
            if ev['month'] == month and ev['cycle'] == current_cycle:
                event_data = ev
                break
        
        # Eğer yeni bir event dönemiyse ve şu anki event farklıysa güncelle
        if event_data:
            if self.current_event is None or self.current_event.name != event_data['name']:
                # Önceki eventi bitir (Varsa kart ver)
                if self.current_event:
                    self.end_current_event(completed=False) # Süre bittiği için
                
                # Yeni eventi başlat
                self.current_event = ActiveEvent(event_data, day)

    def daily_reset(self, daily_score):
        """Gün sonu işlemleri"""
        if not self.current_event: return "No Active Event"
        
        # Kusursuz gün kontrolü (Örn: 100 puan üstü kusursuz olsun)
        is_perfect = daily_score >= 100
        if is_perfect:
            self.perfect_streak += 1
            msg = "🌟 PERFECT DAY! Event streak increased."
        else:
            self.perfect_streak = 0
            msg = "❌ Streak broken."
            
        # Eğer etkinlik bitiş günüyse (15 veya Ay Sonu)
        today = date.today().day
        if today == 15 or today >= 28: # Basit bitiş kontrolü
            card = self.end_current_event(completed=True, final_score=daily_score)
            return f"EVENT ENDED! You earned: {card.name} ({card.rarity})"
            
        # Görevleri yenile
        self.current_event.generate_daily_event_tasks()
        return msg

    def end_current_event(self, completed, final_score=0):
        """Etkinliği bitirir ve kartı oluşturur"""
        if not self.current_event: return None
        
        # Kart oluştur
        # Kusursuzluk şartı: En az 5 gün streak yapmış olmak
        is_perfect_run = self.perfect_streak >= 5
        
        card = EventCard(
            self.current_event.name, 
            self.current_event.type, 
            player_ovr=60, # Burası player.py'den gelecek normalde, şimdilik default
            is_perfect_run=is_perfect_run
        )
        
        self.collected_cards.append(card)
        self.current_event = None # Event bitti
        return card