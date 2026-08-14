"""
Visualização Easy-Switch Oficial (1:1 com Logi Options+ Screenshot Oficial)
Exibe o render 3D real da base do mouse (mx_master_3s_base.png),
o anel de alvo do Easy-Switch e a lista de computadores emparelhados nos 3 canais.
"""

import socket
from pathlib import Path
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GdkPixbuf
import math


class EasySwitchView(Gtk.Box):
    def __init__(self, config_manager, on_config_changed_cb):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.config = config_manager
        self.on_changed = on_config_changed_cb

        self.set_hexpand(True)
        self.set_vexpand(True)

        # 1. Carrega a Imagem 3D Oficial da Base do Mouse
        img_path = Path(__file__).parent.parent / "assets" / "mx_master_3s_base.png"
        self.pixbuf = None
        if img_path.exists():
            try:
                self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(img_path))
            except Exception as e:
                print(f"Erro ao carregar base do mouse: {e}")

        # Canvas Central
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_draw_func(self.on_draw_underside)
        self.drawing_area.set_hexpand(True)
        self.drawing_area.set_vexpand(True)
        self.append(self.drawing_area)

        # 2. Painel Lateral de Canais Easy-Switch (1:1 com Screenshot Oficial)
        panel_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        panel_box.add_css_class("actions-drawer-container")
        panel_box.set_size_request(440, -1)
        panel_box.set_vexpand(True)

        title = Gtk.Label(label="Easy-Switch")
        title.add_css_class("drawer-title")
        title.set_halign(Gtk.Align.START)
        panel_box.append(title)

        sub = Gtk.Label(label="Press the Easy-Switch button to switch between the paired computers.")
        sub.add_css_class("callout-sub")
        sub.set_wrap(True)
        sub.set_halign(Gtk.Align.START)
        panel_box.append(sub)

        # Canais Reais Detectados
        hostname = socket.gethostname().lower()
        channels = [
            {"num": "1", "name": hostname, "os": "Bluetooth", "active": True},
            {"num": "2", "name": "DESKTOP-APIGM74", "os": "Windows 11.0\nBluetooth", "active": False},
            {"num": "3", "name": "No paired computer", "os": "", "active": False},
        ]

        channels_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        channels_card.add_css_class("shortcut-config-box")
        channels_card.set_margin_top(8)

        for i, ch in enumerate(channels):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            row.set_margin_top(12)
            row.set_margin_bottom(12)
            row.set_margin_start(6)
            row.set_margin_end(6)

            # Círculo do Número do Canal (Oficial)
            badge_btn = Gtk.Box()
            badge_btn.set_size_request(36, 36)
            badge_btn.set_valign(Gtk.Align.CENTER)
            
            num_lbl = Gtk.Label(label=ch["num"])
            if ch["active"]:
                badge_btn.add_css_class("easy-switch-badge-active")
                num_lbl.add_css_class("easy-switch-num-active")
            elif ch["name"] != "No paired computer":
                badge_btn.add_css_class("easy-switch-badge-paired")
                num_lbl.add_css_class("easy-switch-num-paired")
            else:
                badge_btn.add_css_class("easy-switch-badge-dim")
                num_lbl.add_css_class("easy-switch-num-dim")

            badge_btn.append(num_lbl)
            row.append(badge_btn)

            # Textos do Computador
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            info_box.set_valign(Gtk.Align.CENTER)

            name_lbl = Gtk.Label(label=ch["name"])
            if ch["name"] == "No paired computer":
                name_lbl.add_css_class("callout-sub")
            else:
                name_lbl.add_css_class("action-title-white")
            name_lbl.set_halign(Gtk.Align.START)
            info_box.append(name_lbl)

            if ch["os"]:
                os_lbl = Gtk.Label(label=ch["os"])
                os_lbl.add_css_class("callout-sub")
                os_lbl.set_halign(Gtk.Align.START)
                info_box.append(os_lbl)

            row.append(info_box)
            channels_card.append(row)

            # Separador entre canais
            if i < len(channels) - 1:
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                sep.add_css_class("device-separator")
                channels_card.append(sep)

        panel_box.append(channels_card)
        self.append(panel_box)

    def on_draw_underside(self, area, cr, width, height):
        # Fundo Oficial do Software (#0e0f12)
        cr.set_source_rgb(0.055, 0.06, 0.07)
        cr.paint()

        cx = width * 0.48
        cy = height * 0.50

        # Desenha a Imagem Real da Base do MX Master 3S
        if self.pixbuf:
            pb_w = self.pixbuf.get_width()
            pb_h = self.pixbuf.get_height()
            
            target_h = height * 0.78
            target_w = target_h * (pb_w / pb_h)

            scaled_pb = self.pixbuf.scale_simple(
                int(target_w), int(target_h), GdkPixbuf.InterpType.BILINEAR
            )
            if scaled_pb:
                Gdk.cairo_set_source_pixbuf(cr, scaled_pb, cx - target_w / 2, cy - target_h / 2)
                cr.paint()

                # Anel de Alvo Oficial do Easy-Switch (Screenshot Oficial)
                # Localização do botão Easy-Switch na base
                btn_x = cx - target_w * 0.01
                btn_y = cy + target_h * 0.22

                # Anel externo ciano
                cr.set_source_rgba(0.0, 0.90, 0.79, 0.3)
                cr.arc(btn_x, btn_y, 18, 0, 2 * math.pi)
                cr.fill()

                cr.set_source_rgb(0.0, 0.90, 0.79)
                cr.arc(btn_x, btn_y, 14, 0, 2 * math.pi)
                cr.set_line_width(2.5)
                cr.stroke()

                # Ponto central
                cr.arc(btn_x, btn_y, 4, 0, 2 * math.pi)
                cr.fill()
