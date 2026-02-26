import os
import time
import json

from ui.menus import draw_main_title_screen, draw_dashboard
from ui.style import get_safe_input
from models.player import Player, SAVE_FILE
import setup_season # Otomatik kurulum için modülü içe aktardık

def load_season_data():
    """Veritabanını okur, yoksa otomatik olarak oluşturur."""
    db_path = "data/season_data.json"
    if not os.path.exists(db_path):
        print("\n      [SYSTEM] Initializing league databases for the first time... Please wait.")
        setup_season.generate_database()
        time.sleep(1)
        
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def start_new_journey():
    """Yeni kariyer oluşturur, şehir seçtirir ve takıma atar."""
    print("\n      [SYSTEM] Initializing new career protocol...")
    
    name = input("      >> Enter your player name: ").strip() or "Rookie"
    jersey = input("      >> Enter your jersey number (e.g., 23): ").strip() or "00"
    
    print("\n      [POSITIONS] 1: PG | 2: SG | 3: SF | 4: PF | 5: C")
    pos_choice = get_safe_input("      >> Select your position (1-5): ", input_type=int, min_val=1, max_val=5)
    pos_map = {1: "PG", 2: "SG", 3: "SF", 4: "PF", 5: "C"}
    position = pos_map[pos_choice]
    
    # Veritabanını yükle (Yoksa burada otomatik yaratılacak)
    season_data = load_season_data()
    cities = list(season_data["city_leagues"].keys())
    
    print("\n      [CITY SELECTION] Choose your starting city:")
    for i in range(0, len(cities), 4):
        chunk = cities[i:i+4]
        row_str = "      "
        for j, c in enumerate(chunk):
            idx = i + j + 1
            row_str += f"[{idx:2}] {c:<12} "
        print(row_str)
        
    city_choice = get_safe_input("\n      >> Enter city number (1-16): ", input_type=int, min_val=1, max_val=16)
    selected_city = cities[city_choice - 1]
    
    # Seçilen şehrin Şehir Liginden (city_leagues) ilk takımı oyuncuya ata
    assigned_team = season_data["city_leagues"][selected_city]["teams"][0]["name"]
        
    player = Player(name, jersey, position, selected_city, assigned_team)
    player.save() 
    
    print(f"\n      [CONTRACT SIGNED] Welcome to {assigned_team}!")
    time.sleep(2)
    return player

def boot_system():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    # Başlangıçta veritabanını garantiye alalım
    load_season_data()

    current_player = None

    while True:
        has_save = os.path.exists(SAVE_FILE)
        draw_main_title_screen(has_save)
        
        choice = get_safe_input("\n      >> SYSTEM INPUT: ", input_type=int, min_val=1, max_val=4)
        
        if choice == 1:
            current_player = start_new_journey()
            break 
            
        elif choice == 2:
            if has_save:
                print("\n      [SYSTEM] Loading saved data...")
                current_player = Player.load() 
                time.sleep(1)
                print(f"      [SUCCESS] {current_player.name} logged in! Team: {current_player.team_name}")
                time.sleep(2)
                break 
            else:
                print("\n      [ERROR] No save file found! Please start a New Journey.")
                time.sleep(1.5)
                
        elif choice == 3:
            print("\n      [SYSTEM] Settings module is under construction...")
            time.sleep(1.5)
            
        elif choice == 4:
            print("\n      [SYSTEM] Terminating session. Goodbye!")
            time.sleep(1)
            exit()
            
    run_game_loop(current_player)

def run_game_loop(player):
    while True:
        draw_dashboard(player)
        choice = get_safe_input("\n      >> WHAT WOULD YOU LIKE TO DO? (1-4): ", input_type=int, min_val=1, max_val=4)

        if choice == 1:
            print("\n      [CATEGORIES] 1: SHOOTING (Work) | 2: DEFENSE (Sports) | 3: PLAYMAKING (Mind)")
            cat_choice = get_safe_input("      >> Select a category (1-3): ", input_type=int, min_val=1, max_val=3)
            cat_map = {1: "SHOOTING", 2: "DEFENSE", 3: "PLAYMAKING"}
            
            task_name = input("      >> Task Name: ").strip()
            if task_name:
                player.daily_tasks.append({"name": task_name, "category": cat_map[cat_choice], "done": False})
                player.save() 
                print("      [SUCCESS] Task added!")
                time.sleep(1)

        elif choice == 2:
            if not player.daily_tasks:
                print("\n      [ERROR] Add a task first!")
                time.sleep(1.5)
                continue

            task_idx = get_safe_input(f"\n      >> Which task did you complete? (1-{len(player.daily_tasks)}): ", input_type=int, min_val=1, max_val=len(player.daily_tasks))
            selected_task = player.daily_tasks[task_idx - 1]

            if not selected_task["done"]:
                selected_task["done"] = True
                cat = selected_task["category"]
                player.stats[cat] += 1
                player.save()
                print(f"\n      [CONGRATS!] {cat} attribute increased by +1!")
            else:
                print("\n      [INFO] Already completed.")
            time.sleep(1.5)

        elif choice == 3:
            print("\n      [SYSTEM] End Day mechanics under construction.")
            time.sleep(1.5)

        elif choice == 4:
            player.save()
            print("\n      [SYSTEM] Returning to Main Menu...")
            time.sleep(1)
            boot_system() 

if __name__ == "__main__":
    boot_system()