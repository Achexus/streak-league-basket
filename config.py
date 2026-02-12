# config.py

# --- OYUN AYARLARI ---
XP_VALUES = {'E': 10, 'M': 25, 'H': 50}

# SADELEŞTİRİLMİŞ STAT İSİMLERİ (YENİ KART TASARIMI İÇİN)
STAT_NAMES = {
    "OFF": "OFFENSE",  # Hücum (Şut, Bitiricilik)
    "DEF": "DEFENSE",  # Defans (Çalma, Blok)
    "PHY": "PHYSICAL", # Fizik (Kondisyon, Güç)
    "MEN": "MENTAL",   # Mental (Zeka, Soğukkanlılık)
    "TEC": "TECHNIQUE" # Teknik (Pas, Dribling)
}

# --- ETKİNLİK TİPLERİ (OYUN MODLARI) ---
# Bu tipler mechanics.py içinde farklı mantıklarla çalışacak.
EVENT_TYPE_BOSS = "BOSS_BATTLE"       # Görev yaptıkça Boss'un canı azalır
EVENT_TYPE_CLIMB = "STAGE_CLIMB"      # Kule tırmanışı (Kat 1, Kat 2...)
EVENT_TYPE_BOARD = "BOARD_GAME"       # Monopoly tarzı, görev yaptıkça piyon ilerler
EVENT_TYPE_STORY = "STORY_MODE"       # Hikayeli, seçimli ilerleme
EVENT_TYPE_BINGO = "BINGO_GRID"       # 3x3 veya 4x4 görev kutularını tamamlama
EVENT_TYPE_COLLECT = "COLLECTION"     # Token toplama (Örn: Paskalya Yumurtası)
EVENT_TYPE_SURVIVAL = "SURVIVAL"      # Hiç hata yapmadan zinciri koruma
EVENT_TYPE_TOURNEY = "TOURNAMENT"     # Eleme usulü maç simülasyonu
EVENT_TYPE_CRAFT = "CRAFTING"         # Parça toplayıp kartı inşa etme
EVENT_TYPE_TIME = "TIME_ATTACK"       # Belirli sürede maksimum görev
EVENT_TYPE_PUZZLE = "PUZZLE_PIECE"    # Kartın parçalarını açma
EVENT_TYPE_TRAIN = "TRAINING_CAMP"    # Saf stat odaklı gelişim kampı

