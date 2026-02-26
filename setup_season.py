import json
import os

# 16 Şehir ve İlçe Havuzları
CITY_DISTRICTS = {
    "Istanbul": ["Kadikoy", "Besiktas", "Sisli", "Uskudar", "Bakirkoy", "Maltepe", "Sariyer", "Beyoglu"],
    "Ankara": ["Cankaya", "Kecioren", "Yenimahalle", "Mamak", "Etimesgut", "Sincan", "Altindag", "Golbasi"],
    "Izmir": ["Karsiyaka", "Bornova", "Buca", "Konak", "Balcova", "Cigli", "Gaziemir", "Urla"],
    "Bursa": ["Nilufer", "Osmangazi", "Yildirim", "Mudanya", "Gemlik", "Inegol", "Kestel", "Gursu"],
    "Antalya": ["Muratpasa", "Konyaalti", "Kepez", "Alanya", "Manavgat", "Kemer", "Kas", "Serik"],
    "Konya": ["Selcuklu", "Meram", "Karatay", "Eregli", "Aksehir", "Beysehir", "Cumra", "Seydisehir"],
    "Adana": ["Cukurova", "Seyhan", "Yuregir", "Saricam", "Ceyhan", "Kozan", "Imamoglu", "Karatas"],
    "Sanliurfa": ["Haliliye", "Eyyubiye", "Karakopru", "Siverek", "Viransehir", "Birecik", "Suruc", "Ceylanpinar"],
    "Gaziantep": ["Sahinbey", "Sehitkamil", "Nizip", "Islahiye", "Nurdagi", "Araban", "Oguzeli", "Yavuzeli"],
    "Kocaeli": ["Izmit", "Gebze", "Darica", "Golcuk", "Korfez", "Derince", "Kartepe", "Cayirova"],
    "Mersin": ["Yenisehir", "Mezitli", "Toroslar", "Akdeniz", "Tarsus", "Erdemli", "Silifke", "Anamur"],
    "Diyarbakir": ["Kayapinar", "Yenisehir", "Baglar", "Sur", "Ergani", "Bismil", "Silvan", "Cermik"],
    "Hatay": ["Antakya", "Defne", "Iskenderun", "Arsuz", "Dortyol", "Samandag", "Kirikhan", "Reyhanli"],
    "Kayseri": ["Melikgazi", "Kocasinan", "Talas", "Develi", "Yahyali", "Bunyan", "Incesu", "Tomarza"],
    "Manisa": ["Yunusemre", "Sehzadeler", "Akhisar", "Salihli", "Turgutlu", "Soma", "Alasehir", "Kula"],
    "Samsun": ["Atakum", "Ilkadim", "Canik", "Bafra", "Carsamba", "Tekkekoy", "Vezirkopru", "Terme"]
}

