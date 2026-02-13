# systems/loops.py
import time
from datetime import datetime, date
from core import controls
from models import AgendaItem
import ui

def tasks_loop(player):
    while True:
        ui.tasks_view(player)
        c = ui.get_safe_input(">> ", str).upper()
        
        if c == controls.KEY_BACK: 
            break
        elif c == controls.KEY_ADD: 
            n = input("Task Name: ")
            d = ui.get_safe_input("Diff (E/M/H): ", str, valid_options=['E','M','H'])
            player.tasks.add_task(n, d)
        elif c == controls.KEY_DELETE: 
            idx = ui.get_safe_input("Task #: ", int)
            try: player.tasks.remove_task(idx-1)
            except: pass
        elif c == controls.KEY_IMPORT: 
            count = player.import_agenda_to_task()
            print(f"   Imported {count} items.")
            time.sleep(1)
        elif c.isdigit(): 
            player.tasks.toggle_task(int(c)-1)

def calendar_loop(player):
    while True:
        ui.agenda_view(player)
        c = ui.get_safe_input(">> ", str).upper()
        
        if c == controls.KEY_BACK: 
            break
        elif c == controls.KEY_NEW:
            try:
                day = ui.get_safe_input("Day: ", int, min_val=1, max_val=31)
                dt = datetime(date.today().year, date.today().month, day)
                player.tasks.agenda.append(AgendaItem(dt, input("Note: ")))
            except: pass

def home_cycle(player, league):
    """Ev Döngüsü"""
    while True:
        ui.home_hub_view(player, league)
        c = ui.get_safe_input(">> ", str).upper()
        
        if c == controls.KEY_BACK: break
        elif c == 'A':
            n = input("Habit Name: ")
            d = ui.get_safe_input("Diff (E/M/H): ", str, valid_options=['E','M','H'])
            player.tasks.add_habit(n, d)
        elif c == '2': tasks_loop(player)
        elif c == '3': calendar_loop(player)
        elif c.isdigit(): player.tasks.toggle_habit(int(c)-1)

def event_cycle(player):
    """Etkinlik Döngüsü"""
    while True:
        ui.event_center_view(player)
        c = ui.get_safe_input(">> ", str).upper()
        
        if c == controls.KEY_BACK: break
        
        elif c.startswith('E') and c[1:].isdigit():
            idx = int(c[1:]) - 1
            if player.events.current_event:
                xp = player.events.current_event.complete_task(idx)
                if xp > 0:
                    print(f"   {ui.Style.GREEN}Objective Completed! +{xp} XP{ui.Style.END}")
                    time.sleep(0.5)