# stats.py
import random

class StatsManager:
    def __init__(self, position):
        # 3 Ana Hayal
        self.dreams = ["", "", ""] 
        
        # FUT KART STATLARI (60-70 arası başlar)
        self.attributes = {
            "SHT": random.randint(60, 70), 
            "FIN": random.randint(60, 70), 
            "DEF": random.randint(55, 65), 
            "PAS": random.randint(60, 70), 
            "REB": random.randint(50, 65), 
            "MEN": random.randint(65, 75)  
        }
        
        self.apply_position_bonus(position)

    def apply_position_bonus(self, pos):
        if pos == "PG":
            self.attributes["PAS"] += 10; self.attributes["SHT"] += 5
        elif pos == "SG":
            self.attributes["SHT"] += 10; self.attributes["FIN"] += 5
        elif pos == "SF":
            self.attributes["FIN"] += 8; self.attributes["DEF"] += 7
        elif pos == "PF":
            self.attributes["REB"] += 8; self.attributes["DEF"] += 7
        elif pos == "C":
            self.attributes["REB"] += 12; self.attributes["FIN"] += 5
            self.attributes["SHT"] -= 5

    def get_overall(self):
        return int(sum(self.attributes.values()) / 6)

    def set_dreams(self, d1, d2, d3):
        self.dreams = [d1, d2, d3]
        
    def upgrade_stat(self, stat_key, amount=1):
        if stat_key in self.attributes:
            self.attributes[stat_key] += amount
            if self.attributes[stat_key] > 99: self.attributes[stat_key] = 99