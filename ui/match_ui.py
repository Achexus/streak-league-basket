from .style import Style, print_centered, print_header, print_section_header
from core import controls

def league_standings_view(league):
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
        if i == 7: 
            print_centered(f"{Style.YELLOW}" + "-"*30 + " PLAYOFF CUTOFF " + "-"*30 + f"{Style.END}")
            
    print("\n")
    print_centered(f"[{controls.KEY_PLAY}] Play Match | [{controls.KEY_BACK}] Back")