# --- 12 AYLIK ETKİNLİK TAKVİMİ (24 EVENT) ---
# Cycle 1: Ayın 1-15'i
# Cycle 2: Ayın 16-30'u
SEASON_SCHEDULE = [
    # OCAK
    {
        "month": 1, "cycle": 1, "name": "New Year's Resolution", "emoji": "🏔️", 
        "type": EVENT_TYPE_CLIMB, "desc": "Yeni yıl zirvesine tırman. Her görev bir adımdır."
    },
    {
        "month": 1, "cycle": 2, "name": "Frozen Lake Survival", "emoji": "❄️", 
        "type": EVENT_TYPE_SURVIVAL, "desc": "Buz kırılmadan ilerle. Hata yaparsan donarsın."
    },
    # ŞUBAT
    {
        "month": 2, "cycle": 1, "name": "Cupid's Target", "emoji": "💘", 
        "type": EVENT_TYPE_BOSS, "desc": "Aşk Boss'unu yen! Görevler kalbine ok atar."
    },
    {
        "month": 2, "cycle": 2, "name": "Winter Training Camp", "emoji": "🏋️", 
        "type": EVENT_TYPE_TRAIN, "desc": "Sezon ortası yüklemesi. Fiziksel statları katla."
    },
    # MART
    {
        "month": 3, "cycle": 1, "name": "Luck of the Irish", "emoji": "🍀", 
        "type": EVENT_TYPE_BOARD, "desc": "Yonca tarlasında zar at. Hazineleri topla."
    },
    {
        "month": 3, "cycle": 2, "name": "Spring Cleaning", "emoji": "🧹", 
        "type": EVENT_TYPE_BINGO, "desc": "Dağınıklığı topla. Bingo yaparak ödül kazan."
    },
    # NİSAN
    {
        "month": 4, "cycle": 1, "name": "Easter Egg Hunt", "emoji": "🥚", 
        "type": EVENT_TYPE_COLLECT, "desc": "Saklı yumurtaları bul. Koleksiyonu tamamla."
    },
    {
        "month": 4, "cycle": 2, "name": "The Jester's Riddle", "emoji": "🃏", 
        "type": EVENT_TYPE_STORY, "desc": "Soytarının bilmecelerini çöz. Hikayeyi bitir."
    },
    # MAYIS
    {
        "month": 5, "cycle": 1, "name": "Labor Ladder", "emoji": "🏗️", 
        "type": EVENT_TYPE_CRAFT, "desc": "Kendi özel kartını inşa et. Malzeme topla."
    },
    {
        "month": 5, "cycle": 2, "name": "Blossom Festival", "emoji": "🌸", 
        "type": EVENT_TYPE_PUZZLE, "desc": "Çiçek desenini tamamla. Resmi ortaya çıkar."
    },
    # HAZİRAN
    {
        "month": 6, "cycle": 1, "name": "Summer Heat Wave", "emoji": "🔥", 
        "type": EVENT_TYPE_TIME, "desc": "Sıcakta erimeden maksimum görevi yap."
    },
    {
        "month": 6, "cycle": 2, "name": "Beach Volley Tourney", "emoji": "🏐", 
        "type": EVENT_TYPE_TOURNEY, "desc": "Kumsalda turnuva. Rakipleri ele."
    },
    # TEMMUZ
    {
        "month": 7, "cycle": 1, "name": "Independence Boss", "emoji": "🎆", 
        "type": EVENT_TYPE_BOSS, "desc": "Devasa Havai Fişek Boss'unu patlat."
    },
    {
        "month": 7, "cycle": 2, "name": "Star Gazing", "emoji": "🔭", 
        "type": EVENT_TYPE_COLLECT, "desc": "Takımyıldızları birleştir. Gökyüzünü keşfet."
    },
    # AĞUSTOS
    {
        "month": 8, "cycle": 1, "name": "Deep Sea Dive", "emoji": "🤿", 
        "type": EVENT_TYPE_CLIMB, "desc": "Okyanusun derinliklerine in (Ters Tırmanış)."
    },
    {
        "month": 8, "cycle": 2, "name": "Pre-Season Grind", "emoji": "👟", 
        "type": EVENT_TYPE_TRAIN, "desc": "Lig başlıyor! Hazırlık kampında ter dök."
    },
    # EYLÜL
    {
        "month": 9, "cycle": 1, "name": "Back to School", "emoji": "📚", 
        "type": EVENT_TYPE_STORY, "desc": "Basketbol Akademisi macerası. Sınavları geç."
    },
    {
        "month": 9, "cycle": 2, "name": "Autumn Harvest", "emoji": "🍂", 
        "type": EVENT_TYPE_BINGO, "desc": "Hasat zamanı. Ürünleri topla (Bingo)."
    },
    # EKİM
    {
        "month": 10, "cycle": 1, "name": "Zombie Dunker", "emoji": "🧟", 
        "type": EVENT_TYPE_BOSS, "desc": "Zombi smaçöre blok koy! Canını azalt."
    },
    {
        "month": 10, "cycle": 2, "name": "Haunted Mansion", "emoji": "👻", 
        "type": EVENT_TYPE_BOARD, "desc": "Perili evde ilerle. Hayaletlerden kaç."
    },
    # KASIM
    {
        "month": 11, "cycle": 1, "name": "Thanksgiving Feast", "emoji": "🦃", 
        "type": EVENT_TYPE_CRAFT, "desc": "Mükemmel ziyafeti hazırla. Kartını pişir."
    },
    {
        "month": 11, "cycle": 2, "name": "Black Friday Rush", "emoji": "🛍️", 
        "type": EVENT_TYPE_TIME, "desc": "İndirim bitmeden görevleri kapış."
    },
    # ARALIK
    {
        "month": 12, "cycle": 1, "name": "Advent Calendar", "emoji": "📆", 
        "type": EVENT_TYPE_PUZZLE, "desc": "Her gün bir kutu aç. Büyük resme ulaş."
    },
    {
        "month": 12, "cycle": 2, "name": "Santa's Workshop", "emoji": "🎅", 
        "type": EVENT_TYPE_STORY, "desc": "Kuzey kutbunda elflere yardım et."
    }
]