# 600+ Benzersiz Tek Kelimelik Takım Sıfatı (Suffix)
# Program bunları okuyacak, mükerrerleri silecek ve bize tam 544 tane eşsiz isim verecek.
RAW_WORDS = """
United City Athletic Sporting Elite Legends Stars Meteors Comets Asteroids Planets Moons Suns Galaxies Nebulas Quasars Pulsars Blackholes Supernovas Novas Eclipses Auroras Halos Rainbows Clouds Storms Thunders Lightnings Raindrops Snowflakes Blizzards Avalanches Glaciers Icebergs Frosts Freezes Chills Winds Breezes Gusts Gales Hurricanes Tornadoes Cyclones Typhoons Monsoons Tsunamis Waves Tides Currents Whirlpools Eddies Rapids Falls Springs Geysers Volcanoes Eruptions Magmas Lavas Ashes Embers Flames Fires Infernos Blazes Sparks Flashes Beams Rays Shadows Shades Ghosts Spirits Phantoms Specters Wraiths Banshees Demons Devils Fiends Imps Angels Cherubs Seraphs Archangels Gods Deities Immortals Divines Celestials Eternals Cosmos Universes Dimensions Realms Worlds Globes Spheres Orbs Rings Disks Wheels Gears Cogs Pistons Engines Motors Machines Devices Tools Weapons Swords Blades Daggers Knives Axes Hammers Maces Clubs Spears Lances Javelins Pikes Halberds Bows Arrows Darts Bolts Slings Shields Armors Helmets Gauntlets Boots Crowns Tiaras Jewels Gems Diamonds Rubies Sapphires Emeralds Amethysts Topazes Opals Pearls Golds Silvers Bronzes Coppers Irons Steels Alloys Metals Minerals Rocks Stones Pebbles Boulders Mountains Hills Peaks Valleys Canyons Gorges Chasms Abysses Caves Caverns Tunnels Mines Shafts Pits Holes Craters Deserts Dunes Sands Dusts Muds Clays Soils Earths Lands Continents Islands Peninsulas Capes Coasts Shores Beaches Banks Rivers Streams Creeks Brooks Lakes Ponds Pools Seas Oceans Gulfs Bays Straits Channels Canals Sounds Echoes Whispers Shouts Roars Howls Growls Barks Bites Strikes Punches Kicks Slaps Chops Blocks Dodges Jumps Leaps Bounds Dashes Sprints Runs Walks Crawls Climbs Swims Dives Flights Soars Glides Drops Crashes Smashes Breaks Cracks Snaps Pops Bangs Booms Clashes Clangs Rings Chimes Bells Gongs Horns Drums Flutes Harps Lutes Lyres Guitars Pianos Organs Violins Cellos Basses Lions Tigers Bears Hawks Eagles Falcons Wolves Foxes Sharks Dolphins Panthers Jaguars Leopards Pumas Cougars Wildcats Bobcats Lynx Cheetahs Rhinos Hippos Elephants Giraffes Zebras Camels Llamas Alpacas Moose Elks Deers Bucks Antelopes Gazelles Mustangs Broncos Colts Stallions Bulls Cows Calves Rams Sheep Goats Boars Pigs Hounds Dogs Pups Cats Kittens Rats Mice Bats Vampires Werewolves Zombies Ghouls Goblins Orcs Trolls Ogres Giants Titans Cyclopes Dragons Wyverns Hydras Basilisks Phoenixes Griffins Gargoyles Sphinxes Minotaurs Centaurs Pegasi Unicorns Sirens Mermaids Krakens Leviathans Serpents Snakes Vipers Pythons Cobras Mambas Boas Adders Rattlers Spiders Scorpions Ants Bees Wasps Hornets Yellowjackets Beetles Mantises Crickets Locusts Grasshoppers Flies Mosquitoes Moths Butterflies Caterpillars Worms Slugs Snails Crabs Lobsters Shrimp Squids Octopuses Jellyfish Starfish Urchins Sponges Corals Fish Piranhas Barracudas Marlins Swordfish Sailfish Tunas Salmons Trouts Bass Carps Catfish Eels Rays Skates Flounders Halibuts Cods Haddocks Herrings Sardines Anchovies Mackerels Whales Orcas Narwhals Belugas Porpoises Seals Walruses Penguins Pelicans Seagulls Albatrosses Cranes Herons Flamingos Storks Swans Geese Ducks Mallards Loons Grebes Puffins Owls Ospreys Kites Harriers Vultures Condors Buzzards Ravens Crows Magpies Jays Robins Bluebirds Cardinals Finches Sparrows Swallows Swifts Hummingbirds Woodpeckers Flickers Toucans Parrots Macaws Cockatoos Ostriches Emus Kiwis Cassowaries Moas Dodos Dinosaurs Raptors Triceratops Mammoths Mastodons Sabertooths Kings Queens Princes Princesses Dukes Duchesses Lords Ladies Knights Squires Pages Barons Counts Earls Viscounts Emperors Empresses Tsars Pharaohs Sultans Caliphs Rajas Maharajas Shoguns Samurais Ninjas Ronins Assassins Thieves Rogues Bandits Pirates Corsairs Buccaneers Smugglers Vikings Raiders Pillagers Marauders Barbarians Berserkers Warriors Soldiers Fighters Brawlers Boxers Wrestlers Gladiators Champions Heroes Villains Mutants Cyborgs Robots Androids Clones Aliens Astronauts Cosmonauts Pilots Drivers Racers Riders Surfers Skaters Skiers Snowboarders Climbers Hikers Swimmers Sailors Captains Commanders Admirals Generals Colonels Majors Lieutenants Sergeants Corporals Privates Snipers Gunners Cavalry Infantry Medics Engineers Spies Agents Detectives Inspectors Cops Police Sheriffs Deputies Marshals Rangers Wardens Guards Sentinels Watchmen Protectors Defenders Guardians Keepers Masters Teachers Mentors Gurus Sages Wizards Sorcerers Witches Warlocks Mages Necromancers Alchemists Enchanters Illusionists Seers Prophets Oracles Priests Monks Friars Nuns Clerics Paladins Templars Crusaders Inquisitors Heretics Cultists Zealots Fanatics Rebels Revolutionaries Patriots Citizens Civilians Locals Natives Nomads Wanderers Travelers Explorers Adventurers Pioneers Settlers Colonists Founders Creators Builders Makers Smiths Forgers Miners Diggers Farmers Planters Harvesters Reapers Hunters Trackers Trappers Fishers Anglers
"""

