# league.py
import random
from config import TURKEY_DATA, TEAM_IDENTITIES

class Team:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        # Takım gücü (Rastgele - Lig oluşturulurken atanır)
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
        
        # --- YENİ İSİM ALGORİTMASI ---
        # 1. Havuzu kopyala ve karıştır (Her oyun farklı olsun diye)
        name_pool = list(TEAM_IDENTITIES)
        random.shuffle(name_pool)
        
        # 2. Takımları oluştur
        while len(self.teams) < target_count:
            # Rastgele bir ilçe seç
            dist = random.choice(districts)
            
            # Havuzdan benzersiz bir kimlik çek (Pop: listeden silerek alır)
            if not name_pool:
                # Eğer havuz biterse (350 takımdan fazla olursa) başa sar
                name_pool = list(TEAM_IDENTITIES)
                random.shuffle(name_pool)
                
            identity = name_pool.pop()
            
            # İsim Formatı: "Muratpasa Lions" veya "Lara Storm"
            team_name = f"{dist} {identity}"
            
            # Eğer bu isim (ilçe + kimlik) daha önce çıktıysa ekleme (Çok düşük ihtimal ama önlem)
            if not any(t.name == team_name for t in self.teams):
                self.teams.append(Team(team_name))
        
        # 3. Konferanslara Böl
        random.shuffle(self.teams)
        self.conf_a = self.teams[:16]
        self.conf_b = self.teams[16:]