import os
import time
import calendar
import re
from datetime import date
from config import TURKEY_DATA, STAT_NAMES, EVENT_TYPE_BOSS, EVENT_TYPE_BINGO, EVENT_TYPE_CLIMB
import controls

class Style:
    PURPLE = '\033[95m'; CYAN = '\033[96m'; DARKCYAN = '\033[36m'; BLUE = '\033[94m'
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
    BOLD = '\033[1m'; UNDERLINE = '\033[4m'; END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, width=80):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible_length = len(ansi_escape.sub('', text))
    padding = (width - visible_length) // 2
    print(" " * padding + text)

def print_header():
    print(f"{Style.BOLD}{Style.CYAN}" + "━"*80)
    print_centered(f"S T R E A K   L E A G U E   :   U L T I M A T E   E V E N T S")
    print("━"*80 + f"{Style.END}")

def print_section_header(title, width=60):
    print("\n")
    print_centered(f"{Style.YELLOW}╔" + "═" * width + "╗" + f"{Style.END}")
    print_centered(f"{Style.BOLD}{title}{Style.END}")
    print_centered(f"{Style.YELLOW}╚" + "═" * width + "╝" + f"{Style.END}")

def get_safe_input(prompt_text, input_type=str, valid_options=None, min_val=None, max_val=None):
    while True:
        try:
            user_input = input(f"{prompt_text}")
            if not user_input.strip():
                if input_type == str: return ""
                continue
            if input_type == int:
                val = int(user_input)
                if min_val is not None and val < min_val: continue
                if max_val is not None and val > max_val: continue
                return val
            else:
                val = user_input.upper() if valid_options else user_input
                if valid_options and val not in valid_options: continue
                return val
        except ValueError: pass

def draw_modern_bar(val, total, length=30, color=Style.GREEN):
    if total == 0: percent = 0
    else: percent = val / total
    filled_len = int(length * percent)
    bar = "█" * filled_len + "░" * (length - filled_len)
    percent_num = int(percent * 100)
    return f"{color}{bar} {percent_num}%{Style.END}"

def play_intro_animation():
    clear_screen()
    print("\n" * 10)
    print_centered(f"{Style.YELLOW}LOADING SEASON EVENTS...{Style.END}")
    time.sleep(1)

# --- YENİ: EVENT GÖRSELLEŞTİRME ---
def draw_active_event_panel(event):
    """Aktif etkinliğin durumunu (Boss, Bingo vb.) çizer"""
    if not event:
        print_centered("(No Active Event currently)")
        return

    print("\n")
    print_centered(f"{Style.PURPLE}★ ACTIVE EVENT: {event.name} {event.emoji} ★{Style.END}")
    print_centered(f"{Style.CYAN}{event.desc}{Style.END}")
    print("\n")

    if event.is_locked:
        print_centered(f"{Style.RED}🔒 EVENT LOCKED{Style.END}")
        print_centered(event.lock_reason)
        return

    # OYUN MODUNA GÖRE ÇİZİM
    if event.type == EVENT_TYPE_BOSS:
        # Boss Can Barı
        hp_percent = event.boss_hp / 1000
        hp_len = int(40 * hp_percent)
        hp_bar = "█" * hp_len + "░" * (40 - hp_len)
        color = Style.GREEN if hp_percent > 0.5 else Style.RED
        
        print_centered(f"BOSS HP: {int(event.boss_hp)} / 1000")
        print_centered(f"{color}[{hp_bar}]{Style.END}")
        print_centered("Complete tasks to deal damage!")

    elif event.type == EVENT_TYPE_BINGO:
        # 3x3 Bingo Izgarası
        print_centered("BINGO CARD")
        grid = event.bingo_grid
        # 0 1 2
        # 3 4 5
        # 6 7 8
        for r in range(0, 9, 3):
            row_str = ""
            for c in range(3):
                idx = r + c
                symbol = "✅" if grid[idx] else "⬜"
                row_str += f" [ {symbol} ] "
            print_centered(row_str)
        print_centered("Complete tasks to unlock cells!")

    elif event.type == EVENT_TYPE_CLIMB:
        # Kule Görünümü
        print_centered(f"🏢 CURRENT FLOOR: {Style.YELLOW}{event.current_floor}{Style.END}")
        print_centered("☁️  ☁️  ☁️")
        print_centered("  |   |  ")
        print_centered(f"  [{event.current_floor}]  ")
        print_centered("  |   |  ")
        print_centered("Base Camp")

    else:
        # Standart Progress Bar
        print_centered(draw_modern_bar(event.progress, event.goal, length=40, color=Style.PURPLE))

