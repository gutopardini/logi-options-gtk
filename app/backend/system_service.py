"""
Serviços de Integração de Sistema: UPower (Bateria e Reconexão), Systemd (Logid) e Polkit (Aplicação)
"""

import subprocess
import os
from pathlib import Path


class SystemService:
    @staticmethod
    def get_battery_info():
        """
        Obtém o nível de bateria e status do mouse via UPower com auto-recuperação
        ao desconectar e reconectar.
        """
        try:
            # Lista dispositivos UPower
            out = subprocess.check_output(["upower", "-e"], text=True, stderr=subprocess.DEVNULL)
            device_paths = [
                p.strip() for p in out.splitlines()
                if ("mouse" in p.lower() or "hidpp" in p.lower() or "logitech" in p.lower())
                and "battery_bat" not in p.lower()
                and "line_power" not in p.lower()
                and "displaydevice" not in p.lower()
            ]

            for path in device_paths:
                try:
                    info_out = subprocess.check_output(["upower", "-i", path], text=True, stderr=subprocess.DEVNULL)
                    percentage = None
                    state = "discharging"
                    model = "MX Master 3S"

                    for line in info_out.splitlines():
                        line = line.strip()
                        if line.startswith("percentage:"):
                            percentage = line.split(":", 1)[1].strip()
                        elif line.startswith("state:"):
                            state = line.split(":", 1)[1].strip().lower()
                        elif line.startswith("model:"):
                            model = line.split(":", 1)[1].strip()

                    if percentage:
                        is_charging = ("charging" in state and "discharging" not in state)
                        return {
                            "connected": True,
                            "percentage": percentage,
                            "state": state.capitalize(),
                            "model": model,
                            "is_charging": is_charging
                        }
                except Exception:
                    continue

            # Fallback direto em /sys/class/power_supply
            sys_ps = Path("/sys/class/power_supply")
            if sys_ps.exists():
                for p in sys_ps.iterdir():
                    if "hidpp" in p.name.lower() or "mouse" in p.name.lower():
                        cap_file = p / "capacity"
                        status_file = p / "status"
                        if cap_file.exists():
                            try:
                                cap = cap_file.read_text().strip()
                                st = status_file.read_text().strip() if status_file.exists() else "Discharging"
                                if cap.isdigit():
                                    return {
                                        "connected": True,
                                        "percentage": f"{cap}%",
                                        "state": st.capitalize(),
                                        "model": "MX Master 3S",
                                        "is_charging": ("charging" in st.lower() and "discharging" not in st.lower())
                                    }
                            except Exception:
                                pass

            # Dispositivo desconectado
            return {
                "connected": False,
                "percentage": None,
                "state": "Disconnected",
                "model": "MX Master 3S",
                "is_charging": False
            }
        except Exception:
            return {
                "connected": False,
                "percentage": None,
                "state": "Disconnected",
                "model": "MX Master 3S",
                "is_charging": False
            }

    @staticmethod
    def is_logid_running():
        """Verifica se o serviço systemd do logid está ativo"""
        try:
            res = subprocess.run(["systemctl", "is-active", "logid"], capture_output=True, text=True)
            return res.stdout.strip() == "active"
        except Exception:
            return False

    @staticmethod
    def apply_config(cfg_content: str):
        """
        Salva em ~/Documents/logid.cfg e aplica em /etc/logid.cfg com reinício do serviço
        via pkexec para exibir o diálogo nativo do GNOME.
        """
        user_cfg = Path(os.path.expanduser("~/Documents/logid.cfg"))
        with open(user_cfg, "w", encoding="utf-8") as f:
            f.write(cfg_content)

        cmd = f"cp {user_cfg} /etc/logid.cfg && systemctl restart logid"
        
        try:
            result = subprocess.run(
                ["pkexec", "bash", "-c", cmd],
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stderr or result.stdout
        except Exception as e:
            return False, str(e)
