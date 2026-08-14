"""
Gerenciador e Parser Completo de Configuração do LogiOps (logid.cfg)
Suporta 100% dos botões e recursos do MX Master 3S:
- 0x52: Middle Click (Roda)
- 0xc4: Top Button (Mode Shift)
- 0x56: Forward (Avançar)
- 0x53: Back (Voltar)
- 0xc3: Gesture Button (Gestos ou Ação Simples)
- thumbwheel: Roda do Polegar (divert: true/false + intervalo + teclas)
- smartshift: Free-spin automático + threshold + torque
- hiresscroll: Rolagem suave alta resolução
- dpi: Resolução do sensor óptico
"""

import os
import re
from pathlib import Path

DEFAULT_DOCUMENTS_PATH = Path(os.path.expanduser("~/Documents/logid.cfg"))
SYSTEM_PATH = Path("/etc/logid.cfg")


class LogidConfig:
    def __init__(self):
        self.device_name = "MX Master 3S"
        self.dpi = 1600
        
        # SmartShift
        self.smartshift_on = True
        self.smartshift_threshold = 30
        self.smartshift_torque = 50
        
        # HiRes Scroll
        self.hiresscroll_hires = True
        self.hiresscroll_invert = False
        self.hiresscroll_target = False
        
        # Thumbwheel
        self.thumbwheel_divert = True
        self.thumbwheel_invert = False
        self.thumbwheel_left_interval = 7
        self.thumbwheel_left_keys = ["KEY_LEFTMETA", "KEY_PAGEUP"]
        self.thumbwheel_right_interval = 7
        self.thumbwheel_right_keys = ["KEY_LEFTMETA", "KEY_PAGEDOWN"]
        
        # Botões
        # 0x52: Botão do Meio (Wheel Click)
        self.btn_middle_keys = [] # [] = Default middle click
        
        # 0xc4: Botão Superior
        self.btn_top_keys = ["KEY_LEFTMETA", "KEY_SPACE"]
        
        # 0xc3: Botão de Gestos
        self.gesture_mode = "gestures" # "gestures" ou "keypress"
        self.gesture_single_keys = ["KEY_LEFTMETA"]
        self.gesture_up_keys = ["KEY_LEFTMETA"]
        self.gesture_down_keys = ["KEY_LEFTMETA"]
        self.gesture_left_keys = ["KEY_LEFTMETA", "KEY_PAGEUP"]
        self.gesture_right_keys = ["KEY_LEFTMETA", "KEY_PAGEDOWN"]
        
        # 0x56: Avançar
        self.btn_forward_keys = ["KEY_FORWARD"]
        
        # 0x53: Voltar
        self.btn_back_keys = ["KEY_BACK"]

    def load_from_file(self, file_path=None):
        target = file_path
        if target is None:
            if DEFAULT_DOCUMENTS_PATH.exists():
                target = DEFAULT_DOCUMENTS_PATH
            elif SYSTEM_PATH.exists():
                target = SYSTEM_PATH
            else:
                return False

        try:
            with open(target, "r", encoding="utf-8") as f:
                content = f.read()
            self.parse_content(content)
            return True
        except Exception as e:
            print(f"Erro ao ler {target}: {e}")
            return False

    def parse_content(self, text: str):
        # DPI
        dpi_m = re.search(r"dpi\s*:\s*(\d+);", text)
        if dpi_m:
            self.dpi = int(dpi_m.group(1))

        # SmartShift
        ss_m = re.search(r"smartshift\s*:\s*\{([^}]+)\}", text)
        if ss_m:
            block = ss_m.group(1)
            on_m = re.search(r"on\s*:\s*(true|false);", block)
            if on_m:
                self.smartshift_on = (on_m.group(1) == "true")
            th_m = re.search(r"threshold\s*:\s*(\d+);", block)
            if th_m:
                self.smartshift_threshold = int(th_m.group(1))
            tq_m = re.search(r"torque\s*:\s*(\d+);", block)
            if tq_m:
                self.smartshift_torque = int(tq_m.group(1))

        # HiRes Scroll
        hrs_m = re.search(r"hiresscroll\s*:\s*\{([^}]+)\}", text)
        if hrs_m:
            block = hrs_m.group(1)
            h_m = re.search(r"hires\s*:\s*(true|false);", block)
            if h_m:
                self.hiresscroll_hires = (h_m.group(1) == "true")
            inv_m = re.search(r"invert\s*:\s*(true|false);", block)
            if inv_m:
                self.hiresscroll_invert = (inv_m.group(1) == "true")

        # Thumbwheel
        tw_m = re.search(r"thumbwheel\s*:\s*\{(.+?)\n\s*\}\s*;", text, re.DOTALL)
        if tw_m:
            block = tw_m.group(1)
            div_m = re.search(r"divert\s*:\s*(true|false);", block)
            if div_m:
                self.thumbwheel_divert = (div_m.group(1) == "true")
            inv_m = re.search(r"invert\s*:\s*(true|false);", block)
            if inv_m:
                self.thumbwheel_invert = (inv_m.group(1) == "true")

            left_m = re.search(r"left\s*:\s*\{([^}]+keys\s*=\s*\[(.*?)\];?[^}]*)\}", block, re.DOTALL)
            if left_m:
                l_block = left_m.group(1)
                l_int = re.search(r"interval\s*:\s*(\d+);", l_block)
                if l_int:
                    self.thumbwheel_left_interval = int(l_int.group(1))
                l_keys = re.findall(r'"([^"]+)"', left_m.group(2))
                if l_keys:
                    self.thumbwheel_left_keys = l_keys

            right_m = re.search(r"right\s*:\s*\{([^}]+keys\s*=\s*\[(.*?)\];?[^}]*)\}", block, re.DOTALL)
            if right_m:
                r_block = right_m.group(1)
                r_int = re.search(r"interval\s*:\s*(\d+);", r_block)
                if r_int:
                    self.thumbwheel_right_interval = int(r_int.group(1))
                r_keys = re.findall(r'"([^"]+)"', right_m.group(2))
                if r_keys:
                    self.thumbwheel_right_keys = r_keys

        # Buttons
        # 0x52 (Middle button)
        btn_52 = re.search(r"cid\s*:\s*0x52;.*?keys\s*=\s*\[(.*?)\];", text, re.DOTALL)
        if btn_52:
            keys = re.findall(r'"([^"]+)"', btn_52.group(1))
            self.btn_middle_keys = keys

        # 0xc4 (Top button)
        btn_c4 = re.search(r"cid\s*:\s*0xc4;.*?keys\s*=\s*\[(.*?)\];", text, re.DOTALL)
        if btn_c4:
            keys = re.findall(r'"([^"]+)"', btn_c4.group(1))
            if keys:
                self.btn_top_keys = keys

        # 0x56 (Forward)
        btn_56 = re.search(r"cid\s*:\s*0x56;.*?keys\s*=\s*\[(.*?)\];", text, re.DOTALL)
        if btn_56:
            keys = re.findall(r'"([^"]+)"', btn_56.group(1))
            if keys:
                self.btn_forward_keys = keys

        # 0x53 (Back)
        btn_53 = re.search(r"cid\s*:\s*0x53;.*?keys\s*=\s*\[(.*?)\];", text, re.DOTALL)
        if btn_53:
            keys = re.findall(r'"([^"]+)"', btn_53.group(1))
            if keys:
                self.btn_back_keys = keys

        # Gestures (0xc3)
        gestures_block = re.search(r"cid\s*:\s*0xc3;.*?gestures\s*:\s*\((.*?)\);", text, re.DOTALL)
        if gestures_block:
            self.gesture_mode = "gestures"
            g_body = gestures_block.group(1)
            for direction in ["Up", "Down", "Left", "Right"]:
                dir_match = re.search(rf'direction\s*:\s*"{direction}";.*?keys\s*=\s*\[(.*?)\];', g_body, re.DOTALL)
                if dir_match:
                    keys = re.findall(r'"([^"]+)"', dir_match.group(1))
                    if keys:
                        if direction == "Up":
                            self.gesture_up_keys = keys
                        elif direction == "Down":
                            self.gesture_down_keys = keys
                        elif direction == "Left":
                            self.gesture_left_keys = keys
                        elif direction == "Right":
                            self.gesture_right_keys = keys
        else:
            # Verifica se foi mapeado como Keypress simples
            btn_c3 = re.search(r"cid\s*:\s*0xc3;.*?keys\s*=\s*\[(.*?)\];", text, re.DOTALL)
            if btn_c3:
                self.gesture_mode = "keypress"
                keys = re.findall(r'"([^"]+)"', btn_c3.group(1))
                if keys:
                    self.gesture_single_keys = keys

    def generate_config_string(self) -> str:
        def format_keys(klist):
            return ", ".join(f'"{k}"' for k in klist)

        buttons_entries = []

        # 0x52: Middle button se customizado
        if self.btn_middle_keys:
            buttons_entries.append(f"""    // Botão do meio (Roda)
    {{
      cid: 0x52;
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.btn_middle_keys)}];
      }};
    }}""")

        # 0xc4: Botão Superior
        if self.btn_top_keys:
            buttons_entries.append(f"""    // Botão superior atrás da roda de rolagem
    {{
      cid: 0xc4;
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.btn_top_keys)}];
      }};
    }}""")

        # 0xc3: Botão de Gestos
        if self.gesture_mode == "keypress" and self.gesture_single_keys:
            buttons_entries.append(f"""    // Botão de gestos (Ação direta)
    {{
      cid: 0xc3;
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.gesture_single_keys)}];
      }};
    }}""")
        else:
            buttons_entries.append(f"""    // Botão de gestos (no apoio do polegar)
    {{
      cid: 0xc3;
      action =
      {{
        type: "Gestures";
        gestures:
        (
          {{
            direction: "Up";
            mode: "OnRelease";
            action =
            {{
              type: "Keypress";
              keys: [{format_keys(self.gesture_up_keys)}];
            }};
          }},
          {{
            direction: "Down";
            mode: "OnRelease";
            action =
            {{
              type: "Keypress";
              keys: [{format_keys(self.gesture_down_keys)}];
            }};
          }},
          {{
            direction: "Left";
            mode: "OnRelease";
            action =
            {{
              type: "Keypress";
              keys: [{format_keys(self.gesture_left_keys)}];
            }};
          }},
          {{
            direction: "Right";
            mode: "OnRelease";
            action =
            {{
              type: "Keypress";
              keys: [{format_keys(self.gesture_right_keys)}];
            }};
          }}
        );
      }};
    }}""")

        # 0x56: Lateral Avançar
        if self.btn_forward_keys:
            buttons_entries.append(f"""    // Botão lateral avançar
    {{
      cid: 0x56;
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.btn_forward_keys)}];
      }};
    }}""")

        # 0x53: Lateral Voltar
        if self.btn_back_keys:
            buttons_entries.append(f"""    // Botão lateral voltar
    {{
      cid: 0x53;
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.btn_back_keys)}];
      }};
    }}""")

        buttons_block = ",\n".join(buttons_entries)

        cfg = f"""devices:
({{
  name: "{self.device_name}";

  // Transição automática para rolagem livre (Free-spin)
  smartshift:
  {{
    on: {"true" if self.smartshift_on else "false"};
    threshold: {self.smartshift_threshold};
    torque: {self.smartshift_torque};
  }};

  // Rolagem de alta resolução suave
  hiresscroll:
  {{
    hires: {"true" if self.hiresscroll_hires else "false"};
    invert: {"true" if self.hiresscroll_invert else "false"};
    target: false;
  }};

  // Roda de rolagem do polegar (Thumbwheel)
  thumbwheel:
  {{
    divert: {"true" if self.thumbwheel_divert else "false"};
    invert: {"true" if self.thumbwheel_invert else "false"};

    left:
    {{
      mode: "OnInterval";
      interval: {self.thumbwheel_left_interval};
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.thumbwheel_left_keys)}];
      }};
    }};

    right:
    {{
      mode: "OnInterval";
      interval: {self.thumbwheel_right_interval};
      action =
      {{
        type: "Keypress";
        keys: [{format_keys(self.thumbwheel_right_keys)}];
      }};
    }};
  }};

  dpi: {self.dpi};

  buttons:
  (
{buttons_block}
  );
}});
"""
        return cfg