# --- TAKIM İSİM HAVUZU (350+ BENZERSİZ KİMLİK) ---
TEAM_IDENTITIES = [
    # Animals
    "Lions", "Tigers", "Eagles", "Sharks", "Wolves", "Bears", "Falcons", "Hawks", "Panthers", "Dragons",
    "Bulls", "Foxes", "Cobras", "Vipers", "Pythons", "Ravens", "Crows", "Owls", "Stags", "Bucks",
    "Rams", "Goats", "Boars", "Rhinos", "Hippos", "Gators", "Crocs", "Toads", "Frogs", "Bats",
    "Spiders", "Scorpions", "Wasps", "Bees", "Ants", "Beetles", "Mantis", "Cranes", "Swans", "Ducks",
    "Geese", "Gulls", "Pelicans", "Herons", "Orcas", "Whales", "Dolphins", "Seals", "Otters", "Beavers",
    "Badgers", "Raccoons", "Pandas", "Koalas", "Lemurs", "Monkeys", "Apes", "Gorillas", "Chimps", "Lynx",
    "Pumas", "Jaguars", "Leopards", "Cheetahs", "Hyenas", "Jackals", "Coyotes", "Dingos", "Huskies", "Pugs",
    "Mastiffs", "Bulldogs", "Boxers", "Terriers", "Hounds", "Beagles", "Collies", "Shepherds", "Danes",
    "Horses", "Stallions", "Mustangs", "Broncos", "Colts", "Mules", "Donkeys", "Camels", "Llamas", "Alpacas",
    "Bison", "Buffalo", "Oxen", "Yaks", "Elk", "Moose", "Deer", "Gazelles", "Impalas", "Zebras",
    
    # Mythology & Fantasy
    "Titans", "Giants", "Cyclops", "Hydras", "Griffins", "Phoenix", "Pegasus", "Unicorns", "Centaurs", "Minotaurs",
    "Satyrs", "Nymphs", "Dryads", "Elves", "Dwarves", "Orcs", "Goblins", "Trolls", "Ogres", "Golems",
    "Wraiths", "Ghosts", "Spirits", "Phantoms", "Specters", "Shadows", "Shades", "Souls", "Demons", "Devils",
    "Angels", "Saints", "Gods", "Lords", "Kings", "Queens", "Princes", "Knights", "Paladins", "Mages",
    "Wizards", "Witches", "Sorcerers", "Warlocks", "Druids", "Clerics", "Monks", "Ninjas", "Samurai", "Vikings",
    "Spartans", "Trojans", "Romans", "Greeks", "Celts", "Saxons", "Vandals", "Huns", "Mongols", "Aztecs",
    "Mayans", "Incas", "Pharaohs", "Mummies", "Zombies", "Vampires", "Werewolves", "Aliens", "Martians", "Cyborgs",
    
    # Nature & Elements
    "Storm", "Thunder", "Lightning", "Rain", "Wind", "Breeze", "Gale", "Gust", "Tornado", "Hurricane",
    "Cyclone", "Typhoon", "Blizzard", "Snow", "Ice", "Frost", "Hail", "Sleet", "Fog", "Mist",
    "Cloud", "Sky", "Sun", "Moon", "Star", "Comet", "Meteor", "Asteroid", "Planet", "Galaxy",
    "Cosmos", "Universe", "Void", "Abyss", "Deep", "Ocean", "Sea", "River", "Lake", "Pond",
    "Stream", "Creek", "Waterfall", "Wave", "Tide", "Current", "Flow", "Surge", "Flood", "Drought",
    "Desert", "Sand", "Dune", "Rock", "Stone", "Boulder", "Pebble", "Mountain", "Peak", "Summit",
    "Cliff", "Valley", "Canyon", "Forest", "Woods", "Jungle", "Swamp", "Marsh", "Bog", "Field",
    "Meadow", "Grass", "Flower", "Bloom", "Rose", "Lily", "Thorn", "Vine", "Root", "Leaf",
    "Tree", "Oak", "Pine", "Cedar", "Maple", "Willow", "Birch", "Ash", "Elm", "Palm",
    
    # Concepts
    "Force", "Power", "Energy", "Strength", "Might", "Vigor", "Vitality", "Life", "Death", "Chaos",
    "Order", "Law", "Justice", "Honor", "Glory", "Pride", "Valor", "Courage", "Fear", "Terror",
    "Horror", "Dread", "Panic", "Rage", "Anger", "Fury", "Wrath", "Hate", "Love", "Peace",
    "War", "Battle", "Combat", "Fight", "Conflict", "Struggle", "Victory", "Triumph", "Defeat", "Loss",
    "Speed", "Velocity", "Momentum", "Pace", "Tempo", "Rhythm", "Beat", "Pulse", "Sound", "Noise",
    "Silence", "Quiet", "Light", "Dark", "Bright", "Dim", "Glow", "Shine", "Spark", "Flash",
    "Blaze", "Fire", "Flame", "Heat", "Cold", "Warm", "Hot", "Cool", "Chill", "Freeze",
    "Hard", "Soft", "Rough", "Smooth", "Sharp", "Dull", "Heavy", "Light", "Big", "Small",
    "Fast", "Slow", "Quick", "Swift", "Rapid", "Sudden", "Steady", "Stable", "Solid", "Liquid",
    "Gas", "Plasma", "Magic", "Mystic", "Arcane", "Divine", "Holy", "Unholy", "Evil", "Good",
    
    # Colors & Materials
    "Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Violet", "Indigo", "Black", "White",
    "Gray", "Grey", "Brown", "Pink", "Magenta", "Cyan", "Teal", "Turquoise", "Aqua", "Azure",
    "Gold", "Silver", "Bronze", "Copper", "Iron", "Steel", "Metal", "Chrome", "Nickel", "Zinc",
    "Tin", "Lead", "Mercury", "Platinum", "Titanium", "Diamond", "Ruby", "Emerald", "Sapphire", "Topaz",
    "Opal", "Pearl", "Jade", "Amber", "Coral", "Quartz", "Crystal", "Glass", "Stone", "Gem",
    
    # Society
    "United", "City", "Town", "Village", "Nation", "State", "Republic", "Empire", "Kingdom", "Union",
    "Alliance", "Coalition", "League", "Guild", "Clan", "Tribe", "Squad", "Team", "Crew", "Gang",
    "Mob", "Horde", "Swarm", "Pack", "Flock", "Herd", "School", "Group", "Band", "Club",
    "Society", "Association", "Organization", "Foundation", "Institute", "Academy", "College", "University", "School",
    "Hospital", "Clinic", "Center", "Station", "Base", "Post", "Fort", "Castle", "Palace", "Tower"
]

