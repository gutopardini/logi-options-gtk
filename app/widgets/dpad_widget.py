"""
Widget de Visualização e Configuração em Cruz / D-Pad para Gestos
"""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject


class DPadWidget(Gtk.Box):
    __gsignals__ = {
        'direction-selected': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add_css_class("dpad-container")
        self.set_halign(Gtk.Align.CENTER)
        self.selected_dir = "Up"

        # Grid 3x3 para formar a Cruz / D-Pad
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_halign(Gtk.Align.CENTER)

        # Botão CIMA
        self.btn_up = Gtk.Button(label="⬆️ Deslizar p/ CIMA")
        self.btn_up.add_css_class("dpad-arrow-btn")
        self.btn_up.connect("clicked", lambda b: self.select_dir("Up"))
        self.grid.attach(self.btn_up, 1, 0, 1, 1)

        # Botão ESQUERDA
        self.btn_left = Gtk.Button(label="⬅️ Deslizar p/ ESQUERDA")
        self.btn_left.add_css_class("dpad-arrow-btn")
        self.btn_left.connect("clicked", lambda b: self.select_dir("Left"))
        self.grid.attach(self.btn_left, 0, 1, 1, 1)

        # Botão CENTRO (Apoio / Clique)
        self.btn_center = Gtk.Button(label="🔘 Apoio Polegar")
        self.btn_center.add_css_class("dpad-arrow-btn")
        self.btn_center.set_sensitive(False)
        self.grid.attach(self.btn_center, 1, 1, 1, 1)

        # Botão DIREITA
        self.btn_right = Gtk.Button(label="➡️ Deslizar p/ DIREITA")
        self.btn_right.add_css_class("dpad-arrow-btn")
        self.btn_right.connect("clicked", lambda b: self.select_dir("Right"))
        self.grid.attach(self.btn_right, 2, 1, 1, 1)

        # Botão BAIXO
        self.btn_down = Gtk.Button(label="⬇️ Deslizar p/ BAIXO")
        self.btn_down.add_css_class("dpad-arrow-btn")
        self.btn_down.connect("clicked", lambda b: self.select_dir("Down"))
        self.grid.attach(self.btn_down, 1, 2, 1, 1)

        self.append(self.grid)
        self.buttons = {
            "Up": self.btn_up,
            "Down": self.btn_down,
            "Left": self.btn_left,
            "Right": self.btn_right
        }
        self.select_dir("Up")

    def select_dir(self, direction):
        self.selected_dir = direction
        for d, b in self.buttons.items():
            if d == direction:
                b.add_css_class("active")
            else:
                b.remove_css_class("active")
        self.emit('direction-selected', direction)
