import os
import time
import calendar
import re
from datetime import date
from config import TURKEY_DATA

# --- RENKLER VE STİL ---
class Style:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Terminali temizler ve imleci en başa alır"""
    # Windows için 'cls', diğerleri için 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, width=80):
    """Metni ortalar (Renk kodlarını hesaba katarak)"""
    # Görünmez renk kodlarını temizle ki gerçek uzunluğu bulalım
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible_length = len(ansi_escape.sub('', text))
    padding = (width - visible_length) // 2
    print(" " * padding + text)

def print_header():
    print(f"{Style.BOLD}{Style.CYAN}" + "━"*80)
    print_centered(f"S T R E A K   L E A G U E   :   B E   A   P R O")
    print("━"*80 + f"{Style.END}")

def print_section_header(title, width=60):
    """Yan çizgiler olmadan şık bir başlık kutusu (KAYMA YAPMAZ)"""
    print("\n")
    print_centered(f"{Style.YELLOW}╔" + "═" * width + "╗" + f"{Style.END}")
    print_centered(f"{Style.BOLD}{title}{Style.END}")
    print_centered(f"{Style.YELLOW}╚" + "═" * width + "╝" + f"{Style.END}")

def draw_modern_bar(val, total, length=30, color=Style.GREEN):
    if total == 0: 
        percent = 0
    else:
        percent = val / total
    
    filled_len = int(length * percent)
    # Dolu kısım kare, boş kısım nokta
    bar = "█" * filled_len + "░" * (length - filled_len)
    percent_num = int(percent * 100)
    return f"{color}{bar} {percent_num}%{Style.END}"

# --- MENÜ GÖRÜNÜMLERİ ---

def home_hub_view(player):
    clear_screen() # EKRANI EN BAŞTAN TEMİZLE
    print_header()

    # ÜST BİLGİ KUTUSU (Yan çizgiler yok, kayma riski yok)
    print_section_header("🏠  H O M E   H U B", width=40)
    print_centered(f"{Style.CYAN}{player.get_today_str()}{Style.END}")
    print("\n")
    print_centered(f"PLAYER: {Style.BOLD}{player.name}{Style.END} | LEVEL: {Style.YELLOW}{player.level}{Style.END}")
    print_centered(f"XP POOL: {Style.GREEN}{player.xp_pool} pts{Style.END}")

    print("\n")

    # FOCUS BAR
    current_score = player.tasks.calculate_daily_score()
    
    total_habits = len(player.tasks.habits)
    done_habits = sum(1 for h in player.tasks.habits if h.done)
    total_tasks = len(player.tasks.daily_tasks)
    done_tasks = sum(1 for t in player.tasks.daily_tasks if t.done)
    
    total_all = total_habits + total_tasks
    done_all = done_habits + done_tasks

    print_centered(f"{Style.BOLD}DAILY FOCUS & GRIND{Style.END}")
    print_centered(draw_modern_bar(done_all, total_all, length=40, color=Style.BLUE))
    
    print("\n")
    
    # SKOR TABLOSU
    score_color = Style.GREEN if current_score > 0 else Style.RED
    print_centered("─" * 40)
    print_centered(f"PENDING SCORE: {score_color}{current_score}{Style.END}")
    print_centered(f"YESTERDAY:     {player.tasks.yesterday_score}")
    print_centered("─" * 40)

    print("\n" + " "*15 + "Choose Action:")
    print(" "*15 + f"{Style.YELLOW}[1]{Style.END} 🔁 Habits (Routines)")
    print(" "*15 + f"{Style.YELLOW}[2]{Style.END} 📝 Daily Tasks")
    print(" "*15 + f"{Style.YELLOW}[3]{Style.END} 📅 Calendar")
    print(" "*15 + f"{Style.RED}[B]{Style.END} Back")


def habits_view(player):
    clear_screen()
    print_header()
    print_section_header("🔁  DAILY ROUTINES", width=40)
    print_centered("Reset every morning.")
    print("\n")
    
    if not player.tasks.habits:
        print_centered("(No habits set yet. Add one!)")
    else:
        for i, h in enumerate(player.tasks.habits):
            icon = "✅" if h.done else "⬜"
            color = Style.GREEN if h.done else Style.END
            # Hizalama için f-string padding kullanıyoruz
            line = f"{i+1}. {icon} {color}{h.task:<25}{Style.END} [{h.diff}] {h.xp} XP"
            print(" " * 15 + line)

    print("\n" + "━"*80)
    print(f" {Style.YELLOW}[A]{Style.END} Add Habit | {Style.YELLOW}[Number]{Style.END} Check/Uncheck | {Style.RED}[B]{Style.END} Back")


def tasks_view(player):
    clear_screen()
    print_header()
    print_section_header("📝  ONE-OFF TASKS", width=40)
    print("\n")
    
    # AJANDA UYARISI
    alerts = player.check_agenda_alerts()
    if alerts:
        print_centered(f"{Style.RED}🔔 AGENDA ALERT! PRESS 'I' TO IMPORT 🔔{Style.END}")
        for alert in alerts:
            print_centered(f"• {alert}")
        print("\n")
    
    if not player.tasks.daily_tasks:
        print_centered("(No tasks for today)")
    else:
        for i, t in enumerate(player.tasks.daily_tasks):
            icon = "✅" if t.done else "⬜"
            color = Style.GREEN if t.done else Style.END
            line = f"{i+1}. {icon} {color}{t.task:<25}{Style.END} [{t.diff}] {t.xp} XP"
            print(" " * 15 + line)

    print("\n" + "━"*80)
    print(f" [A] Add | [S] Del | [I] Import | [Num] Toggle | [B] Back")


def agenda_view(player):
    clear_screen()
    print_header()
    print_section_header("📅  CALENDAR", width=40)
    print("\n")
    
    cal = calendar.month(date.today().year, date.today().month)
    for line in cal.split('\n'):
        print_centered(line)
        
    print_centered("─" * 40)
    
    upcoming = [x for x in player.tasks.agenda if x.event_date.date() >= date.today()]
    upcoming.sort(key=lambda x: x.event_date)
    
    if not upcoming:
        print_centered("No upcoming events.")
    else:
        for item in upcoming:
            d_str = item.event_date.strftime('%d %b')
            print(" " * 20 + f"📅 {Style.CYAN}{d_str}{Style.END} : {item.content}")

    print("\n" + "━" * 80)
    print(" [N] New Event | [B] Back")


def profile_view(player):
    clear_screen()
    print_header()
    
    print_section_header("📊  PLAYER CARD", width=50)
    print_centered(f"{Style.BOLD}{player.name} #{player.number}{Style.END}")
    print_centered(f"{player.team_obj.name}")
    print_centered(f"{player.city}")
    
    print("\n")
    
    off_p = player.stats.get_offense_power(player.level)
    def_p = player.stats.get_defense_power(player.level)
    
    # Barları ortalamak için biraz manuel boşluk bırakıyoruz
    bar_width = 30
    
    print(" " * 15 + f"⚡ LEVEL: {Style.YELLOW}{player.level}{Style.END}")
    print(" " * 15 + f"   Lifetime XP: {player.total_lifetime_xp}")
    print("\n")
    
    off_bar = "█" * (off_p // 10) + "░" * (10 - (off_p // 10))
    def_bar = "█" * (def_p // 10) + "░" * (10 - (def_p // 10))
    
    print(" " * 15 + f"OFFENSE: {Style.RED}{off_bar}{Style.END} ({off_p})")
    print(" " * 15 + f"DEFENSE: {Style.BLUE}{def_bar}{Style.END} ({def_p})")
    
    print("\n")
    print_centered(f"{Style.UNDERLINE}CAREER STATS{Style.END}")
    print_centered(player.get_averages())
    
    print("\n")
    print_centered(f"{Style.UNDERLINE}DREAMS (Attack){Style.END}")
    for s in player.stats.dreams:
        print_centered(f"🌟 {s.name}")
    
    print("\n")
    input(f"{Style.YELLOW}      [Press Enter to Back]{Style.END}")


def select_city_view():
    clear_screen()
    print_header()
    print_section_header("🏙️  SELECT CITY", width=40)
    print("\n")
    
    # 3 Sütunlu Düzen
    items = list(TURKEY_DATA.items())
    for i in range(0, len(items), 3):
        row = items[i:i+3]
        line = ""
        for code, data in row:
            line += f"[{code}] {data['name']:<15}"
        print_centered(line)

    while True:
        try:
            return int(input("\n" + " "*30 + "Enter Code: "))
        except: pass

def select_position_view():
    print("\n")
    print_centered("🏀 SELECT POSITION")
    print_centered("──────────────────")
    print_centered("1. PG - Point Guard")
    print_centered("2. SG - Shooting Guard")
    print_centered("3. SF - Small Forward")
    print_centered("4. PF - Power Forward")
    print_centered("5. C  - Center")
    m = {1:"PG", 2:"SG", 3:"SF", 4:"PF", 5:"C"}
    while True:
        try:
            return m[int(input("\n" + " "*30 + "Select: "))]
        except: pass
    
def play_intro_animation():
    # Hızlı açılması için animasyonu atlayabiliriz veya kısa tutabiliriz
    clear_screen()
    print("\n"*10)
    print_centered("🏀 LOADING STREAK LEAGUE...")
    time.sleep(1)

def league_standings_view(league):
    clear_screen()
    print_header()
    print_section_header(f"🏆 {league.city_name.upper()} LEAGUE", width=50)
    
    print("\n")
    header = f"{'CONFERENCE A':<35}  {'CONFERENCE B':<35}"
    print_centered(header)
    print_centered("━"*74)
    
    league.conf_a.sort(key=lambda x: x.wins, reverse=True)
    league.conf_b.sort(key=lambda x: x.wins, reverse=True)
    
    for i in range(16):
        ta = league.conf_a[i]
        tb = league.conf_b[i]
        
        color = Style.GREEN if i < 8 else Style.END
        
        # Stringleri hazırla
        str_a = f"{i+1:2}. {color}{ta.name[:20]:<21}{Style.END} {ta.get_record()}"
        str_b = f"{i+1:2}. {color}{tb.name[:20]:<21}{Style.END} {tb.get_record()}"
        
        # Yan yana bas, ortalamak için padding kullan
        full_line = f"{str_a:<45}  {str_b:<45}"
        # Ortalamak için biraz hile yapıyoruz, manuel boşluk
        print(" " * 4 + full_line)
        
        if i == 7:
             print_centered(f"{Style.YELLOW}" + "-"*30 + " PLAYOFF CUTOFF " + "-"*30 + f"{Style.END}")

    print("\n")
    print_centered("[P] Play Match | [B] Back")

def main_menu_view(player):
    clear_screen()
    print_header()
    
    # Hoşgeldin Mesajı
    print("\n")
    print_centered(f"Welcome, {Style.BOLD}{player.name}{Style.END} ({player.position})")
    print_centered(f"{player.team_obj.name}")
    print_centered(f"Record: {player.team_obj.get_record()}")
    
    print("\n")
    print_centered("╔════════════════════════════════════╗")
    print_centered(f"║ {Style.CYAN}[1]{Style.END} 🏀 PLAY NEXT MATCH (Career)    ║")
    print_centered(f"║ {Style.CYAN}[2]{Style.END} 🏠 HOME HUB (Life RPG)         ║")
    print_centered(f"║ {Style.CYAN}[3]{Style.END} 📊 PROFILE & STATS             ║")
    print_centered(f"║ {Style.CYAN}[4]{Style.END} 🏆 LEAGUE TABLE                ║")
    print_centered(f"║ {Style.CYAN}[5]{Style.END} 💤 END DAY (Apply XP)          ║")
    print_centered(f"║ {Style.RED}[Q]{Style.END} QUIT                         ║")
    print_centered("╚════════════════════════════════════╝")
    