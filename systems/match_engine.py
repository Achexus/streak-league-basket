import random
import time

def calculate_player_performance(player):
    # (Eski kodun aynısı - Sadece görsel kısalttım)
    stats = player.stats.attributes
    scoring_base = (stats["OFF"] * 0.5) + (stats["TEC"] * 0.3) + (stats["MEN"] * 0.2)
    form_factor = random.uniform(0.8, 1.2)
    streak_bonus = player.get_match_bonus()
    final_score_pot = (scoring_base + streak_bonus) * form_factor
    pts = int(final_score_pot / 3.5)
    ast = int(((stats["TEC"]*0.7) + (stats["MEN"]*0.3))/12 * random.uniform(0.5, 1.5))
    reb = int(((stats["PHY"]*0.6) + (stats["DEF"]*0.4))/14 * random.uniform(0.5, 1.5))
    stl = int(((stats["DEF"]*0.8) + (stats["PHY"]*0.2))/25 * random.uniform(0.0, 1.5))
    return {'pts': pts, 'ast': ast, 'reb': reb, 'stl': stl}

def simulate_match_logic(fixture):
    """Tekil maç simülasyonu (Oyuncusuz)"""
    if fixture.played: return
    
    hs = int(fixture.home_team.offense * 0.9 + random.randint(5, 25))
    as_ = int(fixture.away_team.offense * 0.9 + random.randint(5, 25))
    if hs == as_: hs += 1 # Beraberlik yok
    
    fixture.home_score = hs
    fixture.away_score = as_
    fixture.played = True
    
    if hs > as_:
        fixture.home_team.wins += 1
        fixture.away_team.losses += 1
    else:
        fixture.away_team.wins += 1
        fixture.home_team.losses += 1

def simulate_entire_week(league_manager):
    """
    DEVASA SİMÜLASYON: 
    17 Ligdeki o haftanın tüm maçlarını (oyuncunun maçı hariç) oynatır.
    """
    week = league_manager.current_week
    
    for league in league_manager.get_all_leagues():
        fixtures = league.get_week_fixtures(week)
        for f in fixtures:
            # Eğer maç oynanmadıysa (Oyuncunun maçı oynandıysa o True olmuştur)
            if not f.played:
                simulate_match_logic(f)

def play_match(player, league_manager):
    # Oyuncunun ligini bul
    # Player nesnesine 'league_id' eklememiz gerekecek
    player_league = league_manager.get_league(player.league_id)
    
    my_match = player_league.get_my_match(player.team_obj, league_manager.current_week)
    
    if not my_match:
        print("⚠️  No match scheduled.")
        return
    if my_match.played:
        print("⚠️  Match already played.")
        return

    opponent = my_match.away_team if my_match.home_team.name == player.team_obj.name else my_match.home_team
    
    print(f"\n🏀 GAME DAY: {player.team_obj.name} vs {opponent.name}")
    print("WARMING UP", end="")
    for _ in range(3):
        time.sleep(0.3); print(".", end="", flush=True)
    print("\n")
    
    # Performans & Skor
    my_perf = calculate_player_performance(player)
    
    my_pwr = player.team_obj.offense
    opp_pwr = opponent.offense
    
    # Yıldız oyuncu bonusu
    perf_sum = my_perf['pts'] + my_perf['ast'] + my_perf['reb']
    bonus = 10 if perf_sum > (player.stats.get_overall()/3) else 0
    
    my_score = int(my_pwr * 0.9 + random.randint(10, 20) + bonus)
    opp_score = int(opp_pwr * 0.9 + random.randint(10, 20))
    if my_score == opp_score: my_score += 1
    
    my_match.home_score = my_score if my_match.home_team.name == player.team_obj.name else opp_score
    my_match.away_score = opp_score if my_match.home_team.name == player.team_obj.name else my_score
    my_match.played = True
    
    won = my_score > opp_score
    if won: player.team_obj.wins += 1
    else: player.team_obj.losses += 1
    
    player.update_match_stats(my_perf['pts'], my_perf['ast'], my_perf['reb'], my_perf['stl'], 0)
    
    res = "VICTORY" if won else "DEFEAT"
    print("-" * 50)
    print(f"   FINAL: {my_match} [{res}]")
    print("-" * 50)
    print(f"   STATS: {my_perf['pts']} PTS | {my_perf['ast']} AST")
    
    xp = (my_perf['pts']*2) + (my_perf['ast']*3) + 50 if won else 0
    player.xp_pool += xp
    
    # MAÇ BİTTİ, ŞİMDİ TÜM DÜNYAYI SİMÜLE ET
    print("\n🌎 Simulating results from other stadiums...")
    simulate_entire_week(league_manager)
    time.sleep(1)
    
    # Haftayı ilerlet
    league_manager.current_week += 1