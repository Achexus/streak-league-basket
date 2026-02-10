# mechanics.py
import random
import time

def calculate_player_performance(player):
    """
    Oyuncunun performansını hesaplar.
    Bu artık 'Şans' değil, 'Hayaller' ve 'Level'e bağlıdır.
    """
    # Oyuncunun Stat Gücü (Hayallerinden gelir)
    off_power = player.stats.get_offense_power(player.level)
    def_power = player.stats.get_defense_power(player.level)
    
    # Ortalama bir performans değeri (0-40 arası)
    base_perf = (off_power + def_power) / 5 
    # Rastgelelik ekle
    real_perf = int(base_perf * random.uniform(0.5, 1.2))
    
    stats = {'pts': 0, 'ast': 0, 'reb': 0}
    
    # Mevkiye göre dağıt
    if player.position == "PG":
        stats['pts'] = int(real_perf * 0.4)
        stats['ast'] = int(real_perf * 0.4)
        stats['reb'] = int(real_perf * 0.1)
    elif player.position == "SG":
        stats['pts'] = int(real_perf * 0.7)
        stats['ast'] = int(real_perf * 0.2)
        stats['reb'] = int(real_perf * 0.1)
    elif player.position == "SF": # Dengeli
        stats['pts'] = int(real_perf * 0.5)
        stats['ast'] = int(real_perf * 0.25)
        stats['reb'] = int(real_perf * 0.25)
    elif player.position == "PF" or player.position == "C":
        stats['pts'] = int(real_perf * 0.4)
        stats['ast'] = int(real_perf * 0.1)
        stats['reb'] = int(real_perf * 0.5)
        
    return stats

def play_match(player, league):
    opponent = random.choice(league.teams)
    while opponent == player.team_obj:
        opponent = random.choice(league.teams)
        
    print(f"\n🏀 GAME DAY: {player.team_obj.name} vs {opponent.name}")
    print("WARMING UP", end="")
    for _ in range(3):
        time.sleep(0.3); print(".", end="", flush=True)
    print("\n")
    
    # Maç Skoru (Takım güçlerine göre)
    my_team_score = int(player.team_obj.offense * 0.8 + random.randint(10, 30))
    opp_team_score = int(opponent.offense * 0.8 + random.randint(10, 30))
    
    # Senin katkın (Bonus)
    my_stats = calculate_player_performance(player)
    # Eğer iyi oynadıysan takımına + puan
    if my_stats['pts'] > 20: my_team_score += 5
    
    if my_team_score == opp_team_score: my_team_score += 1
    
    won = my_team_score > opp_team_score
    if won: player.team_obj.wins += 1
    else: player.team_obj.losses += 1
    
    player.update_match_stats(my_stats['pts'], my_stats['ast'], my_stats['reb'])
    
    # Rapor
    res = "WON" if won else "LOST"
    color = "\033[92m" if won else "\033[91m"
    end = "\033[0m"
    
    print(f"   FINAL: {player.team_obj.name} {my_team_score} - {opp_team_score} {opponent.name} [{color}{res}{end}]")
    print("-" * 50)
    print(f"   YOUR STATS: {my_stats['pts']} PTS | {my_stats['ast']} AST | {my_stats['reb']} REB")
    print("   (XP awarded at End of Day, not here!)")