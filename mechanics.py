# mechanics.py
import random
import time

def calculate_player_performance(player):
    stats = player.stats.attributes
    
    # 1. Şut ve Bitiricilik
    scoring_pot = (stats["SHT"] * 0.6) + (stats["FIN"] * 0.4)
    mental_factor = stats["MEN"] / 100 
    game_luck = random.uniform(0.8, 1.2)
    
    final_score_base = scoring_pot * mental_factor * game_luck
    
    # İstatistik Üretimi
    pts = int(final_score_base / 3.5)
    ast = int((stats["PAS"] / 10) * random.uniform(0.5, 1.5))
    reb = int((stats["REB"] / 12) * random.uniform(0.5, 1.5))
    stl = int((stats["DEF"] / 25) * random.uniform(0.0, 1.5))
    
    return {'pts': pts, 'ast': ast, 'reb': reb, 'stl': stl}

def play_match(player, league):
    opponent = random.choice(league.teams)
    while opponent == player.team_obj:
        opponent = random.choice(league.teams)
        
    print(f"\n🏀 GAME DAY: {player.team_obj.name} vs {opponent.name}")
    print("WARMING UP", end="")
    for _ in range(3):
        time.sleep(0.3); print(".", end="", flush=True)
    print("\n")
    
    my_team_ovr = player.team_obj.offense
    opp_team_ovr = opponent.offense
    
    my_perf = calculate_player_performance(player)
    
    # Yıldız Oyuncu Bonusu
    player_ovr = player.stats.get_overall()
    performance_rating = my_perf['pts'] + my_perf['ast'] + my_perf['reb']
    team_bonus = 0
    if performance_rating > (player_ovr / 3):
        team_bonus = 10 
        
    my_score = int(my_team_ovr * 0.9 + random.randint(5, 20) + team_bonus)
    opp_score = int(opp_team_ovr * 0.9 + random.randint(5, 20))
    
    if my_score == opp_score: my_score += 2 
    
    won = my_score > opp_score
    if won: player.team_obj.wins += 1
    else: player.team_obj.losses += 1
    
    player.update_match_stats(my_perf['pts'], my_perf['ast'], my_perf['reb'])
    
    res = "VICTORY" if won else "DEFEAT"
    color = "\033[92m" if won else "\033[91m"
    end = "\033[0m"
    
    print(f"   FINAL: {player.team_obj.name} {my_score} - {opp_score} {opponent.name} [{color}{res}{end}]")
    print("-" * 50)
    print(f"   YOUR STATS: {my_perf['pts']} PTS | {my_perf['ast']} AST | {my_perf['reb']} REB | {my_perf['stl']} STL")
    
    xp_gained = (my_perf['pts'] * 10) + (my_perf['ast'] * 15) + (my_perf['reb'] * 15)
    if won: xp_gained += 100
    
    player.xp_pool += int(xp_gained / 5) 
    print(f"   📈 EXPERIENCE: +{int(xp_gained/5)} XP gained from match.")