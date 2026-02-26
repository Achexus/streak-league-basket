import json
import os
from datetime import date

SAVE_FILE = "data/savegame.json"

class Player:
    def __init__(self, name, jersey_number, position, city, team_name):
        self.name = name
        self.jersey_number = jersey_number
        self.position = position
        
        # YENİ EKLENENLER: Şehir ve Takım
        self.city = city
        self.team_name = team_name
        
        self.stats = {
            "SHOOTING": 50,
            "DEFENSE": 50,
            "PLAYMAKING": 50
        }
        
        self.level = 1
        self.xp = 0
        self.streak = 0
        self.last_login_date = str(date.today())
        self.daily_tasks = [] 
        
    def to_dict(self):
        return {
            "name": self.name,
            "jersey_number": self.jersey_number,
            "position": self.position,
            "city": self.city,
            "team_name": self.team_name,
            "stats": self.stats,
            "level": self.level,
            "xp": self.xp,
            "streak": self.streak,
            "last_login_date": self.last_login_date,
            "daily_tasks": self.daily_tasks
        }
        
    @classmethod
    def from_dict(cls, data):
        p = cls(
            name=data["name"], 
            jersey_number=data.get("jersey_number", "00"), 
            position=data.get("position", "PG"),
            city=data.get("city", "Unknown City"),
            team_name=data.get("team_name", "Free Agent")
        )
        p.stats = data.get("stats", p.stats)
        p.level = data.get("level", 1)
        p.xp = data.get("xp", 0)
        p.streak = data.get("streak", 0)
        p.last_login_date = data.get("last_login_date", str(date.today()))
        p.daily_tasks = data.get("daily_tasks", [])
        return p

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)
            
    @staticmethod
    def load():
        if not os.path.exists(SAVE_FILE):
            return None
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Player.from_dict(data)