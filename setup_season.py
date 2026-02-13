import json
import random
import os
from core.config import TURKEY_DATA, TEAM_MASCOTS

DATA_FILE = "data/season_data.json"

class TeamGenerator:
    def __init__(self):
        self.used_names = set()

    def create_team(self, city, districts, is_national=False):
        # Takım Gücü Ayarlama
        if is_national:
            off = random.randint(80, 99)
            def_ = random.randint(80, 99)
            prefix = f"{city} United"
        else:
            off = random.randint(60, 90)
            def_ = random.randint(60, 90)
            dist = random.choice(districts)
            mascot = random.choice(TEAM_MASCOTS)
            prefix = f"{dist} {mascot}"

        # İsim Benzersizliği Kontrolü
        counter = 1
        base_name = prefix
        while prefix in self.used_names:
            prefix = f"{base_name} {counter}"
            counter += 1
        
        self.used_names.add(prefix)
        
        return {
            "name": prefix,
            "city": city,
            "wins": 0, "losses": 0,
            "offense": off, "defense": def_
        }

def generate_round_robin_schedule(teams):
    """32 Takımlı Lig Fikstürü Oluşturucu"""
    schedule = {}
    if len(teams) % 2 == 1: teams.append(None)
    n = len(teams)
    team_names = [t['name'] for t in teams]
    rounds = (n - 1) * 2
    
    for r in range(rounds):
        week_matches = []
        for i in range(n // 2):
            t1 = team_names[i]
            t2 = team_names[n - 1 - i]
            # Rövanş mantığı
            if r >= (n - 1): t1, t2 = t2, t1
            
            week_matches.append({
                "home": t1, 
                "away": t2, 
                "played": False, 
                "score": None
            })
        schedule[r + 1] = week_matches
        
        # Takımları kaydır
        team_names = [team_names[0]] + [team_names[-1]] + team_names[1:-1]
        
    return schedule

def main():
    # Data klasörü yoksa oluştur
    if not os.path.exists("data"):
        os.makedirs("data")
        
    print("⚙️  GENERATING SEASON DATABASE (This may take a moment)...")
    
    gen = TeamGenerator()
    database = {
        "leagues": {},
        "current_week": 1
    }
    
    # 1. ULUSAL LİG OLUŞTURMA
    print("   - Drafting National League (32 Teams)...")
    national_teams = []
    for code, data in TURKEY_DATA.items():
        # Her şehirden 2 takım al
        for _ in range(2):
            national_teams.append(gen.create_team(data['name'], data['districts'], is_national=True))
            
    database["leagues"]["NATIONAL_LEAGUE"] = {
        "name": "TURKEY SUPER LEAGUE",
        "city_name": "Turkey", # <--- HATA DÜZELTİCİ SATIR
        "teams": national_teams,
        "fixtures": generate_round_robin_schedule(national_teams)
    }
    
    # 2. ŞEHİR LİGLERİ OLUŞTURMA (16 LİG)
    print("   - Drafting 16 City Leagues (32 Teams each)...")
    for code, data in TURKEY_DATA.items():
        city_teams = []
        # Her şehre 32 takım
        for _ in range(32):
            city_teams.append(gen.create_team(data['name'], data['districts'], is_national=False))
            
        database["leagues"][f"CITY_{code}"] = {
            "name": f"{data['name'].upper()} LEAGUE",
            "city_name": data['name'], # <--- HATA DÜZELTİCİ SATIR (UI Bunu Arıyor)
            "teams": city_teams,
            "fixtures": generate_round_robin_schedule(city_teams)
        }
        
    # KAYDET
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
        
    print(f"✅ SUCCESS! Database saved to {DATA_FILE}")
    print("   You can now run 'main.py'")

if __name__ == "__main__":
    main()