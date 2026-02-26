import os
from ui.style import Style, clear_screen, print_centered

def draw_main_title_screen(has_save_file):
    """Draws the detailed main title screen."""
    clear_screen()
    
    # ASCII Art Title
    title = f"""{Style.CYAN}
     ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗
    ██╔════╝ ██╔══██╗██║   ██║██╔══██╗╚══██╔══╝
    ██║  ███╗██████╔╝██║   ██║██████╔╝   ██║   
    ██║   ██║██╔══██╗██║   ██║██╔═══╝    ██║   
    ╚██████╔╝██║  ██║╚██████╔╝██║        ██║   
     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝        ╚═╝   
    {Style.END}"""
    
    print(title)
    print_centered(f"{Style.YELLOW}>>  H A B I T   T R A C K E R   &   R P G  <<{Style.END}")
    print("\n")
    
    # System Details for immersion
    print_centered(f"{Style.DARKCYAN}┌────────────────────────────────────────────────────────┐{Style.END}")
    print_centered(f"{Style.DARKCYAN}│{Style.END}  SYSTEM CORE: {Style.GREEN}ONLINE{Style.END}   |   DATABASE: {Style.GREEN}CONNECTED{Style.END}       {Style.DARKCYAN}│{Style.END}")
    print_centered(f"{Style.DARKCYAN}│{Style.END}  MODULES: INITIALIZED  |   ENGINE v1.0.0             {Style.DARKCYAN}│{Style.END}")
    print_centered(f"{Style.DARKCYAN}└────────────────────────────────────────────────────────┘{Style.END}")
    print("\n")

    # Main Menu Options
    print_centered(f"[{Style.CYAN}1{Style.END}] 🆕 NEW JOURNEY")
    
    if has_save_file:
        print_centered(f"[{Style.CYAN}2{Style.END}] 🔄 CONTINUE {Style.GREEN}[Save Found]{Style.END}")
    else:
        print_centered(f"[{Style.DARKCYAN}2{Style.END}] {Style.DARKCYAN}🔄 CONTINUE [No Save File]{Style.END}")
        
    print_centered(f"[{Style.CYAN}3{Style.END}] ⚙️  SETTINGS")
    print_centered(f"[{Style.CYAN}4{Style.END}] 🚪 QUIT")
    
    print("\n")
    print_centered(f"{Style.DARKCYAN}=========================================================={Style.END}")
    print_centered("Awaiting system input (1-4)")

def draw_dashboard(player):
    """Draws the player's main dashboard."""
    clear_screen()
    print_centered(f"{Style.CYAN}===================================================={Style.END}")
    print_centered(f"{Style.BOLD}🏀 PLAYER DASHBOARD 🏀{Style.END}")
    print_centered(f"{Style.CYAN}===================================================={Style.END}\n")

    # Top Info Strip (Now includes Position and Jersey Number)
    identity_str = f"#{player.jersey_number} {player.name} ({player.position})"
    print_centered(f"👤 {Style.YELLOW}{identity_str}{Style.END} | 🌟 LVL: {Style.CYAN}{player.level}{Style.END} | 🔥 STREAK: {Style.RED}{player.streak} Days{Style.END}\n")

    # Attributes
    print_centered(f"{Style.UNDERLINE}CURRENT ATTRIBUTES:{Style.END}")
    print_centered(f"🎯 SHOOTING (Work/Code)   : {Style.GREEN}{player.stats['SHOOTING']}{Style.END}")
    print_centered(f"🛡️ DEFENSE (Sports/Health): {Style.GREEN}{player.stats['DEFENSE']}{Style.END}")
    print_centered(f"🧠 PLAYMAKING (Mind)      : {Style.GREEN}{player.stats['PLAYMAKING']}{Style.END}\n")

    # Task List
    print_centered(f"{Style.UNDERLINE}DAILY TASKS:{Style.END}")
    if not player.daily_tasks:
        print_centered("(No tasks added for today. You can add them from the menu.)")
    else:
        for idx, task in enumerate(player.daily_tasks):
            status = f"{Style.GREEN}✅{Style.END}" if task["done"] else f"{Style.RED}❌{Style.END}"
            print_centered(f"{idx + 1}. [{status}] {task['name']} {Style.DARKCYAN}({task['category']}){Style.END}")

    print("\n")
    print_centered(f"{Style.DARKCYAN}----------------------------------------------------{Style.END}")
    print_centered(f"[{Style.CYAN}1{Style.END}] Add Task      |  [{Style.CYAN}2{Style.END}] Complete Task")
    print_centered(f"[{Style.CYAN}3{Style.END}] End Day       |  [{Style.CYAN}4{Style.END}] Main Menu")
    print_centered(f"{Style.DARKCYAN}----------------------------------------------------{Style.END}")