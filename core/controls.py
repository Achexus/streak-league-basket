# core/controls.py

# --- KLAVYE KISAYOLLARI ---
KEY_BACK = 'B'
KEY_QUIT = 'Q'
KEY_ADD = 'A'
KEY_DELETE = 'D'
KEY_IMPORT = 'I'
KEY_NEW = 'N'
KEY_EDIT = 'E'
KEY_PLAY = 'P'

# --- MENÜ SEÇENEKLERİ ---
MENU_MATCH = '1'
MENU_HOME = '2'
MENU_PROFILE = '3'
MENU_LEAGUE = '4'
MENU_END_DAY = '5'
MENU_EVENTS = '6'

# --- ZORLUKLAR ---
DIFF_EASY = 'E'
DIFF_MEDIUM = 'M'
DIFF_HARD = 'H'

# --- YARDIMCI FONKSİYONLAR ---
def wait_for_enter():
    input("\n[Press Enter to Continue...]")

def get_upper_input(prompt):
    return input(prompt).strip().upper()