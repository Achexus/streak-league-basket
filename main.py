# main.py
import time
from datetime import datetime, date
from player import Player
from league import League
from tasks import AgendaItem
import views
import mechanics
import controls # <--- YENİ EKLENDİ

def create_game():
    views.play_intro_animation()
    views.clear_screen()
    views.print_header()
    
    name = views.get_safe_input("   Name: ", str) or "Pro Player"
    number = views.get_safe_input("   Jersey #: ", str) or "10"
    pos = views.select_position_view()
    city_code = views.select_city_view()
    
    print("\n⚙️  BUILDING CAREER MODE...")
    league = League(city_code)
    time.sleep(0.5)
    
    player = Player(name, number, pos)
    player.assign_team(league)
    
    views.clear_screen()
    views.print_header()
    print("\n✨ DEFINE YOUR LEGACY (3 MAIN DREAMS) ✨")
    print("For each dream, you must define at least 1 daily habit.\n")
    
    dreams = []
    
    d1 = input("   1. MAIN DREAM (e.g. Buy a House): ") or "Become MVP"
    t1 = input(f"      -> Linked Habit for '{d1}': ") or "Train Hard"
    player.tasks.add_habit(t1, controls.DIFF_MEDIUM)
    dreams.append(d1)
    print("-" * 40)
    
    d2 = input("   2. MAIN DREAM: ") or "Win Championship"
    t2 = input(f"      -> Linked Habit for '{d2}': ") or "Watch Film"
    player.tasks.add_habit(t2, controls.DIFF_MEDIUM)
    dreams.append(d2)
    print("-" * 40)
    
    d3 = input("   3. MAIN DREAM: ") or "Be Rich"
    t3 = input(f"      -> Linked Habit for '{d3}': ") or "Read Books"
    player.tasks.add_habit(t3, controls.DIFF_MEDIUM)
    dreams.append(d3)
    
    player.stats.set_dreams(dreams[0], dreams[1], dreams[2])
    
    print(f"\n✅ WELCOME TO {player.team_obj.name}!")
    time.sleep(2)
    return player, league

def habits_loop(player):
    while True:
        views.habits_view(player)
        c = views.get_safe_input(">> ", str).upper()
        if c == controls.KEY_BACK: break
        elif c == controls.KEY_ADD: 
            n = input("Habit Name: ")
            d = views.get_safe_input("Diff (E/M/H): ", str, valid_options=[controls.DIFF_EASY, controls.DIFF_MEDIUM, controls.DIFF_HARD])
            player.tasks.add_habit(n, d)
        elif c.isdigit(): player.tasks.toggle_habit(int(c)-1)

def tasks_loop(player):
    while True:
        views.tasks_view(player)
        c = views.get_safe_input(">> ", str).upper()
        if c == controls.KEY_BACK: break
        elif c == controls.KEY_ADD: 
            n = input("Task Name: ")
            d = views.get_safe_input("Diff (E/M/H): ", str, valid_options=[controls.DIFF_EASY, controls.DIFF_MEDIUM, controls.DIFF_HARD])
            player.tasks.add_task(n, d)
        elif c == controls.KEY_DELETE: 
            idx = views.get_safe_input("Task #: ", int)
            try: player.tasks.remove_task(idx-1)
            except: pass
        elif c == controls.KEY_IMPORT: player.import_agenda_to_task()
        elif c.isdigit(): player.tasks.toggle_task(int(c)-1)

def calendar_loop(player):
    while True:
        views.agenda_view(player)
        c = views.get_safe_input(">> ", str).upper()
        if c == controls.KEY_BACK: break
        elif c == controls.KEY_NEW:
            try:
                day = views.get_safe_input("Day: ", int, min_val=1, max_val=31)
                dt = datetime(date.today().year, date.today().month, day)
                player.tasks.agenda.append(AgendaItem(dt, input("Note: ")))
            except: pass

def home_cycle(player):
    while True:
        views.home_hub_view(player)
        c = views.get_safe_input(">> ", str).upper()
        if c == controls.KEY_BACK: break
        elif c == '1': habits_loop(player)
        elif c == '2': tasks_loop(player)
        elif c == '3': calendar_loop(player)

def main():
    player, league = create_game()

    while True:
        views.main_menu_view(player)
        choice = views.get_safe_input("Select >> ", str).upper()
        
        if choice == controls.MENU_MATCH:
            mechanics.play_match(player, league)
            controls.wait_for_enter()
        elif choice == controls.MENU_HOME:
            home_cycle(player)
        elif choice == controls.MENU_PROFILE:
            views.profile_view(player)
        elif choice == controls.MENU_LEAGUE:
            while True:
                views.league_standings_view(league)
                c = views.get_safe_input(">> ", str).upper()
                if c == controls.KEY_BACK: break
                elif c == controls.KEY_PLAY:
                    mechanics.play_match(player, league)
                    controls.wait_for_enter()

        elif choice == controls.MENU_END_DAY:
            print("\n💤 Sleeping & Simulating...")
            time.sleep(1)
            score = player.tasks.reset_for_new_day()
            
            event_msg = player.apply_daily_score(score)
            
            print(f"📊 DAY RESULT: {score} XP.")
            if event_msg:
                print(f"\n📅 {views.Style.YELLOW}MONTHLY EVENT TRIGGERED!{views.Style.END}")
                print(f"   {event_msg}")
                controls.wait_for_enter()
            
            if score < 0: print("⚠️  Lost momentum.")
            else: print("✅  Progress saved.")
            
            controls.wait_for_enter()
        elif choice == controls.KEY_QUIT:
            break

if __name__ == "__main__":
    main()