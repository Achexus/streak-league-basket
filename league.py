# league.py
import random
from config import TURKEY_DATA, ADJECTIVES, TEAM_SUFFIXES

class Team:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        # Takım gücü (Rastgele)
        self.offense = random.randint(65, 95)
        self.defense = random.randint(65, 95)
    
    def get_record(self):
        return f"{self.wins}-{self.losses}"

class League:
    def __init__(self, city_code):
        self.city_name = TURKEY_DATA[city_code]['name']
        self.teams = []
        self.conf_a = []
        self.conf_b = []
        self.generate_league(city_code)
        
    def generate_league(self, city_code):
        city_data = TURKEY_DATA[city_code]
        districts = city_data['districts']
        
        target_count = 32
        generated_names = set()
        
        # Yeterli takım çıkana kadar üret
        while len(self.teams) < target_count:
            dist = random.choice(districts)
            adj = random.choice(ADJECTIVES)
            suf = random.choice(TEAM_SUFFIXES)
            team_name = f"{dist} {adj} {suf}"
            
            if team_name not in generated_names:
                generated_names.add(team_name)
                self.teams.append(Team(team_name))
        
        random.shuffle(self.teams)
        self.conf_a = self.teams[:16]
        self.conf_b = self.teams[16:]