# core/config.py

# --- OYUN AYARLARI ---
XP_VALUES = {'E': 10, 'M': 25, 'H': 50}

STAT_NAMES = {
    "OFF": "OFFENSE", "DEF": "DEFENSE", "PHY": "PHYSICAL",
    "MEN": "MENTAL", "TEC": "TECHNIQUE"
}

# --- ETKİNLİK TİPLERİ ---
EVENT_TYPE_BOSS = "BOSS_BATTLE"
EVENT_TYPE_CLIMB = "STAGE_CLIMB"
EVENT_TYPE_BOARD = "BOARD_GAME"
EVENT_TYPE_STORY = "STORY_MODE"
EVENT_TYPE_BINGO = "BINGO_GRID"
EVENT_TYPE_COLLECT = "COLLECTION"
EVENT_TYPE_SURVIVAL = "SURVIVAL"
EVENT_TYPE_TOURNEY = "TOURNAMENT"
EVENT_TYPE_CRAFT = "CRAFTING"
EVENT_TYPE_TIME = "TIME_ATTACK"
EVENT_TYPE_PUZZLE = "PUZZLE_PIECE"
EVENT_TYPE_TRAIN = "TRAINING_CAMP"

# --- 12 AYLIK ETKİNLİK TAKVİMİ (SEASON_SCHEDULE) ---
SEASON_SCHEDULE = [
    {"month": 1, "cycle": 1, "name": "New Year's Resolution", "emoji": "🏔️", "type": EVENT_TYPE_CLIMB, "desc": "Yeni yıl zirvesine tırman."},
    {"month": 1, "cycle": 2, "name": "Frozen Lake Survival", "emoji": "❄️", "type": EVENT_TYPE_SURVIVAL, "desc": "Buz kırılmadan ilerle."},
    {"month": 2, "cycle": 1, "name": "Cupid's Target", "emoji": "💘", "type": EVENT_TYPE_BOSS, "desc": "Aşk Boss'unu yen!"},
    {"month": 2, "cycle": 2, "name": "Winter Training Camp", "emoji": "🏋️", "type": EVENT_TYPE_TRAIN, "desc": "Fiziksel statları katla."},
    {"month": 3, "cycle": 1, "name": "Luck of the Irish", "emoji": "🍀", "type": EVENT_TYPE_BOARD, "desc": "Yonca tarlasında zar at."},
    {"month": 3, "cycle": 2, "name": "Spring Cleaning", "emoji": "🧹", "type": EVENT_TYPE_BINGO, "desc": "Dağınıklığı topla (Bingo)."},
    {"month": 4, "cycle": 1, "name": "Easter Egg Hunt", "emoji": "🥚", "type": EVENT_TYPE_COLLECT, "desc": "Saklı yumurtaları bul."},
    {"month": 4, "cycle": 2, "name": "The Jester's Riddle", "emoji": "🃏", "type": EVENT_TYPE_STORY, "desc": "Soytarının bilmecelerini çöz."},
    {"month": 5, "cycle": 1, "name": "Labor Ladder", "emoji": "🏗️", "type": EVENT_TYPE_CRAFT, "desc": "Kartını inşa et."},
    {"month": 5, "cycle": 2, "name": "Blossom Festival", "emoji": "🌸", "type": EVENT_TYPE_PUZZLE, "desc": "Çiçek desenini tamamla."},
    {"month": 6, "cycle": 1, "name": "Summer Heat Wave", "emoji": "🔥", "type": EVENT_TYPE_TIME, "desc": "Sıcakta erimeden görev yap."},
    {"month": 6, "cycle": 2, "name": "Beach Volley Tourney", "emoji": "🏐", "type": EVENT_TYPE_TOURNEY, "desc": "Kumsalda turnuva."},
    {"month": 7, "cycle": 1, "name": "Independence Boss", "emoji": "🎆", "type": EVENT_TYPE_BOSS, "desc": "Havai Fişek Boss'unu patlat."},
    {"month": 7, "cycle": 2, "name": "Star Gazing", "emoji": "🔭", "type": EVENT_TYPE_COLLECT, "desc": "Takımyıldızları birleştir."},
    {"month": 8, "cycle": 1, "name": "Deep Sea Dive", "emoji": "🤿", "type": EVENT_TYPE_CLIMB, "desc": "Okyanusun derinliklerine in."},
    {"month": 8, "cycle": 2, "name": "Pre-Season Grind", "emoji": "👟", "type": EVENT_TYPE_TRAIN, "desc": "Hazırlık kampında ter dök."},
    {"month": 9, "cycle": 1, "name": "Back to School", "emoji": "📚", "type": EVENT_TYPE_STORY, "desc": "Akademi macerası."},
    {"month": 9, "cycle": 2, "name": "Autumn Harvest", "emoji": "🍂", "type": EVENT_TYPE_BINGO, "desc": "Hasat zamanı (Bingo)."},
    {"month": 10, "cycle": 1, "name": "Zombie Dunker", "emoji": "🧟", "type": EVENT_TYPE_BOSS, "desc": "Zombi smaçöre blok koy!"},
    {"month": 10, "cycle": 2, "name": "Haunted Mansion", "emoji": "👻", "type": EVENT_TYPE_BOARD, "desc": "Perili evde ilerle."},
    {"month": 11, "cycle": 1, "name": "Thanksgiving Feast", "emoji": "🦃", "type": EVENT_TYPE_CRAFT, "desc": "Ziyafeti hazırla."},
    {"month": 11, "cycle": 2, "name": "Black Friday Rush", "emoji": "🛍️", "type": EVENT_TYPE_TIME, "desc": "İndirim bitmeden yetiş."},
    {"month": 12, "cycle": 1, "name": "Advent Calendar", "emoji": "📆", "type": EVENT_TYPE_PUZZLE, "desc": "Her gün bir kutu aç."},
    {"month": 12, "cycle": 2, "name": "Santa's Workshop", "emoji": "🎅", "type": EVENT_TYPE_STORY, "desc": "Elflere yardım et."}
]

