# stats.py

class StatItem:
    def __init__(self, name, category):
        self.name = name
        self.category = category # 'Dream' or 'Improvement'
        self.value = 50 # Başlangıç değeri

class StatsManager:
    def __init__(self):
        self.dreams = []       # Hücum gücünü etkiler
        self.improvements = [] # Defans/Gücü etkiler
        
    def add_dream(self, name):
        """Hücum statı ekler"""
        self.dreams.append(StatItem(name, 'Dream'))
        
    def add_improvement(self, name):
        """Defans/Gelişim statı ekler"""
        self.improvements.append(StatItem(name, 'Improvement'))

    def get_offense_power(self, level):
        """
        Hücum gücü hesaplama:
        Temel 50 + (Hayal Sayısı * 2) + (Level * 2)
        """
        base = 50
        dream_bonus = len(self.dreams) * 2
        level_bonus = level * 2
        return base + dream_bonus + level_bonus

    def get_defense_power(self, level):
        """
        Defans gücü hesaplama:
        Temel 50 + (Gelişim Hedefi Sayısı * 2) + (Level * 2)
        """
        base = 50
        imp_bonus = len(self.improvements) * 2
        level_bonus = level * 2
        return base + imp_bonus + level_bonus