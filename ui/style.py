import os
import re
from core import controls

class Style:
    PURPLE = '\033[95m'; CYAN = '\033[96m'; DARKCYAN = '\033[36m'; BLUE = '\033[94m'
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
    BOLD = '\033[1m'; UNDERLINE = '\033[4m'; END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, width=80):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible_length = len(ansi_escape.sub('', text))
    padding = (width - visible_length) // 2
    print(" " * padding + text)

def print_header():
    print(f"{Style.BOLD}{Style.CYAN}" + "━"*80)
    print_centered(f"S T R E A K   L E A G U E   :   B E   A   P R O")
    print("━"*80 + f"{Style.END}")

def print_section_header(title, width=60):
    print("\n")
    print_centered(f"{Style.YELLOW}╔" + "═" * width + "╗" + f"{Style.END}")
    print_centered(f"{Style.BOLD}{title}{Style.END}")
    print_centered(f"{Style.YELLOW}╚" + "═" * width + "╝" + f"{Style.END}")

def draw_modern_bar(val, total, length=30, color=Style.GREEN):
    if total == 0: percent = 0
    else: percent = val / total
    filled_len = int(length * percent)
    bar = "█" * filled_len + "░" * (length - filled_len)
    percent_num = int(percent * 100)
    return f"{color}{bar} {percent_num}%{Style.END}"

def get_safe_input(prompt_text, input_type=str, valid_options=None, min_val=None, max_val=None):
    while True:
        try:
            user_input = input(f"{prompt_text}")
            if not user_input.strip():
                if input_type == str: return ""
                continue
            if input_type == int:
                val = int(user_input)
                if min_val is not None and val < min_val: continue
                if max_val is not None and val > max_val: continue
                return val
            else:
                val = user_input.upper() if valid_options else user_input
                if valid_options and val not in valid_options: continue
                return val
        except ValueError: pass