# --- YENİ: KART ÇİZİMİ (SADELEŞTİRİLMİŞ) ---
def draw_simple_card(player):
    """Yeni sade ve anlamlı oyuncu kartı"""
    stats = player.stats.attributes
    ovr = player.stats.get_overall()
    
    # Kart Rengi
    c = Style.CYAN if ovr >= 85 else (Style.YELLOW if ovr >= 75 else Style.END)
    e = Style.END
    
    print_centered(f"{c}╭─────────────────────────────╮{e}")
    print_centered(f"{c}│ {player.name:^27} │{e}")
    print_centered(f"{c}│ {player.position:^27} │{e}")
    print_centered(f"{c}│                             │{e}")
    print_centered(f"{c}│      {Style.BOLD}OVR {ovr}{e}{c}                 │{e}")
    print_centered(f"{c}│                             │{e}")
    print_centered(f"{c}│  OFF: {stats['OFF']:<3}       DEF: {stats['DEF']:<3}  │{e}")
    print_centered(f"{c}│  PHY: {stats['PHY']:<3}       MEN: {stats['MEN']:<3}  │{e}")
    print_centered(f"{c}│  TEC: {stats['TEC']:<3}               │{e}")
    print_centered(f"{c}│                             │{e}")
    print_centered(f"{c}│  {player.team_obj.name:^27}  │{e}")
    print_centered(f"{c}╰─────────────────────────────╯{e}")

