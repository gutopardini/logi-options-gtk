"""
Visualização de Botões e Actions Drawer Oficial (1:1 com Logi Options+ Oficial)
Mapeamento cirúrgico de 100% das ações oficiais da Logitech baseadas em todas as capturas de tela:
- Wheel (Middle button)
- Top Button (Shift wheel mode)
- Forward / Back Buttons
- Button Gestures (6 Presets completos + Custom)
- Accordion Colapsável de OTHER ACTIONS (Dicionário Alfabético Completo)
- Gravador interativo de atalhos para todos os botões e direções do Thumbwheel.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk

from ..i18n import _
from ..widgets.mouse_canvas import MouseCanvas
from ..backend.keycodes import format_keys_display


def get_unified_other_actions():
    return [
        {"name": _("Action center"), "keys": ["KEY_LEFTMETA", "KEY_A"], "type": "action"},
        {"name": _("Back"), "keys": ["KEY_BACK"], "type": "action"},
        {"name": _("Brightness down"), "keys": ["KEY_BRIGHTNESSDOWN"], "type": "action"},
        {"name": _("Brightness up"), "keys": ["KEY_BRIGHTNESSUP"], "type": "action"},
        {"name": _("Calculator"), "keys": ["KEY_CALC"], "type": "action"},
        {"name": _("Close window"), "keys": ["KEY_LEFTALT", "KEY_F4"], "type": "action"},
        {"name": _("Copy"), "keys": ["KEY_LEFTCTRL", "KEY_C"], "type": "action"},
        {"name": _("Cut"), "keys": ["KEY_LEFTCTRL", "KEY_X"], "type": "action"},
        {"name": _("Desktop left"), "keys": ["KEY_LEFTMETA", "KEY_PAGEUP"], "type": "action"},
        {"name": _("Desktop right"), "keys": ["KEY_LEFTMETA", "KEY_PAGEDOWN"], "type": "action"},
        {"name": _("Do nothing"), "keys": [], "type": "action"},
        {"name": _("Emoji menu"), "keys": ["KEY_LEFTMETA", "KEY_DOT"], "type": "action"},
        {"name": _("Forward"), "keys": ["KEY_FORWARD"], "type": "action"},
        {"name": _("Input language"), "keys": ["KEY_LEFTMETA", "KEY_SPACE"], "type": "action"},
        {"name": _("Lock"), "keys": ["KEY_LEFTMETA", "KEY_L"], "type": "action"},
        {"name": _("Maximize window"), "keys": ["KEY_LEFTMETA", "KEY_UP"], "type": "action"},
        {"name": _("Minimize window"), "keys": ["KEY_LEFTMETA", "KEY_DOWN"], "type": "action"},
        {"name": _("Mute/Unmute speaker"), "keys": ["KEY_MUTE"], "type": "action"},
        {"name": _("New browser tab"), "keys": ["KEY_LEFTCTRL", "KEY_T"], "type": "action"},
        {"name": _("Next"), "keys": ["KEY_NEXTSONG"], "type": "action"},
        {"name": _("Paste"), "keys": ["KEY_LEFTCTRL", "KEY_V"], "type": "action"},
        {"name": _("Play/Pause"), "keys": ["KEY_PLAYPAUSE"], "type": "action"},
        {"name": _("Previous"), "keys": ["KEY_PREVIOUSSONG"], "type": "action"},
        {"name": _("Print screen"), "keys": ["KEY_PRINT"], "type": "action"},
        {"name": _("Redo"), "keys": ["KEY_LEFTCTRL", "KEY_Y"], "type": "action"},
        {"name": _("Right Ctrl"), "keys": ["KEY_RIGHTCTRL"], "type": "action"},
        {"name": _("Screen capture"), "keys": ["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_S"], "type": "action"},
        {"name": _("Screen snip"), "keys": ["KEY_PRINT"], "type": "action"},
        {"name": _("Shift wheel mode"), "keys": [], "type": "toggle_smartshift"},
        {"name": _("Show/hide desktop"), "keys": ["KEY_LEFTMETA", "KEY_D"], "type": "action"},
        {"name": _("Switch application"), "keys": ["KEY_LEFTALT", "KEY_TAB"], "type": "action"},
        {"name": _("Task view"), "keys": ["KEY_LEFTMETA"], "type": "action"},
        {"name": _("Undo"), "keys": ["KEY_LEFTCTRL", "KEY_Z"], "type": "action"},
        {"name": _("Volume down"), "keys": ["KEY_VOLUMEDOWN"], "type": "action"},
        {"name": _("Volume up"), "keys": ["KEY_VOLUMEUP"], "type": "action"},
        {"name": _("Zoom in"), "keys": ["KEY_LEFTCTRL", "KEY_EQUAL"], "type": "action"},
        {"name": _("Zoom out"), "keys": ["KEY_LEFTCTRL", "KEY_MINUS"], "type": "action"},
    ]


def get_gesture_presets_map():
    return {
        0: {
            "name": _("Virtual desktops"),
            "up": ["KEY_LEFTMETA"],
            "down": ["KEY_LEFTMETA", "KEY_D"],
            "left": ["KEY_LEFTMETA", "KEY_PAGEUP"],
            "right": ["KEY_LEFTMETA", "KEY_PAGEDOWN"],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Desktop left")),
                (_("→ HOLD + MOVE RIGHT"), _("Desktop right")),
                (_("↑ HOLD + MOVE UP"), _("Start menu")),
                (_("↓ HOLD + MOVE DOWN"), _("Show/hide desktop")),
                (_("○ CLICK"), _("Task view")),
            ]
        },
        1: {
            "name": _("Media controls"),
            "up": ["KEY_VOLUMEUP"],
            "down": ["KEY_VOLUMEDOWN"],
            "left": ["KEY_PREVIOUSSONG"],
            "right": ["KEY_NEXTSONG"],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Previous")),
                (_("→ HOLD + MOVE RIGHT"), _("Next")),
                (_("↑ HOLD + MOVE UP"), _("Volume up")),
                (_("↓ HOLD + MOVE DOWN"), _("Volume down")),
                (_("○ CLICK"), _("Play/Pause")),
            ]
        },
        2: {
            "name": _("Windows management"),
            "up": ["KEY_LEFTMETA", "KEY_UP"],
            "down": ["KEY_LEFTMETA", "KEY_D"],
            "left": ["KEY_LEFTMETA", "KEY_LEFT"],
            "right": ["KEY_LEFTMETA", "KEY_RIGHT"],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Snap left")),
                (_("→ HOLD + MOVE RIGHT"), _("Snap right")),
                (_("↑ HOLD + MOVE UP"), _("Maximize window")),
                (_("↓ HOLD + MOVE DOWN"), _("Show/hide desktop")),
                (_("○ CLICK"), _("Switch application")),
            ]
        },
        3: {
            "name": _("App navigation"),
            "up": ["KEY_LEFTMETA"],
            "down": ["KEY_LEFTMETA", "KEY_D"],
            "left": ["KEY_LEFTALT", "KEY_LEFTSHIFT", "KEY_TAB"],
            "right": ["KEY_LEFTALT", "KEY_TAB"],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Switch application")),
                (_("→ HOLD + MOVE RIGHT"), _("Switch application")),
                (_("↑ HOLD + MOVE UP"), _("Start menu")),
                (_("↓ HOLD + MOVE DOWN"), _("Show/hide desktop")),
                (_("○ CLICK"), _("Switch application")),
            ]
        },
        4: {
            "name": _("Pan"),
            "up": ["KEY_UP"],
            "down": ["KEY_DOWN"],
            "left": ["KEY_LEFT"],
            "right": ["KEY_RIGHT"],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Pan left")),
                (_("→ HOLD + MOVE RIGHT"), _("Pan right")),
                (_("↑ HOLD + MOVE UP"), _("Pan up")),
                (_("↓ HOLD + MOVE DOWN"), _("Pan down")),
                (_("○ CLICK"), _("Middle button")),
            ]
        },
        5: {
            "name": _("Arrange windows"),
            "up": ["KEY_LEFTMETA", "KEY_UP"],
            "down": ["KEY_LEFTMETA", "KEY_DOWN"],
            "left": ["KEY_LEFTMETA", "KEY_LEFT"],
            "right": ["KEY_LEFTMETA", "KEY_RIGHT"],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Snap left")),
                (_("→ HOLD + MOVE RIGHT"), _("Snap right")),
                (_("↑ HOLD + MOVE UP"), _("Maximize window")),
                (_("↓ HOLD + MOVE DOWN"), _("Minimize window")),
                (_("○ CLICK"), _("Switch application")),
            ]
        },
        6: {
            "name": _("Custom"),
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "rows": [
                (_("← HOLD + MOVE LEFT"), _("Do nothing")),
                (_("→ HOLD + MOVE RIGHT"), _("Do nothing")),
                (_("↑ HOLD + MOVE UP"), _("Do nothing")),
                (_("↓ HOLD + MOVE DOWN"), _("Do nothing")),
                (_("○ CLICK"), _("Do nothing")),
            ]
        }
    }


class ButtonsView(Gtk.Box):
    def __init__(self, config_manager, on_config_changed_cb, on_drawer_toggle_cb=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.config = config_manager
        self.on_changed = on_config_changed_cb
        self.on_drawer_toggle = on_drawer_toggle_cb
        self.current_pin = None
        self.search_filter = ""
        self.active_recording_target = None
        self.thumb_mode = "default"
        self.other_actions_expanded = False
        self.gesture_preset_index = 0

        self.set_hexpand(True)
        self.set_vexpand(True)

        # 1. Canvas Central com Render 3D Oficial e Callouts
        self.mouse_canvas = MouseCanvas(self.config)
        self.mouse_canvas.connect('pin-selected', self.on_pin_selected)
        self.append(self.mouse_canvas)

        # 2. Drawer Lateral Oficial de Ações
        self.drawer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        self.drawer_box.add_css_class("actions-drawer-container")
        self.drawer_box.set_size_request(400, -1)
        self.drawer_box.set_vexpand(True)
        self.drawer_box.set_visible(False)

        # Header do Drawer com Título e Botão Fechar
        d_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.drawer_title = Gtk.Label(label=_("Actions"))
        self.drawer_title.add_css_class("drawer-title")
        self.drawer_title.set_halign(Gtk.Align.START)
        d_header.append(self.drawer_title)

        sp = Gtk.Box()
        sp.set_hexpand(True)
        d_header.append(sp)

        close_d_btn = Gtk.Button(label="✕")
        close_d_btn.add_css_class("close-nav-btn")
        close_d_btn.set_tooltip_text(_("Close and return to overview"))
        close_d_btn.connect("clicked", lambda b: self.close_drawer())
        d_header.append(close_d_btn)
        self.drawer_box.append(d_header)

        # Campo de Busca Oficial
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.add_css_class("official-search-entry")
        self.search_entry.set_placeholder_text(_("Search"))
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.drawer_box.append(self.search_entry)

        # Container Rolável de Ações com Altura Mínima Garantida
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True)
        self.scroll.set_hexpand(True)
        self.scroll.set_min_content_height(480)
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.content_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.content_container.set_vexpand(True)
        self.content_container.set_hexpand(True)
        self.scroll.set_child(self.content_container)
        self.drawer_box.append(self.scroll)

        self.append(self.drawer_box)

        # Controlador de Teclas Global para Gravação
        key_ctrl = Gtk.EventControllerKey()
        key_ctrl.connect("key-pressed", self.on_key_pressed)
        self.add_controller(key_ctrl)

    def on_pin_selected(self, canvas, pin_id):
        self.current_pin = pin_id
        self.active_recording_target = None
        self.update_drawer()
        self.drawer_box.set_visible(True)
        if self.on_drawer_toggle:
            self.on_drawer_toggle(True)

    def close_drawer(self):
        self.current_pin = None
        self.active_recording_target = None
        self.drawer_box.set_visible(False)
        if self.on_drawer_toggle:
            self.on_drawer_toggle(False)
        self.mouse_canvas.select_pin(None)

    def on_search_changed(self, entry):
        self.search_filter = entry.get_text().strip().lower()
        self.update_drawer()

    def toggle_other_actions(self, btn):
        self.other_actions_expanded = not self.other_actions_expanded
        self.update_drawer()

    def update_drawer(self):
        if not self.current_pin:
            return

        while self.content_container.get_first_child():
            self.content_container.remove(self.content_container.get_first_child())

        # -------------------------------------------------------------
        # 1. Seção: RECOMMENDED (Oficial dos Prints para cada botão)
        # -------------------------------------------------------------
        cat_lbl = Gtk.Label(label=_("RECOMMENDED"))
        cat_lbl.add_css_class("category-header-label")
        cat_lbl.set_halign(Gtk.Align.START)
        self.content_container.append(cat_lbl)

        recommended_items = []

        if self.current_pin == "thumbwheel":
            recommended_items = [
                {"name": _("Horizontal scroll"), "keys": [], "type": "thumb_default"},
                {"name": _("Zoom in/out"), "keys": ["KEY_LEFTCTRL", "KEY_EQUAL"], "type": "thumb_zoom"},
                {"name": _("Volume up/down"), "keys": ["KEY_VOLUMEUP"], "type": "thumb_volume"},
                {"name": _("Navigate between tabs"), "keys": ["KEY_LEFTCTRL", "KEY_PAGEDOWN"], "type": "thumb_tabs"},
                {"name": _("Keyboard shortcut"), "keys": None, "type": "thumb_shortcut"},
            ]
        elif self.current_pin == "btn_middle":
            recommended_items = [
                {"name": _("Middle button"), "keys": [], "type": "middle_default"},
                {"name": _("Shift wheel mode"), "keys": [], "type": "toggle_smartshift"},
                {"name": _("Task view"), "keys": ["KEY_LEFTMETA"], "type": "action"},
                {"name": _("Show/hide desktop"), "keys": ["KEY_LEFTMETA", "KEY_D"], "type": "action"},
                {"name": _("Gestures"), "keys": None, "type": "gestures"},
                {"name": _("Keyboard shortcut"), "keys": None, "type": "single_shortcut"},
            ]
        elif self.current_pin == "btn_top":
            recommended_items = [
                {"name": _("Shift wheel mode"), "keys": [], "type": "toggle_smartshift"},
                {"name": _("Task view"), "keys": ["KEY_LEFTMETA"], "type": "action"},
                {"name": _("Middle button"), "keys": ["BTN_MIDDLE"], "type": "action"},
                {"name": _("Gestures"), "keys": None, "type": "gestures"},
                {"name": _("Screen capture"), "keys": ["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_S"], "type": "action"},
                {"name": _("Print screen"), "keys": ["KEY_PRINT"], "type": "action"},
                {"name": _("Keyboard shortcut"), "keys": None, "type": "single_shortcut"},
            ]
        elif self.current_pin == "btn_forward":
            recommended_items = [
                {"name": _("Forward"), "keys": ["KEY_FORWARD"], "type": "action"},
                {"name": _("Paste"), "keys": ["KEY_LEFTCTRL", "KEY_V"], "type": "action"},
                {"name": _("Volume up"), "keys": ["KEY_VOLUMEUP"], "type": "action"},
                {"name": _("Redo"), "keys": ["KEY_LEFTCTRL", "KEY_Y"], "type": "action"},
                {"name": _("Keyboard shortcut"), "keys": None, "type": "single_shortcut"},
            ]
        elif self.current_pin == "btn_back":
            recommended_items = [
                {"name": _("Back"), "keys": ["KEY_BACK"], "type": "action"},
                {"name": _("Copy"), "keys": ["KEY_LEFTCTRL", "KEY_C"], "type": "action"},
                {"name": _("Volume down"), "keys": ["KEY_VOLUMEDOWN"], "type": "action"},
                {"name": _("Undo"), "keys": ["KEY_LEFTCTRL", "KEY_Z"], "type": "action"},
                {"name": _("Keyboard shortcut"), "keys": None, "type": "single_shortcut"},
            ]
        elif self.current_pin == "btn_gesture":
            recommended_items = [
                {"name": _("Gestures"), "keys": None, "type": "gestures"},
                {"name": _("Task view"), "keys": ["KEY_LEFTMETA"], "type": "action"},
                {"name": _("Show/hide desktop"), "keys": ["KEY_LEFTMETA", "KEY_D"], "type": "action"},
                {"name": _("Screen capture"), "keys": ["KEY_LEFTMETA", "KEY_LEFTSHIFT", "KEY_S"], "type": "action"},
                {"name": _("Print screen"), "keys": ["KEY_PRINT"], "type": "action"},
                {"name": _("Switch application"), "keys": ["KEY_LEFTALT", "KEY_TAB"], "type": "action"},
                {"name": _("Keyboard shortcut"), "keys": None, "type": "single_shortcut"},
            ]

        for item in recommended_items:
            if self.search_filter and self.search_filter not in item["name"].lower():
                continue
            self.append_action_row(item)

        # -------------------------------------------------------------
        # 2. Seção: OTHER ACTIONS (Accordion Colapsável Oficial)
        # -------------------------------------------------------------
        accordion_btn = Gtk.Button()
        accordion_btn.add_css_class("accordion-header-btn")

        acc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        acc_lbl = Gtk.Label(label=_("OTHER ACTIONS"))
        acc_lbl.add_css_class("accordion-header-title")
        acc_lbl.set_halign(Gtk.Align.START)
        acc_box.append(acc_lbl)

        sp_acc = Gtk.Box()
        sp_acc.set_hexpand(True)
        acc_box.append(sp_acc)

        is_expanded = self.other_actions_expanded or bool(self.search_filter)
        chevron_lbl = Gtk.Label(label="⌃" if is_expanded else "⌵")
        chevron_lbl.add_css_class("accordion-chevron")
        acc_box.append(chevron_lbl)

        accordion_btn.set_child(acc_box)
        accordion_btn.connect("clicked", self.toggle_other_actions)
        self.content_container.append(accordion_btn)

        if is_expanded:
            for item in get_unified_other_actions():
                if self.search_filter and self.search_filter not in item["name"].lower():
                    continue
                self.append_action_row(item)

    def append_action_row(self, item):
        btn = Gtk.Button()
        btn.add_css_class("action-radio-row")

        is_selected = False
        itype = item.get("type")

        # Verifica seleção
        if itype == "toggle_smartshift":
            if self.current_pin == "btn_top" and self.config.btn_top_action == "ToggleSmartShift":
                is_selected = True
            elif self.current_pin == "btn_middle" and self.config.btn_middle_action == "ToggleSmartShift":
                is_selected = True
        elif itype == "middle_default":
            if self.current_pin == "btn_middle" and self.config.btn_middle_action == "default" and not self.config.btn_middle_keys:
                is_selected = True
        elif itype == "thumb_shortcut" and self.current_pin == "thumbwheel":
            if self.thumb_mode == "shortcut":
                is_selected = True
            elif self.config.thumbwheel_divert:
                is_preset = self.config.thumbwheel_right_keys in [
                    ["KEY_LEFTCTRL", "KEY_EQUAL"],
                    ["KEY_VOLUMEUP"],
                    ["KEY_LEFTCTRL", "KEY_PAGEDOWN"]
                ]
                if not is_preset:
                    is_selected = True
        elif itype == "single_shortcut" and self.config.gesture_mode == "keypress" and self.current_pin == "btn_gesture":
            is_selected = True
        elif itype == "single_shortcut" and self.thumb_mode == "single_shortcut":
            is_selected = True
        elif itype == "gestures" and self.current_pin == "btn_gesture" and self.config.gesture_mode == "gestures":
            is_selected = True
        elif itype == "thumb_default" and self.current_pin == "thumbwheel" and not self.config.thumbwheel_divert:
            is_selected = True
        elif itype == "thumb_zoom" and self.current_pin == "thumbwheel" and self.config.thumbwheel_divert and self.config.thumbwheel_right_keys == ["KEY_LEFTCTRL", "KEY_EQUAL"]:
            is_selected = True
        elif itype == "thumb_volume" and self.current_pin == "thumbwheel" and self.config.thumbwheel_divert and self.config.thumbwheel_right_keys == ["KEY_VOLUMEUP"]:
            is_selected = True
        elif itype == "thumb_tabs" and self.current_pin == "thumbwheel" and self.config.thumbwheel_divert and self.config.thumbwheel_right_keys == ["KEY_LEFTCTRL", "KEY_PAGEDOWN"]:
            is_selected = True
        elif item.get("keys") is not None and itype == "action":
            if self.current_pin == "btn_top" and self.config.btn_top_action == "ToggleSmartShift":
                is_selected = False
            elif self.current_pin == "btn_middle" and self.config.btn_middle_action != "keypress":
                is_selected = False
            else:
                current_keys = self.get_current_pin_keys()
                if current_keys == item["keys"]:
                    is_selected = True

        if is_selected:
            btn.add_css_class("selected")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        radio_icon = Gtk.Label(label="●" if is_selected else "○")
        radio_icon.set_size_request(18, -1)
        box.append(radio_icon)

        lbl = Gtk.Label(label=item["name"])
        lbl.set_halign(Gtk.Align.START)
        box.append(lbl)

        btn.set_child(box)
        btn.connect("clicked", self.create_select_action_cb(item))
        self.content_container.append(btn)

        # Se for Gestures selecionado, renderiza o Card Oficial de Gestos abaixo dele (Screenshot Oficial)
        if is_selected and itype == "gestures":
            self.content_container.append(self.render_gestures_card())
        elif is_selected and itype == "thumb_shortcut":
            self.content_container.append(self.render_thumb_shortcut_card())
        elif is_selected and itype == "single_shortcut":
            self.content_container.append(self.render_single_shortcut_card())

    def render_thumb_shortcut_card(self):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.add_css_class("shortcut-config-box")

        desc = Gtk.Label(label=_("Press key combination to assign shortcut\n(Eg. 'Ctrl + C' for Copy)"))
        desc.add_css_class("callout-sub")
        desc.set_wrap(True)
        desc.set_halign(Gtk.Align.START)
        card.append(desc)

        # 1. SCROLL UP
        lbl_up = Gtk.Label(label=_("SCROLL UP"))
        lbl_up.add_css_class("category-header-label")
        lbl_up.set_halign(Gtk.Align.START)
        card.append(lbl_up)

        self.up_btn = Gtk.Button()
        self.up_btn.add_css_class("key-recorder-box")
        up_text = format_keys_display(self.config.thumbwheel_left_keys)
        if up_text == "None":
            up_text = _("Press key combination")
        
        self.up_lbl = Gtk.Label(label=up_text)
        self.up_lbl.set_halign(Gtk.Align.START)
        self.up_btn.set_child(self.up_lbl)

        if self.active_recording_target == "scroll_up":
            self.up_btn.add_css_class("recording-active")
            self.up_lbl.set_label(_("⌨️ Type shortcut on keyboard..."))
        
        self.up_btn.connect("clicked", lambda b: self.start_recording("scroll_up"))
        card.append(self.up_btn)

        # 2. SCROLL DOWN
        lbl_down = Gtk.Label(label=_("SCROLL DOWN"))
        lbl_down.add_css_class("category-header-label")
        lbl_down.set_halign(Gtk.Align.START)
        card.append(lbl_down)

        self.down_btn = Gtk.Button()
        self.down_btn.add_css_class("key-recorder-box")
        down_text = format_keys_display(self.config.thumbwheel_right_keys)
        if down_text == "None":
            down_text = _("Press key combination")

        self.down_lbl = Gtk.Label(label=down_text)
        self.down_lbl.set_halign(Gtk.Align.START)
        self.down_btn.set_child(self.down_lbl)

        if self.active_recording_target == "scroll_down":
            self.down_btn.add_css_class("recording-active")
            self.down_lbl.set_label(_("⌨️ Type shortcut on keyboard..."))

        self.down_btn.connect("clicked", lambda b: self.start_recording("scroll_down"))
        card.append(self.down_btn)

        return card

    def render_single_shortcut_card(self):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card.add_css_class("shortcut-config-box")

        desc = Gtk.Label(label=_("Press key combination to assign shortcut\n(Eg. 'Ctrl + C' for Copy)"))
        desc.add_css_class("callout-sub")
        desc.set_wrap(True)
        desc.set_halign(Gtk.Align.START)
        card.append(desc)

        lbl_s = Gtk.Label(label=_("SHORTCUT"))
        lbl_s.add_css_class("category-header-label")
        lbl_s.set_halign(Gtk.Align.START)
        card.append(lbl_s)

        self.single_key_btn = Gtk.Button()
        self.single_key_btn.add_css_class("key-recorder-box")
        cur_keys = self.get_current_pin_keys()
        txt = format_keys_display(cur_keys)
        if txt == "None":
            txt = _("Press key combination")

        self.single_lbl = Gtk.Label(label=txt)
        self.single_lbl.set_halign(Gtk.Align.START)
        self.single_key_btn.set_child(self.single_lbl)

        if self.active_recording_target == "single_key":
            self.single_key_btn.add_css_class("recording-active")
            self.single_lbl.set_label(_("⌨️ Type shortcut on keyboard..."))

        self.single_key_btn.connect("clicked", lambda b: self.start_recording("single_key"))
        card.append(self.single_key_btn)

        return card

    def start_recording(self, target):
        self.active_recording_target = target
        self.update_drawer()

    def render_gestures_card(self):
        g_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        g_card.add_css_class("gestures-config-box")

        title = Gtk.Label(label=_("Choose a preset or select custom to create your own."))
        title.add_css_class("callout-sub")
        title.set_halign(Gtk.Align.START)
        g_card.append(title)

        presets_map = get_gesture_presets_map()
        preset_names = [presets_map[i]["name"] for i in range(len(presets_map))]
        preset_model = Gtk.StringList.new(preset_names)
        preset_combo = Gtk.DropDown.new(preset_model, None)
        preset_combo.set_selected(self.gesture_preset_index)
        preset_combo.connect("notify::selected", self.on_gesture_preset_changed)
        g_card.append(preset_combo)

        # Recupera as 5 linhas do preset ativo
        preset_info = presets_map.get(self.gesture_preset_index, presets_map[0])
        gestures_rows = preset_info["rows"]

        for arrow_text, act_text in gestures_rows:
            s_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            s_row.add_css_class("gesture-subrow")

            a_lbl = Gtk.Label(label=arrow_text)
            a_lbl.add_css_class("gesture-arrow-text")
            a_lbl.set_halign(Gtk.Align.START)
            s_row.append(a_lbl)

            act_lbl = Gtk.Label(label=act_text)
            act_lbl.add_css_class("gesture-action-text")
            act_lbl.set_halign(Gtk.Align.START)
            s_row.append(act_lbl)

            g_card.append(s_row)

        return g_card

    def on_gesture_preset_changed(self, combo, pspec):
        sel = combo.get_selected()
        self.gesture_preset_index = sel
        self.config.gesture_mode = "gestures"
        presets_map = get_gesture_presets_map()
        preset = presets_map.get(sel, presets_map[0])

        self.config.gesture_up_keys = preset["up"]
        self.config.gesture_down_keys = preset["down"]
        self.config.gesture_left_keys = preset["left"]
        self.config.gesture_right_keys = preset["right"]

        if self.on_changed:
            self.on_changed()
        self.mouse_canvas.update_subtitles()
        self.update_drawer()

    def get_current_pin_keys(self):
        if self.current_pin == "btn_middle":
            return self.config.btn_middle_keys
        elif self.current_pin == "btn_top":
            return self.config.btn_top_keys
        elif self.current_pin == "btn_forward":
            return self.config.btn_forward_keys
        elif self.current_pin == "btn_back":
            return self.config.btn_back_keys
        elif self.current_pin == "thumbwheel":
            return self.config.thumbwheel_right_keys
        elif self.current_pin == "btn_gesture":
            return self.config.gesture_single_keys if self.config.gesture_mode == "keypress" else []
        return []

    def set_current_pin_keys(self, keys):
        if self.current_pin == "btn_middle":
            self.config.btn_middle_action = "keypress"
            self.config.btn_middle_keys = keys
        elif self.current_pin == "btn_top":
            self.config.btn_top_action = "keypress"
            self.config.btn_top_keys = keys
        elif self.current_pin == "btn_forward":
            self.config.btn_forward_keys = keys
        elif self.current_pin == "btn_back":
            self.config.btn_back_keys = keys
        elif self.current_pin == "btn_gesture":
            self.config.gesture_mode = "keypress"
            self.config.gesture_single_keys = keys
        elif self.current_pin == "thumbwheel":
            self.config.thumbwheel_divert = True
            self.config.thumbwheel_right_keys = keys
            if "KEY_PAGEDOWN" in keys:
                self.config.thumbwheel_left_keys = [k if k != "KEY_PAGEDOWN" else "KEY_PAGEUP" for k in keys]
            elif "KEY_RIGHT" in keys:
                self.config.thumbwheel_left_keys = [k if k != "KEY_RIGHT" else "KEY_LEFT" for k in keys]
            elif "KEY_VOLUMEUP" in keys:
                self.config.thumbwheel_left_keys = ["KEY_VOLUMEDOWN"]
            elif "KEY_EQUAL" in keys:
                self.config.thumbwheel_left_keys = ["KEY_LEFTCTRL", "KEY_MINUS"]
            elif "KEY_NEXTSONG" in keys:
                self.config.thumbwheel_left_keys = ["KEY_PREVIOUSSONG"]
            elif "KEY_BRIGHTNESSUP" in keys:
                self.config.thumbwheel_left_keys = ["KEY_BRIGHTNESSDOWN"]
            elif "KEY_TAB" in keys:
                self.config.thumbwheel_left_keys = ["KEY_LEFTALT", "KEY_LEFTSHIFT", "KEY_TAB"]
            elif "KEY_FORWARD" in keys:
                self.config.thumbwheel_left_keys = ["KEY_BACK"]
            else:
                self.config.thumbwheel_left_keys = keys

        if self.on_changed:
            self.on_changed()
        self.mouse_canvas.update_subtitles()
        self.update_drawer()

    def create_select_action_cb(self, item):
        def cb(btn):
            itype = item.get("type", "")
            if itype == "toggle_smartshift":
                self.thumb_mode = "preset"
                self.active_recording_target = None
                if self.current_pin == "btn_top":
                    self.config.btn_top_action = "ToggleSmartShift"
                    self.config.btn_top_keys = []
                elif self.current_pin == "btn_middle":
                    self.config.btn_middle_action = "ToggleSmartShift"
                    self.config.btn_middle_keys = []
                if self.on_changed:
                    self.on_changed()
                self.mouse_canvas.update_subtitles()
                self.update_drawer()
            elif itype == "middle_default":
                self.thumb_mode = "preset"
                self.active_recording_target = None
                if self.current_pin == "btn_middle":
                    self.config.btn_middle_action = "default"
                    self.config.btn_middle_keys = []
                if self.on_changed:
                    self.on_changed()
                self.mouse_canvas.update_subtitles()
                self.update_drawer()
            elif itype == "thumb_default":
                self.thumb_mode = "default"
                self.active_recording_target = None
                self.config.thumbwheel_divert = False
                if self.on_changed:
                    self.on_changed()
                self.mouse_canvas.update_subtitles()
                self.update_drawer()
            elif itype == "thumb_zoom":
                self.thumb_mode = "preset"
                self.active_recording_target = None
                self.set_current_pin_keys(["KEY_LEFTCTRL", "KEY_EQUAL"])
            elif itype == "thumb_volume":
                self.thumb_mode = "preset"
                self.active_recording_target = None
                self.set_current_pin_keys(["KEY_VOLUMEUP"])
            elif itype == "thumb_tabs":
                self.thumb_mode = "preset"
                self.active_recording_target = None
                self.set_current_pin_keys(["KEY_LEFTCTRL", "KEY_PAGEDOWN"])
            elif itype == "thumb_shortcut":
                self.thumb_mode = "shortcut"
                self.active_recording_target = "scroll_up"
                self.config.thumbwheel_divert = True
                self.update_drawer()
            elif itype == "single_shortcut":
                self.thumb_mode = "single_shortcut"
                self.active_recording_target = "single_key"
                if self.current_pin == "btn_gesture":
                    self.config.gesture_mode = "keypress"
                self.update_drawer()
            elif itype == "gestures":
                self.thumb_mode = "gestures"
                self.active_recording_target = None
                self.config.gesture_mode = "gestures"
                if self.on_changed:
                    self.on_changed()
                self.mouse_canvas.update_subtitles()
                self.update_drawer()
            elif item.get("keys") is not None:
                self.thumb_mode = "preset"
                self.active_recording_target = None
                self.set_current_pin_keys(item["keys"])
        return cb

    def on_key_pressed(self, controller, keyval, keycode, state):
        if not self.active_recording_target:
            return Gdk.EVENT_PROPAGATE

        evdev_key = None
        if keyval == Gdk.KEY_Control_L or keyval == Gdk.KEY_Control_R:
            evdev_key = "KEY_LEFTCTRL"
        elif keyval == Gdk.KEY_Shift_L or keyval == Gdk.KEY_Shift_R:
            evdev_key = "KEY_LEFTSHIFT"
        elif keyval == Gdk.KEY_Alt_L or keyval == Gdk.KEY_Alt_R:
            evdev_key = "KEY_LEFTALT"
        elif keyval == Gdk.KEY_Super_L or keyval == Gdk.KEY_Super_R:
            evdev_key = "KEY_LEFTMETA"
        elif keyval == Gdk.KEY_Page_Up:
            evdev_key = "KEY_PAGEUP"
        elif keyval == Gdk.KEY_Page_Down:
            evdev_key = "KEY_PAGEDOWN"
        elif keyval == Gdk.KEY_Home:
            evdev_key = "KEY_HOME"
        elif keyval == Gdk.KEY_End:
            evdev_key = "KEY_END"
        elif keyval == Gdk.KEY_Up:
            evdev_key = "KEY_UP"
        elif keyval == Gdk.KEY_Down:
            evdev_key = "KEY_DOWN"
        elif keyval == Gdk.KEY_Left:
            evdev_key = "KEY_LEFT"
        elif keyval == Gdk.KEY_Right:
            evdev_key = "KEY_RIGHT"
        elif keyval == Gdk.KEY_space:
            evdev_key = "KEY_SPACE"
        elif keyval == Gdk.KEY_Return:
            evdev_key = "KEY_ENTER"
        elif keyval == Gdk.KEY_Tab:
            evdev_key = "KEY_TAB"
        elif keyval == Gdk.KEY_BackSpace:
            evdev_key = "KEY_BACKSPACE"
        elif keyval == Gdk.KEY_Delete:
            evdev_key = "KEY_DELETE"
        elif keyval == Gdk.KEY_Print or keyval == Gdk.KEY_Sys_Req:
            evdev_key = "KEY_PRINT"
        elif keyval == Gdk.KEY_Escape:
            self.active_recording_target = None
            self.update_drawer()
            return Gdk.EVENT_STOP
        else:
            u = Gdk.keyval_to_unicode(keyval)
            if u and chr(u).isalnum():
                evdev_key = f"KEY_{chr(u).upper()}"

        if not evdev_key:
            return Gdk.EVENT_PROPAGATE

        keys = []
        if (state & Gdk.ModifierType.SUPER_MASK) and evdev_key != "KEY_LEFTMETA":
            keys.append("KEY_LEFTMETA")
        if (state & Gdk.ModifierType.CONTROL_MASK) and evdev_key != "KEY_LEFTCTRL":
            keys.append("KEY_LEFTCTRL")
        if (state & Gdk.ModifierType.ALT_MASK) and evdev_key != "KEY_LEFTALT":
            keys.append("KEY_LEFTALT")
        if (state & Gdk.ModifierType.SHIFT_MASK) and evdev_key != "KEY_LEFTSHIFT":
            keys.append("KEY_LEFTSHIFT")

        if evdev_key not in keys:
            keys.append(evdev_key)

        # Grava na direção correspondente
        if self.active_recording_target == "scroll_up":
            self.config.thumbwheel_divert = True
            self.config.thumbwheel_left_keys = keys
            self.thumb_mode = "shortcut"
            self.active_recording_target = None
        elif self.active_recording_target == "scroll_down":
            self.config.thumbwheel_divert = True
            self.config.thumbwheel_right_keys = keys
            self.thumb_mode = "shortcut"
            self.active_recording_target = None
        elif self.active_recording_target == "single_key":
            self.set_current_pin_keys(keys)
            self.active_recording_target = None

        if self.on_changed:
            self.on_changed()

        self.mouse_canvas.update_subtitles()
        self.update_drawer()
        return Gdk.EVENT_STOP
