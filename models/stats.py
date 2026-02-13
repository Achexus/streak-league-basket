import random

class StatsManager:
    def __init__(self, position):
        self.dreams = ["", "", ""] 
        # Rastgele başlangıç güçleri
        self.attributes = {
            "OFF": random.randint(60, 70),
            "DEF": random.randint(55, 65),
            "PHY": random.randint(50, 65),
            "MEN": random.randint(60, 70),
            "TEC": random.randint(55, 65)
        }
        self.apply_position_bonus(position)

    def apply_position_bonus(self, pos):
        if pos == "PG":
            self.attributes["TEC"] += 10; self.attributes["OFF"] += 5
        elif pos == "SG":
            self.attributes["OFF"] += 10; self.attributes["TEC"] += 5
        elif pos == "SF":
            self.attributes["OFF"] += 8; self.attributes["PHY"] += 7
        elif pos == "PF":
            self.attributes["PHY"] += 10; self.attributes["DEF"] += 5
        elif pos == "C":
            self.attributes["DEF"] += 10; self.attributes["PHY"] += 10; self.attributes["TEC"] -= 5

    def get_overall(self):
        return int(sum(self.attributes.values()) / 5)

    def set_dreams(self, d1, d2, d3):
        self.dreams = [d1, d2, d3]
        
    def upgrade_stat(self, stat_key, amount=1):
        if stat_key in self.attributes:
            self.attributes[stat_key] += amount
            if self.attributes[stat_key] > 99: self.attributes[stat_key] = 99