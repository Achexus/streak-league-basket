from .style import Style, print_centered, draw_modern_bar
from core.config import EVENT_TYPE_BOSS, EVENT_TYPE_BINGO, EVENT_TYPE_CLIMB

def draw_active_event_panel(event):
    """Aktif etkinlik panelini çizer"""
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
        hp_percent = event.boss_hp / 1000
        hp_len = int(40 * hp_percent)
        hp_bar = "█" * hp_len + "░" * (40 - hp_len)
        color = Style.GREEN if hp_percent > 0.5 else Style.RED
        
        print_centered(f"BOSS HP: {int(event.boss_hp)} / 1000")
        print_centered(f"{color}[{hp_bar}]{Style.END}")
        print_centered("Complete tasks to deal damage!")

    elif event.type == EVENT_TYPE_BINGO:
        print_centered("BINGO CARD")
        grid = event.bingo_grid
        for r in range(0, 9, 3):
            row_str = ""
            for c in range(3):
                idx = r + c
                symbol = "✅" if grid[idx] else "⬜"
                row_str += f" [ {symbol} ] "
            print_centered(row_str)
        print_centered("Complete tasks to unlock cells!")

    elif event.type == EVENT_TYPE_CLIMB:
        print_centered(f"🏢 CURRENT FLOOR: {Style.YELLOW}{event.current_floor}{Style.END}")
        print_centered("☁️  ☁️  ☁️")
        print_centered("  |   |  ")
        print_centered(f"  [{event.current_floor}]  ")
        print_centered("  |   |  ")
        print_centered("Base Camp")

    else:
        print_centered(draw_modern_bar(event.progress, 100, length=40, color=Style.PURPLE))

def draw_simple_card(player):
    """
    YATAY OYUNCU KARTI (Horizontal Strip Card)
    Format: 🃏 [İsim] [Takım] | ★ OVR | OFF:XX DEF:XX ...
    """
    stats = player.stats.attributes
    ovr = player.stats.get_overall()
    
    # 1. Kart Rengi (OVR'ye göre)
    if ovr >= 90:
        c = Style.CYAN      # Elit
    elif ovr >= 80:
        c = Style.YELLOW    # Altın
    elif ovr >= 70:
        c = Style.GREEN     # Gümüş
    else:
        c = Style.END       # Normal
    
    e = Style.END

    # 2. İçerik Hazırlama
    # İsim ve Takımı birleştir (Uzunsa kes)
    identity_str = f"{player.name} ({player.team_obj.name})"
    if len(identity_str) > 28:
        identity_str = identity_str[:25] + "..."
    
    # Statları tek satıra diz
    stats_str = f"OFF:{stats['OFF']} DEF:{stats['DEF']} PHY:{stats['PHY']} MEN:{stats['MEN']} TEC:{stats['TEC']}"
    
    # Ana Satırı Oluştur
    # 🃏 Name (Team)       ★ 85   | OFF:80 DEF:75 ...
    content = f"🃏 {identity_str:<28} ★ {ovr:<3} │ {stats_str}"
    
    # 3. Çerçeve Uzunluğunu Hesapla
    # (Metin uzunluğuna göre dinamik çerçeve)
    # Emoji (🃏) bazen terminalde 2 karakter yer kaplayabilir, görsel denge için +2 ekliyoruz.
    visual_len = len(content) + 1
    
    # 4. Çizim
    print_centered(f"{c}╭{'─'*visual_len}╮{e}")
    print_centered(f"{c}│ {content} │{e}")
    print_centered(f"{c}╰{'─'*visual_len}╯{e}")