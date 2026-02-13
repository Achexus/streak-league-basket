import time
import calendar
import re
from datetime import date
from core import controls
from core.config import TURKEY_DATA
from .style import *
from .event_ui import draw_active_event_panel, draw_simple_card

# --- YARDIMCI: RENK KODU TEMİZLEYİCİ (KAYMAYI ÖNLER) ---
def get_visible_length(text):
    """Metnin içindeki renk kodlarını saymadan gerçek uzunluğunu bulur"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', text))

def center_in_box(text, width):
    """Metni verilen genişlikteki kutuya, renk kodlarını dikkate alarak ortalar"""
    vis_len = get_visible_length(text)
    if vis_len >= width:
        return text 
    padding = width - vis_len
    pad_left = padding // 2
    pad_right = padding - pad_left
    return " " * pad_left + text + " " * pad_right

def play_intro_animation():
    clear_screen()
    print("\n" * 10)
    print_centered(f"{Style.YELLOW}LOADING SEASON EVENTS...{Style.END}")
    time.sleep(1)

def draw_xp_bar(current, total=1000, length=15):
    if total == 0: total = 1
    percent = current / total
    filled = int(length * percent)
    bar = "█" * filled + "░" * (length - filled)
    return f"{Style.GREEN}{bar}{Style.END}"

def main_menu_view(player, league):
    clear_screen()
    print_header()
    
    # --- ÜST BİLGİ ŞERİDİ ---
    try: date_str = player.get_date_str().upper()
    except: date_str = "PRE-SEASON"
    team_rec = player.team_obj.get_record()
    week_str = f"WEEK {league.current_week}"
    
    info_strip = f"📅 {date_str}   |   🛡️ {player.team_obj.name.upper()} ({team_rec})   |   🏆 {week_str}"
    print_centered(f"{Style.YELLOW}{info_strip}{Style.END}")
    print_centered(f"{Style.DARKCYAN}" + "─"*70 + f"{Style.END}")
    
    # --- ORTA BÖLÜM (HERO SECTION) ---
    ovr_str = f"{Style.YELLOW}{player.stats.get_overall()}{Style.END}"
    lvl_str = f"{Style.CYAN}{player.level}{Style.END}"
    ppg = round(player.career_pts / player.games_played, 1) if player.games_played > 0 else 0.0
    xp_bar = draw_xp_bar(player.total_lifetime_xp % 1000, 1000, 15)
    
    next_match = league.get_my_match(player.team_obj)
    if next_match:
        if next_match.played:
            match_status = f"{Style.RED}PLAYED{Style.END}"
            opp_text = "WAITING..."
        else:
            match_status = f"{Style.GREEN}UPCOMING{Style.END}"
            opp_obj = next_match.away_team if next_match.home_team == player.team_obj else next_match.home_team
            opp_text = f"vs {opp_obj.name}"
            # İsim uzunsa kısalt
            if len(opp_text) > 18: opp_text = opp_text[:16] + ".."
            
            if opp_obj.offense > 85: opp_text = f"{Style.RED}{opp_text}{Style.END}"
            else: opp_text = f"{Style.BOLD}{opp_text}{Style.END}"
    else:
        match_status = "BYE WEEK"
        opp_text = "NO MATCH"

    # KUTULARI ÇİZ (KAYMA DÜZELTİLDİ)
    W = 26 # Kutu iç genişliği
    
    # Satır 1
    t1 = center_in_box(f"{Style.CYAN}PLAYER HUB{Style.END}", W)
    t2 = center_in_box(f"{Style.PURPLE}NEXT BATTLE{Style.END}", W)
    
    # Satır 2
    name_d = center_in_box(f"{Style.BOLD}{player.name[:18]}{Style.END}", W)
    stat_d = center_in_box(match_status, W)
    
    # Satır 3
    ovr_d = center_in_box(f"OVR: {ovr_str}  |  LVL: {lvl_str}", W)
    opp_d = center_in_box(opp_text, W)
    
    # Satır 4
    xp_d = center_in_box(f"XP: {xp_bar}", W)
    emp_d = center_in_box("", W)
    
    # Satır 5
    avg_d = center_in_box(f"AVG: {ppg} PPG", W)
    msg_d = center_in_box("Win to gain XP", W)
    
    gap = "       "
    print("      " + f"{Style.CYAN}╔{'═'*W}╗{Style.END}" + gap + f"{Style.PURPLE}╔{'═'*W}╗{Style.END}")
    print("      " + f"║{t1}║" + gap + f"║{t2}║")
    print("      " + f"║{'─'*W}║" + gap + f"║{'─'*W}║")
    print("      " + f"║{name_d}║" + gap + f"║{stat_d}║")
    print("      " + f"║{ovr_d}║" + gap + f"║{opp_d}║")
    print("      " + f"║{xp_d}║" + gap + f"║{emp_d}║")
    print("      " + f"║{avg_d}║" + gap + f"║{msg_d}║")
    print("      " + f"{Style.CYAN}╚{'═'*W}╝{Style.END}" + gap + f"{Style.PURPLE}╚{'═'*W}╝{Style.END}")

    print("\n")
    
    # --- ALT BÖLÜM: MENÜLER ---
    print_centered(f"{Style.UNDERLINE}MAIN ACTIONS{Style.END}")
    
    m1 = f"[{controls.MENU_MATCH}] 🏀 PLAY MATCH"
    m2 = f"[{controls.MENU_HOME}] 🏠 HOME HUB"
    m3 = f"[{controls.MENU_EVENTS}] 🌟 EVENT CENTER"
    
    m4 = f"[{controls.MENU_LEAGUE}] 🏆 LEAGUE"
    m5 = f"[{controls.MENU_PROFILE}] 📊 PROFILE"
    m6 = f"[{controls.MENU_END_DAY}] 💤 END DAY"
    
    m7 = f"[{controls.KEY_QUIT}] 🚪 QUIT GAME"
    
    row1 = f" {m1:<25} {m2:<25} {m3:<25}"
    row2 = f" {m4:<25} {m5:<25} {m6:<25}"
    
    print_centered(row1)
    print_centered(row2)
    print("\n")
    print_centered(m7)
    print("\n" + f"{Style.DARKCYAN}" + "─"*70 + f"{Style.END}")

def home_hub_view(player, league):
    clear_screen()
    print_header()
    print_section_header("🏠  H O M E   H U B", width=40)
    try: date_str = player.get_date_str()
    except: date_str = "Day " + str(player.days_passed)
    print_centered(f"📅 DATE: {Style.CYAN}{date_str}{Style.END}")
    print("\n")
    print_centered("--- 🔁 DAILY HABITS ---")
    if not player.tasks.habits:
        print_centered("(No habits set)")
    else:
        for i, h in enumerate(player.tasks.habits):
            icon = "✅" if h.done else "⬜"
            color = Style.GREEN if h.done else Style.END
            print(" " * 15 + f"{i+1}. {icon} {color}{h.task:<25}{Style.END} [{h.diff}] {h.xp} XP")
    print("\n" + "─" * 40)
    current_score = player.tasks.calculate_daily_score()
    score_color = Style.GREEN if current_score > 0 else Style.RED
    print_centered(f"DAILY XP PENDING: {score_color}{current_score}{Style.END}")
    print("\n" + " "*10 + f"{Style.YELLOW}[A]{Style.END} Add Habit  |  {Style.YELLOW}[1-9]{Style.END} Toggle Habit")
    print(" "*10 + f"{Style.YELLOW}[2]{Style.END} To-Do List  |  {Style.YELLOW}[3]{Style.END} Calendar")
    print(" "*10 + f"{Style.RED}[{controls.KEY_BACK}]{Style.END} Back")

def event_center_view(player):
    clear_screen()
    print_header()
    draw_active_event_panel(player.events.current_event)
    print("\n" + "─" * 40)
    if player.events.current_event and not player.events.current_event.is_locked:
        print_centered(f"{Style.PURPLE}--- 🎯 EVENT OBJECTIVES ---{Style.END}")
        for i, t in enumerate(player.events.current_event.tasks):
            icon = "✅" if t['done'] else "⭕"
            color = Style.PURPLE if t['done'] else Style.END
            val_str = f"(+{t['val']} Progress)"
            print(" " * 12 + f"E{i+1}. {icon} {color}{t['task']}{Style.END} {val_str}")
    else:
        print_centered("(No active tasks available)")
    print("\n" + "─" * 40)
    print_centered(f"STREAK: {player.events.perfect_streak} Days 🔥")
    print("\n" + " "*15 + f"{Style.PURPLE}[E1-E3]{Style.END} Complete Objective")
    print(" "*15 + f"{Style.RED}[{controls.KEY_BACK}]{Style.END} Back to Main Menu")

def tasks_view(player):
    clear_screen()
    print_header()
    print_section_header("📝  ONE-OFF TASKS", width=40)
    alerts = player.check_agenda_alerts()
    if alerts:
        print_centered(f"{Style.RED}🔔 AGENDA ALERT! PRESS 'I' TO IMPORT{Style.END}")
        for alert in alerts: print_centered(f"• {alert}")
    if not player.tasks.daily_tasks: print_centered("(No tasks for today)")
    else:
        for i, t in enumerate(player.tasks.daily_tasks):
            icon = "✅" if t.done else "⬜"
            color = Style.GREEN if t.done else Style.END
            print(" " * 15 + f"{i+1}. {icon} {color}{t.task:<25}{Style.END} [{t.diff}] {t.xp} XP")
    print("\n" + "━"*80)
    print(f" [A] Add | [S] Del | [I] Import | [Num] Toggle | [B] Back")

def agenda_view(player):
    clear_screen()
    print_header()
    print_section_header("📅  CALENDAR", width=40)
    cal = calendar.month(date.today().year, date.today().month)
    for line in cal.split('\n'): print_centered(line)
    print_centered("─" * 40)
    upcoming = [x for x in player.tasks.agenda if x.event_date.date() >= date.today()]
    upcoming.sort(key=lambda x: x.event_date)
    if not upcoming: print_centered("No upcoming events.")
    else:
        for item in upcoming:
            d_str = item.event_date.strftime('%d %b')
            print(" " * 20 + f"📅 {Style.CYAN}{d_str}{Style.END} : {item.content}")
    print("\n" + "━" * 80)
    print(f" [{controls.KEY_NEW}] New Event | [{controls.KEY_BACK}] Back")

def profile_view(player):
    clear_screen()
    print_header()
    print("\n")
    draw_simple_card(player)
    print("\n")
    print_centered(f"{Style.UNDERLINE}COLLECTED EVENT CARDS{Style.END}")
    if not player.events.collected_cards:
        print_centered("(No event cards earned yet)")
    else:
        for card in player.events.collected_cards:
            c = Style.YELLOW if card.rarity == "LEGENDARY" else Style.END
            print_centered(f"{c}★ {card.name} ({card.date_earned}){Style.END}")
    print("\n")
    print_centered(f"{Style.YELLOW}--- 3 MAIN DREAMS ---{Style.END}")
    for i, d in enumerate(player.stats.dreams): print_centered(f"{i+1}. {d}")
    print("\n")
    print_centered("[E] Edit Dreams | [Enter] Back")
    choice = controls.get_upper_input("\n" + " "*35 + ">> ")
    if choice == 'E':
        new_dreams = []
        for i in range(3):
            val = input(f"   New Dream {i+1}: ") or player.stats.dreams[i]
            new_dreams.append(val)
        player.stats.dreams = new_dreams

def select_city_view():
    clear_screen()
    print_header()
    print_section_header("🏙️  SELECT CITY", width=40)
    items = list(TURKEY_DATA.items())
    for i in range(0, len(items), 3):
        row = items[i:i+3]
        line = ""
        for code, data in row: line += f"[{code}] {data['name']:<15}"
        print_centered(line)
    return get_safe_input("\n" + " "*30 + "Enter Code: ", input_type=int, min_val=1, max_val=len(items))

def select_position_view():
    print("\n")
    print_centered("🏀 SELECT POSITION")
    print_centered("1. PG - Point Guard")
    print_centered("2. SG - Shooting Guard")
    print_centered("3. SF - Small Forward")
    print_centered("4. PF - Power Forward")
    print_centered("5. C  - Center")
    m = {1:"PG", 2:"SG", 3:"SF", 4:"PF", 5:"C"}
    choice = get_safe_input("\n" + " "*30 + "Select: ", input_type=int, min_val=1, max_val=5)
    return m[choice]