TURKEY_DATA = {
    1: {"name": "Antalya", "districts": ["Muratpasa", "Kepez", "Konyaalti", "Lara", "Alanya", "Manavgat", "Kemer", "Kas", "Belek", "Side", "Dosemealti", "Aksu", "Finike", "Kumluca", "Serik", "Demre", "Gazipasa", "Korkuteli", "Elmali", "Akseki"]},
    2: {"name": "Istanbul", "districts": ["Kadikoy", "Besiktas", "Sisli", "Uskudar", "Beyoglu", "Fatih", "Bakirkoy", "Maltepe", "Pendik", "Kartal", "Sariyer", "Beykoz", "Atasehir", "Umraniye", "Cekmekoy", "Tuzla", "Zeytinburnu", "Eyup", "Gaziosmanpasa", "Esenler"]},
    3: {"name": "Ankara", "districts": ["Cankaya", "Kecioren", "Yenimahalle", "Mamak", "Etimesgut", "Golbasi", "Altindag", "Sincan", "Pursaklar", "Cubuk", "Polatli", "Beypazari", "Kazan", "Elmadag", "Akyurt", "Ayas", "Bala", "Haymana", "Nallihan", "Kizilcahamam"]},
    4: {"name": "Izmir", "districts": ["Karsiyaka", "Konak", "Bornova", "Buca", "Cesme", "Alacati", "Urla", "Balcova", "Gaziemir", "Cigli", "Menemen", "Aliaga", "Foca", "Dikili", "Bergama", "Tire", "Odemis", "Torbali", "Selcuk", "Seferihisar"]},
    5: {"name": "Bursa", "districts": ["Nilufer", "Osmangazi", "Yildirim", "Mudanya", "Gemlik", "Inegol", "Iznik", "Orhangazi", "Karacabey", "Mustafakemalpasa", "Gursu", "Kestel", "Yenisehir", "Orhaneli", "Keles", "Buyukorhan", "Harmancik"]},
    6: {"name": "Adana", "districts": ["Seyhan", "Cukurova", "Yuregir", "Saricam", "Ceyhan", "Kozan", "Imamoglu", "Karatas", "Pozanti", "Yumurtalik", "Tufanbeyli", "Feke", "Saimbeyli", "Aladag", "Karaisali"]},
}