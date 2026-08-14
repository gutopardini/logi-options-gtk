"""
Visualização de Gestos Oficial - UI Pro Max com Layout Clamped e Cards de Presets Limpos
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from ..widgets.dpad_widget import DPadWidget
from ..widgets.shortcut_recorder import ShortcutRecorderDialog
from ..backend.keycodes import PRESET_ACTIONS, format_keys_display


class GesturesView(Adw.PreferencesPage):
    def __init__(self, config_manager, on_config_changed_cb):
        super().__init__()
        self.config = config_manager
        self.on_changed = on_config_changed_cb
        self.current_direction = "Up"

        # 1. Bússola Visual de Gestos
        visual_group = Adw.PreferencesGroup(
            title="🖐️ Bússola de Gestos do Polegar (0xC3)",
            description="Mantenha o botão do polegar pressionado e mova o mouse em qualquer direção para disparar o atalho."
        )

        dpad_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        dpad_box.set_halign(Gtk.Align.CENTER)
        dpad_box.set_margin_top(8)
        dpad_box.set_margin_bottom(12)

        self.dpad = DPadWidget()
        self.dpad.connect('direction-selected', self.on_direction_changed)
        dpad_box.append(self.dpad)
        visual_group.add(dpad_box)
        self.add(visual_group)

        # 2. Configuração da Direção Selecionada
        self.direction_group = Adw.PreferencesGroup(
            title="🎯 Ação da Direção Selecionada",
            description="Personalize o atalho disparado ao mover o mouse na direção escolhida acima"
        )
        
        self.active_row = Adw.ActionRow(
            title="⬆️ Deslizar para CIMA",
            subtitle="Atalho Atual: Super"
        )
        self.record_btn = Gtk.Button(label="⌨️ Gravar Teclas...")
        self.record_btn.add_css_class("action-assign-btn")
        self.record_btn.set_valign(Gtk.Align.CENTER)
        self.record_btn.connect("clicked", self.open_recorder)
        self.active_row.add_suffix(self.record_btn)
        self.direction_group.add(self.active_row)
        self.add(self.direction_group)

        # 3. Presets Rápidos de Gestos (Cada um em uma linha estruturada)
        preset_group = Adw.PreferencesGroup(
            title="⚡ Presets Rápidos",
            description="Esquemas prontos de 4 direções para aplicar instantaneamente"
        )

        # Preset GNOME
        row_gnome = Adw.ActionRow(
            title="🖥️ Produtividade GNOME",
            subtitle="Cima/Baixo: Visão Geral | Esq/Dir: Áreas de Trabalho"
        )
        btn_g = Gtk.Button(label="Aplicar Preset")
        btn_g.add_css_class("action-assign-btn")
        btn_g.set_valign(Gtk.Align.CENTER)
        btn_g.connect("clicked", self.apply_preset_gnome)
        row_gnome.add_suffix(btn_g)
        preset_group.add(row_gnome)

        # Preset Mídia
        row_media = Adw.ActionRow(
            title="🎵 Controle Multimídia",
            subtitle="Cima/Baixo: Volume +/- | Esq/Dir: Faixa Anterior/Próxima"
        )
        btn_m = Gtk.Button(label="Aplicar Preset")
        btn_m.add_css_class("action-assign-btn")
        btn_m.set_valign(Gtk.Align.CENTER)
        btn_m.connect("clicked", self.apply_preset_media)
        row_media.add_suffix(btn_m)
        preset_group.add(row_media)

        # Preset Encaixe de Janelas
        row_snap = Adw.ActionRow(
            title="🪟 Encaixe de Janelas (Window Snapping)",
            subtitle="Cima: Maximizar | Baixo: Restaurar | Esq/Dir: Metade da Tela"
        )
        btn_s = Gtk.Button(label="Aplicar Preset")
        btn_s.add_css_class("action-assign-btn")
        btn_s.set_valign(Gtk.Align.CENTER)
        btn_s.connect("clicked", self.apply_preset_snap)
        row_snap.add_suffix(btn_s)
        preset_group.add(row_snap)

        self.add(preset_group)
        self.update_direction_ui()

    def on_direction_changed(self, widget, direction):
        self.current_direction = direction
        self.update_direction_ui()

    def get_keys_for_dir(self, direction):
        if direction == "Up":
            return self.config.gesture_up_keys
        elif direction == "Down":
            return self.config.gesture_down_keys
        elif direction == "Left":
            return self.config.gesture_left_keys
        elif direction == "Right":
            return self.config.gesture_right_keys
        return []

    def set_keys_for_dir(self, direction, keys):
        if direction == "Up":
            self.config.gesture_up_keys = keys
        elif direction == "Down":
            self.config.gesture_down_keys = keys
        elif direction == "Left":
            self.config.gesture_left_keys = keys
        elif direction == "Right":
            self.config.gesture_right_keys = keys
        
        self.update_direction_ui()
        if self.on_changed:
            self.on_changed()

    def update_direction_ui(self):
        dir_labels = {
            "Up": "⬆️ Deslizar para CIMA",
            "Down": "⬇️ Deslizar para BAIXO",
            "Left": "⬅️ Deslizar para ESQUERDA",
            "Right": "➡️ Deslizar para DIREITA"
        }
        name = dir_labels.get(self.current_direction, self.current_direction)
        keys = self.get_keys_for_dir(self.current_direction)
        self.active_row.set_title(name)
        self.active_row.set_subtitle(f"Atalho Atual: {format_keys_display(keys)}")

    def open_recorder(self, btn):
        root = self.get_root()
        current = self.get_keys_for_dir(self.current_direction)
        dlg = ShortcutRecorderDialog(
            root,
            current,
            lambda keys: self.set_keys_for_dir(self.current_direction, keys)
        )
        dlg.present()

    def apply_preset_gnome(self, btn):
        self.config.gesture_up_keys = ["KEY_LEFTMETA"]
        self.config.gesture_down_keys = ["KEY_LEFTMETA"]
        self.config.gesture_left_keys = ["KEY_LEFTMETA", "KEY_PAGEUP"]
        self.config.gesture_right_keys = ["KEY_LEFTMETA", "KEY_PAGEDOWN"]
        self.update_direction_ui()
        if self.on_changed:
            self.on_changed()

    def apply_preset_media(self, btn):
        self.config.gesture_up_keys = ["KEY_VOLUMEUP"]
        self.config.gesture_down_keys = ["KEY_VOLUMEDOWN"]
        self.config.gesture_left_keys = ["KEY_PREVIOUSSONG"]
        self.config.gesture_right_keys = ["KEY_NEXTSONG"]
        self.update_direction_ui()
        if self.on_changed:
            self.on_changed()

    def apply_preset_snap(self, btn):
        self.config.gesture_up_keys = ["KEY_LEFTMETA", "KEY_UP"]
        self.config.gesture_down_keys = ["KEY_LEFTMETA", "KEY_DOWN"]
        self.config.gesture_left_keys = ["KEY_LEFTMETA", "KEY_LEFT"]
        self.config.gesture_right_keys = ["KEY_LEFTMETA", "KEY_RIGHT"]
        self.update_direction_ui()
        if self.on_changed:
            self.on_changed()
