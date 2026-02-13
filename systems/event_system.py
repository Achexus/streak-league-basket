import random
from datetime import date
from core.config import SEASON_SCHEDULE, EVENT_TYPE_BOSS, EVENT_TYPE_CLIMB, EVENT_TYPE_BINGO, EVENT_TYPE_COLLECT

class EventCard:
    """Etkinlik Sonunda Kazanılan Özel Kart"""
    def __init__(self, name, event_type, player_ovr, is_perfect_run):
        self.name = name
        self.type = event_type
        self.date_earned = date.today().strftime("%d %B %Y")
        self.is_perfect = is_perfect_run
        
        base_boost = int(player_ovr * 0.1)
        if is_perfect_run:
            base_boost += 2
            self.rarity = "LEGENDARY"
        else:
            self.rarity = "RARE"
            
        self.stats = {
            "OFF": base_boost + random.randint(0, 2),
            "DEF": base_boost + random.randint(0, 2),
            "MEN": base_boost + 5
        }

class ActiveEvent:
    """Aktif etkinlik durumu"""
    def __init__(self, event_data, current_day):
        self.data = event_data
        self.name = event_data['name']
        self.type = event_data['type']
        self.emoji = event_data['emoji']
        self.desc = event_data['desc']
        
        self.progress = 0
        self.boss_hp = 1000
        self.current_floor = 1
        self.bingo_grid = [False] * 9
        
        start_day = 1 if event_data['cycle'] == 1 else 16
        if current_day > start_day + 2:
            self.is_locked = True
            self.lock_reason = "Event started before you joined. Wait for next cycle."
        else:
            self.is_locked = False
            self.lock_reason = ""
            
        self.tasks = []
        self.generate_daily_event_tasks()

    def generate_daily_event_tasks(self):
        self.tasks = []
        base_tasks = [
            {"desc": "Complete 3 Daily Habits", "xp": 50, "val": 100},
            {"desc": "Win 1 League Match", "xp": 100, "val": 200},
            {"desc": "Don't skip any habit today", "xp": 150, "val": 300}
        ]
        
        for t in base_tasks:
            desc = t['desc']
            if self.type == EVENT_TYPE_BOSS: desc += f" (Deal {t['val']} DMG)"
            elif self.type == EVENT_TYPE_CLIMB: desc += " (Climb 1 Floor)"
            elif self.type == EVENT_TYPE_COLLECT: desc += " (Find 1 Token)"
            
            self.tasks.append({
                "task": desc,
                "xp": t['xp'],
                "done": False,
                "val": t['val']
            })

    def complete_task(self, index):
        if 0 <= index < len(self.tasks) and not self.tasks[index]['done']:
            task = self.tasks[index]
            task['done'] = True
            
            if self.type == EVENT_TYPE_BOSS:
                self.boss_hp -= task['val']
                if self.boss_hp < 0: self.boss_hp = 0
            elif self.type == EVENT_TYPE_CLIMB:
                self.current_floor += 1
            elif self.type == EVENT_TYPE_BINGO:
                empty_slots = [i for i, x in enumerate(self.bingo_grid) if not x]
                if empty_slots: self.bingo_grid[random.choice(empty_slots)] = True
            else:
                self.progress += 10

            return task['xp']
        return 0

class EventManager:
    """Etkinlik yöneticisi"""
    def __init__(self):
        self.current_event = None
        self.collected_cards = []
        self.perfect_streak = 0
        self.check_for_new_event()

    def check_for_new_event(self):
        today = date.today()
        day = today.day
        month = today.month
        current_cycle = 1 if day <= 15 else 2
        
        event_data = None
        for ev in SEASON_SCHEDULE:
            if ev['month'] == month and ev['cycle'] == current_cycle:
                event_data = ev
                break
        
        if event_data:
            if self.current_event is None or self.current_event.name != event_data['name']:
                if self.current_event: self.end_current_event(completed=False)
                self.current_event = ActiveEvent(event_data, day)

    def daily_reset(self, daily_score):
        if not self.current_event: return "No Active Event"
        
        is_perfect = daily_score >= 100
        if is_perfect:
            self.perfect_streak += 1
            msg = "🌟 PERFECT DAY! Streak increased."
        else:
            self.perfect_streak = 0
            msg = "❌ Streak broken."
            
        today = date.today().day
        if today == 15 or today >= 28:
            card = self.end_current_event(completed=True)
            return f"EVENT ENDED! Earned: {card.name}"
            
        self.current_event.generate_daily_event_tasks()
        return msg

    def end_current_event(self, completed):
        if not self.current_event: return None
        is_perfect_run = self.perfect_streak >= 5
        card = EventCard(self.current_event.name, self.current_event.type, 60, is_perfect_run)
        self.collected_cards.append(card)
        self.current_event = None
        return card