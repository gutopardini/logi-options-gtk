"""
Mapeamento de Keycodes do Linux / evdev e Ações Predefinidas para o Logi Options GTK
"""

KEY_MAP = {
    # Modificadores
    "KEY_LEFTMETA": "Super",
    "KEY_RIGHTMETA": "Super",
    "KEY_LEFTCTRL": "Ctrl",
    "KEY_RIGHTCTRL": "Ctrl",
    "KEY_LEFTALT": "Alt",
    "KEY_RIGHTALT": "AltGr",
    "KEY_LEFTSHIFT": "Shift",
    "KEY_RIGHTSHIFT": "Shift",
    
    # Navegação e Edição
    "KEY_PAGEUP": "Page Up",
    "KEY_PAGEDOWN": "Page Down",
    "KEY_HOME": "Home",
    "KEY_END": "End",
    "KEY_UP": "Up",
    "KEY_DOWN": "Down",
    "KEY_LEFT": "Left",
    "KEY_RIGHT": "Right",
    "KEY_SPACE": "Space",
    "KEY_ENTER": "Enter",
    "KEY_ESC": "Esc",
    "KEY_TAB": "Tab",
    "KEY_BACKSPACE": "Backspace",
    "KEY_DELETE": "Delete",
    "KEY_EQUAL": "+",
    "KEY_MINUS": "-",
    
    # Mídia e Especiais
    "KEY_PLAYPAUSE": "Play/Pause",
    "KEY_MUTE": "Mute",
    "KEY_VOLUMEUP": "Volume Up",
    "KEY_VOLUMEDOWN": "Volume Down",
    "KEY_NEXTSONG": "Next Track",
    "KEY_PREVIOUSSONG": "Prev Track",
    "KEY_FORWARD": "Forward",
    "KEY_BACK": "Back",
    "KEY_PRINT": "Prnt Scrn",
    "KEY_SYSRQ": "Prnt Scrn",
    "KEY_BRIGHTNESSUP": "Brightness Up",
    "KEY_BRIGHTNESSDOWN": "Brightness Down",
    "KEY_CALC": "Calculator",
    "KEY_DOT": ".",
    "KEY_COMMA": ",",
}

# Preenche letras e números automaticamente
for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    KEY_MAP[f"KEY_{c}"] = c
for n in "0123456789":
    KEY_MAP[f"KEY_{n}"] = n
for i in range(1, 13):
    KEY_MAP[f"KEY_F{i}"] = f"F{i}"

REV_KEY_MAP = {v: k for k, v in KEY_MAP.items()}


def format_keys_display(keys_list):
    """Converte lista de chaves KEY_* em texto amigável (ex: Prnt Scrn ou Ctrl + C)"""
    if not keys_list:
        return "None"
    labels = [KEY_MAP.get(k, k.replace("KEY_", "")) for k in keys_list]
    return " + ".join(labels)
