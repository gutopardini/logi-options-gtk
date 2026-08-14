"""
Gerenciador de Perfis por Aplicativo (+ ADD APPLICATION)
Permite criar e alternar perfis personalizados para softwares instalados no Linux
"""

import os
import json
import glob
from pathlib import Path

PROFILES_DIR = Path(os.path.expanduser("~/.config/logi-options"))
PROFILES_FILE = PROFILES_DIR / "profiles.json"


class AppManager:
    @staticmethod
    def get_installed_apps():
        """Varre os arquivos .desktop do sistema e do usuário"""
        apps = []
        seen_names = set()
        paths = [
            "/usr/share/applications/*.desktop",
            os.path.expanduser("~/.local/share/applications/*.desktop")
        ]

        for pattern in paths:
            for filepath in glob.glob(pattern):
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if "NoDisplay=true" in content or "Type=Application" not in content:
                        continue

                    name = None
                    icon = None
                    exec_cmd = None

                    for line in content.splitlines():
                        if line.startswith("Name=") and not name:
                            name = line.split("=", 1)[1].strip()
                        elif line.startswith("Icon=") and not icon:
                            icon = line.split("=", 1)[1].strip()
                        elif line.startswith("Exec=") and not exec_cmd:
                            exec_cmd = line.split("=", 1)[1].strip().split()[0]

                    if name and name not in seen_names and not name.startswith("Logi Options"):
                        seen_names.add(name)
                        apps.append({
                            "name": name,
                            "icon": icon or "application-x-executable",
                            "exec": exec_cmd or name.lower(),
                            "file": filepath
                        })
                except Exception:
                    continue

        return sorted(apps, key=lambda x: x["name"].lower())

    @staticmethod
    def load_profiles():
        """Carrega os perfis configurados"""
        if not PROFILES_FILE.exists():
            return {
                "active_profile": "global",
                "apps": []
            }
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "active_profile": "global",
                "apps": []
            }

    @staticmethod
    def save_profiles(data):
        """Salva a lista de perfis do usuário"""
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
