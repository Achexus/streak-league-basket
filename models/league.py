import json
import os

DATA_FILE = "data/season_data.json"

class Team:
    def __init__(self, data):
        self.name = data['name']
        self.city = data['city']
        self.wins = data['wins']
        self.losses = data['losses']
        self.offense = data['offense']
        self.defense = data['defense']
        
    def get_record(self):
        return f"{self.wins}-{self.losses}"

class MatchFixture:
    def __init__(self, data, home_obj, away_obj):
        self.home_team = home_obj
        self.away_team = away_obj
        self.played = data['played']
        self.home_score = 0
        self.away_score = 0
        if data['score']:
            self.home_score = data['score'][0]
            self.away_score = data['score'][1]

    def __str__(self):
        if self.played:
            return f"{self.home_team.name} {self.home_score}-{self.away_score} {self.away_team.name}"
        return f"{self.home_team.name} vs {self.away_team.name}"

class League:
    def __init__(self, league_id, league_data):
        self.id = league_id
        self.name = league_data['name']
        self.city_name = league_data.get('city_name', 'Unknown City')
        
        # Takımları yükle
        self.teams = [Team(t) for t in league_data['teams']]
        
        # --- HATA DÜZELTME: KONFERANSLAR ---
        # Ligdeki 32 takımı ortadan ikiye bölüyoruz (16-16)
        # Böylece UI hatasız çalışacak (conf_a ve conf_b)
        mid_point = len(self.teams) // 2
        self.conf_a = self.teams[:mid_point]
        self.conf_b = self.teams[mid_point:]
        
        self.fixtures = {} 
        self.current_week = 1
        self._load_fixtures(league_data['fixtures'])
        
    def _load_fixtures(self, fixtures_data):
        team_map = {t.name: t for t in self.teams}
        for week, matches in fixtures_data.items():
            match_objects = []
            for m in matches:
                home = team_map.get(m['home'])
                away = team_map.get(m['away'])
                if home and away:
                    match_objects.append(MatchFixture(m, home, away))
            self.fixtures[int(week)] = match_objects

    def get_week_fixtures(self, week):
        return self.fixtures.get(week, [])
    
    def get_my_match(self, my_team_obj, week=None):
        if week is None: week = self.current_week
        week_matches = self.fixtures.get(week, [])
        for m in week_matches:
            if m.home_team.name == my_team_obj.name or m.away_team.name == my_team_obj.name:
                return m
        return None

class LeagueManager:
    def __init__(self):
        self.leagues = {}
        self.current_week = 1
        self.load_database()
        
    def load_database(self):
        if not os.path.exists(DATA_FILE):
            raise FileNotFoundError("Run 'setup_season.py' first!")
            
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.current_week = data.get('current_week', 1)
        
        for lid, ldata in data['leagues'].items():
            new_league = League(lid, ldata)
            new_league.current_week = self.current_week 
            self.leagues[lid] = new_league
            
    def get_league(self, league_id):
        return self.leagues.get(league_id)

    def get_all_leagues(self):
        return self.leagues.values()