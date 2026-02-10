import time
from datetime import datetime, date
from player import Player
from league import League
from tasks import AgendaItem
import views
import mechanics

def get_difficulty():
    while True:
        d = input("Diff (E/M/H): ").upper()
        if d in ['E','M','H']: return d

def create_game():
    views.clear_screen()
    views.print_header()
    
    name = input("Player Name: ") or "Rookie"
    number = input("Jersey #: ") or "23"
    pos = views.select_position_view()
    
    city_code = views.select_city_view()
    
    print("\n⚙️  GENERATING LEAGUE...")
    league = League(city_code)
    time.sleep(1)
    
    player = Player(name, number, pos)
    player.assign_team(league)
    
    print("\n✨ CHARACTER FOUNDATION ✨")
    print("Enter 5 Dreams (Determines Starting Offense):")
    for i in range(5):
        d = input(f"   Dream {i+1}: ") or "Be Great"
        player.stats.add_dream(d)
        
    print("\nEnter 10 Improvements (Determines Starting Defense):")
    for i in range(10):
        imp = input(f"   Improvement {i+1}: ") or "Work Hard"
        player.stats.add_improvement(imp)
        
    print(f"\n✅ WELCOME TO {player.team_obj.name}!")
    time.sleep(2)
    return player, league

# --- DÖNGÜLER ---
def habits_loop(player):
    while True:
        views.habits_view(player)
        c = input(">> ").upper()
        if c == 'B': break
        elif c == 'A': player.tasks.add_habit(input("Name: "), get_difficulty())
        elif c.isdigit(): player.tasks.toggle_habit(int(c)-1)

def tasks_loop(player):
    while True:
        views.tasks_view(player)
        c = input(">> ").upper()
        if c == 'B': break
        elif c == 'A': player.tasks.add_task(input("Name: "), get_difficulty())
        elif c == 'S': 
            try: player.tasks.remove_task(int(input("#: "))-1)
            except: pass
        elif c == 'I': player.import_agenda_to_task()
        elif c.isdigit(): player.tasks.toggle_task(int(c)-1)

def calendar_loop(player):
    while True:
        views.agenda_view(player)
        c = input(">> ").upper()
        if c == 'B': break
        elif c == 'N':
            try:
                # DÜZELTME: Doğru listeye ekleme yapıyoruz
                d = int(input("Day: "))
                dt = datetime(date.today().year, date.today().month, d)
                player.tasks.agenda.append(AgendaItem(dt, input("Note: ")))
            except: pass

def home_cycle(player):
    while True:
        views.home_hub_view(player)
        c = input(">> ").upper()
        if c == 'B': break
        elif c == '1': habits_loop(player)
        elif c == '2': tasks_loop(player)
        elif c == '3': calendar_loop(player)

def main():
    player, league = create_game()

    while True:
        views.main_menu_view(player)
        choice = input("Select >> ").lower()
        
        if choice == '1': # PLAY MATCH
            mechanics.play_match(player, league)
            input("Press Enter...")
        elif choice == '2': # HOME
            home_cycle(player)
        elif choice == '3': # PROFILE
            views.profile_view(player)
        elif choice == '4': # LEAGUE
            while True:
                views.league_standings_view(league)
                if input(">> ").upper() == 'B': break
        elif choice == '5': # END DAY
            print("\n💤 Calculating Daily Score...")
            time.sleep(1)
            score = player.tasks.reset_for_new_day()
            player.apply_daily_score(score)
            print(f"📊 DAY RESULT: {score} Points Applied to Career.")
            if score < 0: print("⚠️  Negative score! You lost potential.")
            else: print("✅  Good job! Potential increased.")
            input("New day starts...")
        elif choice == 'q':
            break

if __name__ == "__main__":
    main()