def get_unique_suffixes():
    """Kelimeleri ayırır ve mükerrerleri temizleyerek eşsiz bir liste döndürür."""
    # dict.fromkeys ile sırayı bozmadan mükerrerleri siliyoruz
    unique_list = list(dict.fromkeys(RAW_WORDS.split()))
    if len(unique_list) < 544:
        raise ValueError(f"[HATA] 544 benzersiz isim gerekli, sadece {len(unique_list)} bulundu!")
    return unique_list

def generate_database():
    """Gelişmiş Veritabanını otomatik olarak oluşturur."""
    suffixes = get_unique_suffixes()
    
    database = {
        "national_league": {"name": "Turkish Super League", "teams": []},
        "city_leagues": {}
    }
    
    suffix_index = 0
    
    for city, districts in CITY_DISTRICTS.items():
        city_league_name = f"{city} Metropolitan League"
        database["city_leagues"][city] = {"name": city_league_name, "teams": []}
        
        for i in range(34):
            # Asla tekrar etmeyen sıfatı al
            suffix = suffixes[suffix_index]
            suffix_index += 1
            
            # Takımın bağlı olduğu ilçeyi belirle (Round-Robin ile eşit dağıtım)
            district = districts[i % len(districts)]
            
            # Takımın her iki lig için de geçerli isimlerini hazırla
            national_name = f"{city} {suffix}"
            local_name = f"{district} {suffix}"
            
            # Dinamik Takım Kimliği (Blueprint)
            team_data = {
                "name": national_name if i < 2 else local_name, # O anki aktif isim
                "national_name": national_name,                 # Terfi ederse alacağı isim (Örn: Antalya Lions)
                "local_name": local_name,                       # Küme düşerse alacağı isim (Örn: Kepez Lions)
                "suffix": suffix,                               # Takımın değişmez hüviyeti (Örn: Lions)
                "city": city,
                "district": district if i >= 2 else "Center",
                "power_rating": 50
            }
            
            if i < 2:
                # İlk 2 takım Ulusal Lige atanır
                database["national_league"]["teams"].append(team_data)
            else:
                # Kalan 32 takım Şehir Ligine atanır
                database["city_leagues"][city]["teams"].append(team_data)
                
    os.makedirs("data", exist_ok=True)
    with open("data/season_data.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4)