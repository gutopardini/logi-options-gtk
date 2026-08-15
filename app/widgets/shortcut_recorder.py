"""
Diálogo Gravador Interativo de Teclas e Atalhos para GTK4
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk

from ..i18n import _
from ..backend.keycodes import KEY_MAP, REV_KEY_MAP, format_keys_display

# Mapeamento de Gdk.Keyval para nomes evdev KEY_*
GDK_TO_EVDEV = {
    Gdk.KEY_Control_L: "KEY_LEFTCTRL",
    Gdk.KEY_Control_R: "KEY_RIGHTCTRL",
    Gdk.KEY_Shift_L: "KEY_LEFTSHIFT",
    Gdk.KEY_Shift_R: "KEY_RIGHTSHIFT",
    Gdk.KEY_Alt_L: "KEY_LEFTALT",
    Gdk.KEY_Alt_R: "KEY_RIGHTALT",
    Gdk.KEY_Super_L: "KEY_LEFTMETA",
    Gdk.KEY_Super_R: "KEY_RIGHTMETA",
    Gdk.KEY_Page_Up: "KEY_PAGEUP",
    Gdk.KEY_Page_Down: "KEY_PAGEDOWN",
    Gdk.KEY_Home: "KEY_HOME",
    Gdk.KEY_End: "KEY_END",
    Gdk.KEY_Up: "KEY_UP",
    Gdk.KEY_Down: "KEY_DOWN",
    Gdk.KEY_Left: "KEY_LEFT",
    Gdk.KEY_Right: "KEY_RIGHT",
    Gdk.KEY_space: "KEY_SPACE",
    Gdk.KEY_Return: "KEY_ENTER",
    Gdk.KEY_Escape: "KEY_ESC",
    Gdk.KEY_Tab: "KEY_TAB",
    Gdk.KEY_BackSpace: "KEY_BACKSPACE",
    Gdk.KEY_Delete: "KEY_DELETE",
    Gdk.KEY_Print: "KEY_PRINT",
    Gdk.KEY_AudioPlay: "KEY_PLAYPAUSE",
    Gdk.KEY_AudioMute: "KEY_MUTE",
    Gdk.KEY_AudioRaiseVolume: "KEY_VOLUMEUP",
    Gdk.KEY_AudioLowerVolume: "KEY_VOLUMEDOWN",
    Gdk.KEY_AudioNext: "KEY_NEXTSONG",
    Gdk.KEY_AudioPrev: "KEY_PREVIOUSSONG",
}

# Preenche F1-F12 e A-Z
for i in range(1, 13):
    gdk_key = getattr(Gdk, f"KEY_F{i}", None)
    if gdk_key:
        GDK_TO_EVDEV[gdk_key] = f"KEY_F{i}"


class ShortcutRecorderDialog(Adw.Window):
    def __init__(self, parent_window, current_keys, on_saved_callback):
        super().__init__(transient_for=parent_window, modal=True)
        self.set_title(_("Record Keyboard Shortcut"))
        self.set_default_size(380, 260)
        self.on_saved_callback = on_saved_callback
        self.recorded_keys = list(current_keys) if current_keys else []

        # Container Principal
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)

        # Título e Instrução
        title_label = Gtk.Label(label=_("Press key combination"))
        title_label.add_css_class("title-3")
        box.append(title_label)

        sub_label = Gtk.Label(label=_("E.g., Super + Shift + PageDown or Ctrl + Alt + T"))
        sub_label.add_css_class("dim-label")
        box.append(sub_label)

        # Caixa de Visualização das Teclas
        self.display_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.display_box.set_halign(Gtk.Align.CENTER)
        self.display_box.set_valign(Gtk.Align.CENTER)
        self.display_box.set_margin_top(12)
        self.display_box.set_margin_bottom(12)

        self.key_label = Gtk.Label(label=format_keys_display(self.recorded_keys))
        self.key_label.add_css_class("title-2")
        self.display_box.append(self.key_label)
        box.append(self.display_box)

        # Botões de Ação
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)

        clear_btn = Gtk.Button(label=_("Clear"))
        clear_btn.connect("clicked", self.on_clear)
        btn_box.append(clear_btn)

        cancel_btn = Gtk.Button(label=_("Cancel"))
        cancel_btn.connect("clicked", lambda b: self.close())
        btn_box.append(cancel_btn)

        save_btn = Gtk.Button(label=_("Save Shortcut"))
        save_btn.add_css_class("suggested-action")
        save_btn.connect("clicked", self.on_save)
        btn_box.append(save_btn)

        box.append(btn_box)
        self.set_content(box)

        # Captura de Eventos de Tecla
        key_ctrl = Gtk.EventControllerKey()
        key_ctrl.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_ctrl)

    def on_key_pressed(self, controller, keyval, keycode, state):
        evdev_key = None
        
        # Converte keyval para EVDEV
        if keyval in GDK_TO_EVDEV:
            evdev_key = GDK_TO_EVDEV[keyval]
        else:
            # Tenta pegar caractere normal (A-Z, 0-9)
            unicode_char = Gdk.keyval_to_unicode(keyval)
            if unicode_char and chr(unicode_char).isalnum():
                evdev_key = f"KEY_{chr(unicode_char).upper()}"

        if not evdev_key:
            return Gdk.EVENT_PROPAGATE

        # Adiciona modificadores ativos
        active_keys = []
        if state & Gdk.ModifierType.SUPER_MASK and evdev_key != "KEY_LEFTMETA":
            active_keys.append("KEY_LEFTMETA")
        if state & Gdk.ModifierType.CONTROL_MASK and evdev_key != "KEY_LEFTCTRL":
            active_keys.append("KEY_LEFTCTRL")
        if state & Gdk.ModifierType.ALT_MASK and evdev_key != "KEY_LEFTALT":
            active_keys.append("KEY_LEFTALT")
        if state & Gdk.ModifierType.SHIFT_MASK and evdev_key != "KEY_LEFTSHIFT":
            active_keys.append("KEY_LEFTSHIFT")

        if evdev_key not in active_keys:
            active_keys.append(evdev_key)

        self.recorded_keys = active_keys
        self.key_label.set_label(format_keys_display(self.recorded_keys))
        return Gdk.EVENT_STOP

    def on_clear(self, btn):
        self.recorded_keys = []
        self.key_label.set_label(_("None"))

    def on_save(self, btn):
        if self.on_saved_callback:
            self.on_saved_callback(self.recorded_keys)
        self.close()
