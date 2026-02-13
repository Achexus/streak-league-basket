import time
import sys
import random
from datetime import datetime, date

# --- MODÜLER İMPORTLAR ---
from core import controls
from models import Player
from models.league import LeagueManager
from systems import match_engine, loops  # loops eklendi
import ui

def create_game():
    ui.play_intro_animation()
    ui.clear_screen()
    ui.print_header()
    
    print("📂 Loading World Database...")
    try:
        lm = LeagueManager()
    except FileNotFoundError:
        print(f"\n{ui.Style.RED}❌ ERROR: Season data missing!{ui.Style.END}")
        print(f"   Please run 'python setup_season.py' first.")
        sys.exit()
    
    time.sleep(0.5)
    ui.clear_screen()
    ui.print_header()

    name = ui.get_safe_input("   Name: ", str) or "Rookie"
    number = ui.get_safe_input("   Jersey #: ", str) or "10"
    pos = ui.select_position_view()
    city_code = ui.select_city_view()
    
    # Ligi Bul
    target_league = lm.get_league(f"CITY_{city_code}")
    if not target_league: target_league = lm.get_league("CITY_1")

    print(f"\n⚙️  Scouting teams in {target_league.name}...")
    time.sleep(1)
    
    # Oyuncu Oluştur
    player = Player(name, number, pos)
    player.team_obj = random.choice(target_league.teams)
    player.league_id = target_league.id
    
    ui.clear_screen()
    ui.print_header()
    print(f"\n✍️  CONTRACT SIGNED WITH {ui.Style.BOLD}{player.team_obj.name}{ui.Style.END}")
    time.sleep(1)
    
    # Hızlı Başlangıç İçin Hayalleri Otomatik Ata (İstersen input'a çevirebilirsin)
    player.stats.set_dreams("MVP", "Champion", "Legend")
    
    return player, lm

def main():
    player, league_manager = create_game()

    while True:
        # Oyuncunun ligini güncelle (Hafta ilerlemesi için önemli)
        current_league = league_manager.get_league(player.league_id)
        current_league.current_week = league_manager.current_week 

        ui.main_menu_view(player, current_league)
        choice = ui.get_safe_input("Select >> ", str).upper()
        
        if choice == controls.MENU_MATCH:
            match_engine.play_match(player, league_manager)
            controls.wait_for_enter()
            
        elif choice == controls.MENU_HOME:
            loops.home_cycle(player, current_league)
            
        elif choice == controls.MENU_EVENTS: 
            loops.event_cycle(player)
            
        elif choice == controls.MENU_PROFILE:
            ui.profile_view(player)
            
        elif choice == controls.MENU_LEAGUE:
            while True:
                ui.league_standings_view(current_league)
                c = ui.get_safe_input(">> ", str).upper()
                if c == controls.KEY_BACK: break
                elif c == controls.KEY_PLAY:
                    match_engine.play_match(player, league_manager)
                    controls.wait_for_enter()

        elif choice == controls.MENU_END_DAY:
            print("\n💤 Sleeping & Recovering...")
            time.sleep(1)
            score = player.tasks.reset_for_new_day()
            messages = player.apply_daily_score(score)
            
            print(f"\n📊 DAY RESULT: {score} XP Gained.")
            try: print(f"📅 Date Advanced to: {player.get_date_str()}")
            except: pass
            
            if messages:
                print(f"\n{ui.Style.YELLOW}--- DAILY REPORT ---{ui.Style.END}")
                for msg in messages: print(f"   • {msg}")
            
            controls.wait_for_enter()
            
        elif choice == controls.KEY_QUIT:
            print("👋 See you on the court!")
            break

if __name__ == "__main__":
    main()