# --- 16 BÜYÜKŞEHİR VERİSİ ---
TURKEY_DATA = {
    1: {"name": "Istanbul", "districts": ["Kadikoy", "Besiktas", "Beyoglu", "Fatih", "Uskudar", "Sisli", "Maltepe", "Kartal"]},
    2: {"name": "Ankara", "districts": ["Cankaya", "Kecioren", "Mamak", "Sincan", "Altindag", "Golbasi"]},
    3: {"name": "Izmir", "districts": ["Karsiyaka", "Konak", "Bornova", "Buca", "Goztepe", "Alsancak"]},
    4: {"name": "Bursa", "districts": ["Nilufer", "Osmangazi", "Yildirim", "Mudanya", "Inegol"]},
    5: {"name": "Antalya", "districts": ["Muratpasa", "Lara", "Kepez", "Konyaalti", "Alanya", "Kas"]},
    6: {"name": "Adana", "districts": ["Seyhan", "Cukurova", "Yuregir", "Kozan"]},
    7: {"name": "Konya", "districts": ["Selcuklu", "Meram", "Karatay", "Aksehir"]},
    8: {"name": "Gaziantep", "districts": ["Sahinbey", "Sehitkamil", "Nizip"]},
    9: {"name": "Sanliurfa", "districts": ["Eyyubiye", "Haliliye", "Siverek"]},
    10: {"name": "Kocaeli", "districts": ["Izmit", "Gebze", "Darica", "Golcuk"]},
    11: {"name": "Mersin", "districts": ["Yenisehir", "Mezitli", "Tarsus", "Toroslar"]},
    12: {"name": "Diyarbakir", "districts": ["Baglar", "Kayapinar", "Sur", "Yenisehir"]},
    13: {"name": "Hatay", "districts": ["Antakya", "Iskenderun", "Defne"]},
    14: {"name": "Manisa", "districts": ["Yunusemre", "Sehzadeler", "Akhisar", "Turgutlu"]},
    15: {"name": "Kayseri", "districts": ["Melikgazi", "Kocasinan", "Talas"]},
    16: {"name": "Samsun", "districts": ["Ilkadim", "Atakum", "Canik", "Bafra"]}
}

# 350+ Takım Kimliği (Maskotlar/Sıfatlar)
TEAM_MASCOTS = [
    "Lions", "Tigers", "Eagles", "Wolves", "Bears", "Falcons", "Hawks", "Panthers", "Bulls", "Dragons",
    "Sharks", "Cobras", "Vipers", "Ravens", "Knights", "Wizards", "Titans", "Giants", "Spartans", "Vikings",
    "Storm", "Thunder", "Lightning", "Cyclones", "Hurricanes", "Tornadoes", "Blizzard", "Heat", "Suns",
    "Stars", "Comets", "Galaxy", "Universe", "Rockets", "Jets", "Pilots", "Marines", "Soldiers", "Warriors"
]