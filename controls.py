# controls.py

# --- GLOBAL TUŞ AYARLARI ---
# Tuşları buradan değiştirirsen tüm oyunda değişir.

KEY_BACK = 'B'
KEY_QUIT = 'Q'
KEY_ADD = 'A'
KEY_DELETE = 'D'      # Eskiden S idi, Delete için D daha mantıklı
KEY_IMPORT = 'I'
KEY_NEW = 'N'
KEY_EDIT = 'E'
KEY_PLAY = 'P'

# Menü Seçenekleri (Ana Menü)
MENU_MATCH = '1'
MENU_HOME = '2'
MENU_PROFILE = '3'
MENU_LEAGUE = '4'
MENU_END_DAY = '5'

# Zorluk Seviyeleri
DIFF_EASY = 'E'
DIFF_MEDIUM = 'M'
DIFF_HARD = 'H'

def get_input(prompt_text):
    """Standart input alma fonksiyonu"""
    return input(prompt_text).strip()

def get_upper_input(prompt_text):
    """Otomatik büyük harfe çeviren input"""
    return input(prompt_text).strip().upper()

def wait_for_enter():
    input("\n[Press Enter to Continue...]")