"""
Visualização de Gestos Oficial - UI Pro Max com Layout Clamped e Cards de Presets Limpos
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from ..i18n import _
from ..widgets.dpad_widget import DPadWidget
from ..widgets.shortcut_recorder import ShortcutRecorderDialog
from ..backend.keycodes import format_keys_display


class GesturesView(Adw.PreferencesPage):
    def __init__(self, config_manager, on_config_changed_cb):
        super().__init__()
        self.config = config_manager
        self.on_changed = on_config_changed_cb
        self.current_direction = "Up"

        # 1. Bússola Visual de Gestos
        visual_group = Adw.PreferencesGroup(
            title=_("🖐️ Thumb Gesture Compass (0xC3)"),
            description=_("Hold down the thumb button and move the mouse in any direction to trigger the shortcut.")
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
            title=_("🎯 Selected Direction Action"),
            description=_("Customize the shortcut triggered when moving the mouse in the direction chosen above")
        )
        
        self.active_row = Adw.ActionRow(
            title=_("⬆️ Swipe UP"),
            subtitle=_("Current Shortcut: Super")
        )
        self.record_btn = Gtk.Button(label=_("⌨️ Record Keys..."))
        self.record_btn.add_css_class("action-assign-btn")
        self.record_btn.set_valign(Gtk.Align.CENTER)
        self.record_btn.connect("clicked", self.open_recorder)
        self.active_row.add_suffix(self.record_btn)
        self.direction_group.add(self.active_row)
        self.add(self.direction_group)

        # 3. Presets Rápidos de Gestos (Cada um em uma linha estruturada)
        preset_group = Adw.PreferencesGroup(
            title=_("⚡ Quick Presets"),
            description=_("Ready-made 4-direction schemes to apply instantly")
        )

        # Preset GNOME
        row_gnome = Adw.ActionRow(
            title=_("🖥️ GNOME Productivity"),
            subtitle=_("Up/Down: Overview | Left/Right: Workspaces")
        )
        btn_g = Gtk.Button(label=_("Apply Preset"))
        btn_g.add_css_class("action-assign-btn")
        btn_g.set_valign(Gtk.Align.CENTER)
        btn_g.connect("clicked", self.apply_preset_gnome)
        row_gnome.add_suffix(btn_g)
        preset_group.add(row_gnome)

        # Preset Mídia
        row_media = Adw.ActionRow(
            title=_("🎵 Media Controls"),
            subtitle=_("Up/Down: Volume +/- | Left/Right: Prev/Next Track")
        )
        btn_m = Gtk.Button(label=_("Apply Preset"))
        btn_m.add_css_class("action-assign-btn")
        btn_m.set_valign(Gtk.Align.CENTER)
        btn_m.connect("clicked", self.apply_preset_media)
        row_media.add_suffix(btn_m)
        preset_group.add(row_media)

        # Preset Encaixe de Janelas
        row_snap = Adw.ActionRow(
            title=_("🪟 Window Snapping"),
            subtitle=_("Up: Maximize | Down: Restore | Left/Right: Split Screen")
        )
        btn_s = Gtk.Button(label=_("Apply Preset"))
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
            "Up": _("⬆️ Swipe UP"),
            "Down": _("⬇️ Swipe DOWN"),
            "Left": _("⬅️ Swipe LEFT"),
            "Right": _("➡️ Swipe RIGHT")
        }
        name = dir_labels.get(self.current_direction, self.current_direction)
        keys = self.get_keys_for_dir(self.current_direction)
        self.active_row.set_title(name)
        keys_str = format_keys_display(keys)
        self.active_row.set_subtitle(_("Current Shortcut: {keys}").format(keys=keys_str))

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