# --- MENÜLER ---
def home_hub_view(player):
    clear_screen()
    print_header()
    
    # 1. ÜST BİLGİ
    print_section_header("🏠  H O M E   H U B", width=40)
    print_centered(f"{Style.CYAN}{player.get_today_str()}{Style.END}")
    
    # Kusursuz Seri Göstergesi
    streak_icon = "🔥" * (player.events.perfect_streak // 5 + 1)
    print_centered(f"PERFECT STREAK: {player.events.perfect_streak} Days {streak_icon}")
    
    print("\n")
    
    # 2. AKTİF ETKİNLİK PANELİ (EN ÖNEMLİ KISIM)
    draw_active_event_panel(player.events.current_event)
    
    print("\n" + "─" * 40)
    
    # 3. KISA ÖZET
    current_score = player.tasks.calculate_daily_score()
    score_color = Style.GREEN if current_score > 0 else Style.RED
    print_centered(f"DAILY XP PENDING: {score_color}{current_score}{Style.END}")
    
    print("\n" + " "*15 + f"{Style.YELLOW}[1]{Style.END} 🔁 Habits & Event Tasks")
    print(" "*15 + f"{Style.YELLOW}[2]{Style.END} 📝 Daily Tasks")
    print(" "*15 + f"{Style.YELLOW}[3]{Style.END} 📅 Calendar")
    print(" "*15 + f"{Style.RED}[{controls.KEY_BACK}]{Style.END} Back")

def habits_view(player):
    clear_screen()
    print_header()
    print_section_header("🔁  ROUTINES & EVENT TASKS", width=50)
    
    # Önce Event Görevlerini Göster
    if player.events.current_event and not player.events.current_event.is_locked:
        print_centered(f"{Style.PURPLE}--- EVENT OBJECTIVES ---{Style.END}")
        for i, t in enumerate(player.events.current_event.tasks):
            icon = "✅" if t['done'] else "⭕" # Event görevi farklı ikon
            color = Style.PURPLE if t['done'] else Style.END
            # Event görevleri listeye sanal olarak eklenir, buradan yönetilir
            print(" " * 10 + f"E{i+1}. {icon} {color}{t['task']}{Style.END} [XP: {t['xp']}]")
        print("\n")

    # Sonra Standart Habitler
    print_centered("--- DAILY HABITS ---")
    if not player.tasks.habits:
        print_centered("(No habits set)")
    else:
        for i, h in enumerate(player.tasks.habits):
            icon = "✅" if h.done else "⬜"
            color = Style.GREEN if h.done else Style.END
            print(" " * 10 + f"{i+1}. {icon} {color}{h.task:<25}{Style.END} [{h.diff}] {h.xp} XP")

    print("\n" + "━"*80)
    print(f" {Style.YELLOW}[A]{Style.END} Add Habit | {Style.YELLOW}[1-9]{Style.END} Toggle Habit | {Style.PURPLE}[E1-E3]{Style.END} Toggle Event Task")
    print(f" {Style.RED}[{controls.KEY_BACK}]{Style.END} Back")

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

# ... (Diğer fonksiyonlar: select_city_view, select_position_view, agenda_view, league_standings_view, main_menu_view) ...
# Bu fonksiyonlar önceki kodlarla hemen hemen aynıdır, yer kaplamasın diye tekrar yazmıyorum.
# Önceki views.py'den kopyalayıp buraya ekleyebilirsin. Sadece draw_fut_card yerine draw_simple_card geldi.
# UNUTMA: main_menu_view vb. fonksiyonları eklemeyi unutma!

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

def league_standings_view(league):
    clear_screen()
    print_header()
    print_section_header(f"🏆 {league.city_name.upper()} LEAGUE", width=50)
    print("\n")
    print_centered(f"{'CONFERENCE A':<35}  {'CONFERENCE B':<35}")
    print_centered("━"*74)
    league.conf_a.sort(key=lambda x: x.wins, reverse=True)
    league.conf_b.sort(key=lambda x: x.wins, reverse=True)
    for i in range(16):
        ta = league.conf_a[i]
        tb = league.conf_b[i]
        color = Style.GREEN if i < 8 else Style.END
        str_a = f"{i+1:2}. {color}{ta.name[:20]:<21}{Style.END} {ta.get_record()}"
        str_b = f"{i+1:2}. {color}{tb.name[:20]:<21}{Style.END} {tb.get_record()}"
        print(" " * 4 + f"{str_a:<45}  {str_b:<45}")
        if i == 7: print_centered(f"{Style.YELLOW}" + "-"*30 + " PLAYOFF CUTOFF " + "-"*30 + f"{Style.END}")
    print("\n")
    print_centered(f"[{controls.KEY_PLAY}] Play Match | [{controls.KEY_BACK}] Back")

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

def main_menu_view(player):
    clear_screen()
    print_header()
    print("\n")
    print_centered(f"Welcome, {Style.BOLD}{player.name}{Style.END} ({player.position})")
    print_centered(f"{player.team_obj.name} | {player.team_obj.get_record()}")
    print("\n")
    print_centered("╔════════════════════════════════════╗")
    print_centered(f"║ {Style.CYAN}[{controls.MENU_MATCH}]{Style.END} 🏀 PLAY NEXT MATCH (Career)    ║")
    print_centered(f"║ {Style.CYAN}[{controls.MENU_HOME}]{Style.END} 🏠 HOME HUB (Life RPG)         ║")
    print_centered(f"║ {Style.CYAN}[{controls.MENU_PROFILE}]{Style.END} 📊 PROFILE & CARDS             ║")
    print_centered(f"║ {Style.CYAN}[{controls.MENU_LEAGUE}]{Style.END} 🏆 LEAGUE TABLE                ║")
    print_centered(f"║ {Style.CYAN}[{controls.MENU_END_DAY}]{Style.END} 💤 END DAY (Apply XP)          ║")
    print_centered(f"║ {Style.RED}[{controls.KEY_QUIT}]{Style.END} QUIT                         ║")
    print_centered("╚════════════════════════════════════╝")