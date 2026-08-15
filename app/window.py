"""
Janela Principal do Logi Options+ (Design 1:1 Oficial da Logitech em GTK4 / Libadwaita)
Fiel às capturas de tela oficiais com navegação fluida, gavetas animadas e suporte a atalhos.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk

from .i18n import _
from .backend.config_manager import LogidConfig
from .backend.system_service import SystemService
from .backend.app_manager import AppManager
from .views.buttons_view import ButtonsView
from .views.point_scroll_view import PointScrollView
from .views.settings_view import SettingsView
from .widgets.add_app_dialog import AddAppDialog


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title(_("Logi Options+ (MX Master 3S)"))
        self.set_default_size(1280, 800)

        # Gerenciador de Configuração e Perfis
        self.config = LogidConfig()
        self.config.load_from_file()
        self.profiles_data = AppManager.load_profiles()
        self.active_profile = self.profiles_data.get("active_profile", "global")

        # Toast Overlay para Notificações Nativas
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        # Container Principal Horizontal
        root_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.toast_overlay.set_child(root_box)

        # -------------------------------------------------------------
        # 1. Barra Lateral Esquerda Oficial (Left Sidebar)
        # -------------------------------------------------------------
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.sidebar.add_css_class("sidebar-container")
        self.sidebar.set_size_request(220, -1)
        root_box.append(self.sidebar)

        top_spacer = Gtk.Box()
        top_spacer.set_size_request(-1, 85)
        self.sidebar.append(top_spacer)

        self.tab_buttons = {}
        nav_items = [
            ("buttons", _("BUTTONS"), "input-mouse-symbolic"),
            ("scroll", _("POINT AND SCROLL"), "preferences-desktop-peripherals-symbolic"),
            ("settings", _("SETTINGS"), "emblem-system-symbolic"),
        ]

        for tab_id, label_text, icon_name in nav_items:
            btn = Gtk.Button()
            btn.add_css_class("sidebar-tab-btn")
            
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            icon = Gtk.Image.new_from_icon_name(icon_name)
            box.append(icon)
            lbl = Gtk.Label(label=label_text)
            box.append(lbl)
            btn.set_child(box)

            btn.connect("clicked", self.create_nav_callback(tab_id))
            self.sidebar.append(btn)
            self.tab_buttons[tab_id] = btn

        bottom_spacer = Gtk.Box()
        bottom_spacer.set_vexpand(True)
        self.sidebar.append(bottom_spacer)

        # Badge de Bateria Real com Auto-Detecção e Clique para Redetectar
        self.bat_box = Gtk.Button()
        self.bat_box.add_css_class("official-battery-badge")
        self.bat_lbl = Gtk.Label(label="--% 🔋")
        self.bat_box.set_child(self.bat_lbl)
        self.bat_box.connect("clicked", lambda b: self.update_battery_status(user_initiated=True))
        self.sidebar.append(self.bat_box)

        # Inicia atualização inicial e polling dinâmico a cada 2 segundos
        self.update_battery_status(user_initiated=False)
        GLib.timeout_add_seconds(2, self.update_battery_status)

        # -------------------------------------------------------------
        # 2. Área Central e Header Superior Oficial (Arrastável com WindowHandle)
        # -------------------------------------------------------------
        center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        center_box.set_hexpand(True)
        center_box.set_vexpand(True)
        root_box.append(center_box)

        window_handle = Gtk.WindowHandle()
        header_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        header_bar.add_css_class("logi-header-official")
        window_handle.set_child(header_bar)
        center_box.append(window_handle)

        # Título do Mouse (← MX Master 3S)
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

        self.back_nav_btn = Gtk.Button(label="←")
        self.back_nav_btn.add_css_class("back-nav-btn")
        self.back_nav_btn.set_visible(False)
        self.back_nav_btn.connect("clicked", self.on_back_nav_clicked)
        title_box.append(self.back_nav_btn)

        dev_title = Gtk.Label(label="MX Master 3S")
        dev_title.add_css_class("device-title")
        title_box.append(dev_title)
        header_bar.append(title_box)

        # Espaçador Central
        header_spacer = Gtk.Box()
        header_spacer.set_hexpand(True)
        header_bar.append(header_spacer)

        # Barra de Perfis de Aplicativos (Oculta temporariamente)
        self.profiles_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.profiles_box.set_visible(False)
        header_bar.append(self.profiles_box)

        # Botão Aplicar no Sistema
        self.apply_btn = Gtk.Button(label=_("Apply to System"))
        self.apply_btn.add_css_class("official-apply-btn")
        self.apply_btn.connect("clicked", self.on_apply_clicked)
        header_bar.append(self.apply_btn)

        # Botão Fechar Oficial (Apenas '✕')
        close_btn = Gtk.Button(label="✕")
        close_btn.add_css_class("close-nav-btn")
        close_btn.set_tooltip_text(_("Close Logi Options+"))
        close_btn.connect("clicked", lambda b: self.close())
        header_bar.append(close_btn)

        # -------------------------------------------------------------
        # 3. ViewStack com as Telas Oficiais
        # -------------------------------------------------------------
        self.view_stack = Gtk.Stack()
        self.view_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.view_stack.set_transition_duration(180)
        self.view_stack.set_hexpand(True)
        self.view_stack.set_vexpand(True)
        center_box.append(self.view_stack)

        self.buttons_view = ButtonsView(self.config, self.on_config_modified, on_drawer_toggle_cb=self.on_drawer_toggled)
        self.point_scroll_view = PointScrollView(self.config, self.on_config_modified, on_drawer_toggle_cb=self.on_drawer_toggled)
        self.settings_view = SettingsView(self.config, self.on_config_modified)

        self.view_stack.add_named(self.buttons_view, "buttons")
        self.view_stack.add_named(self.point_scroll_view, "scroll")
        self.view_stack.add_named(self.settings_view, "settings")

        # Atalhos Globais (Esc / Ctrl+Q)
        key_ctrl = Gtk.EventControllerKey()
        key_ctrl.connect("key-pressed", self.on_window_key_pressed)
        self.add_controller(key_ctrl)

        self.switch_tab("buttons")

    def render_app_profiles_bar(self):
        """Renderiza a barra de perfis com suporte a múltiplos aplicativos"""
        while self.profiles_box.get_first_child():
            self.profiles_box.remove(self.profiles_box.get_first_child())

        # 1. Perfil Global (⊞)
        btn_global = Gtk.Button(label="⊞")
        btn_global.add_css_class("global-app-btn")
        if self.active_profile == "global":
            btn_global.set_tooltip_text(_("Global Settings (Active)"))
        else:
            btn_global.remove_css_class("global-app-btn")
            btn_global.add_css_class("add-app-btn")
            btn_global.set_tooltip_text(_("Switch to Global Settings"))
        btn_global.connect("clicked", lambda b: self.set_active_profile("global"))
        self.profiles_box.append(btn_global)

        # 2. Aplicativos Adicionados
        apps = self.profiles_data.get("apps", [])
        for app in apps:
            app_btn = Gtk.Button()
            app_btn.add_css_class("add-app-btn")
            if self.active_profile == app["name"]:
                app_btn.add_css_class("global-app-btn")
                app_btn.remove_css_class("add-app-btn")

            app_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            if app.get("icon", "").startswith("/"):
                img = Gtk.Image.new_from_file(app["icon"])
            else:
                img = Gtk.Image.new_from_icon_name(app.get("icon", "application-x-executable"))
            img.set_pixel_size(20)
            app_box.append(img)

            lbl = Gtk.Label(label=app["name"])
            app_box.append(lbl)

            # Botão de Remover Perfil no X
            del_lbl = Gtk.Label(label=" ×")
            del_lbl.add_css_class("callout-sub")
            app_box.append(del_lbl)

            app_btn.set_child(app_box)
            app_btn.set_tooltip_text(_("Profile for: {name}").format(name=app['name']))
            app_btn.connect("clicked", self.create_app_profile_cb(app["name"]))
            self.profiles_box.append(app_btn)

        # 3. Botão "+ ADD APPLICATION"
        add_app_btn = Gtk.Button(label=_("+ ADD APPLICATION"))
        add_app_btn.add_css_class("add-app-btn")
        add_app_btn.set_tooltip_text(_("Add profile for installed application"))
        add_app_btn.connect("clicked", self.on_add_application_clicked)
        self.profiles_box.append(add_app_btn)

    def create_app_profile_cb(self, app_name):
        def cb(btn):
            self.set_active_profile(app_name)
        return cb

    def set_active_profile(self, profile_name):
        self.active_profile = profile_name
        self.profiles_data["active_profile"] = profile_name
        AppManager.save_profiles(self.profiles_data)
        self.render_app_profiles_bar()

        toast = Adw.Toast.new(_("📌 Active profile: {name}").format(name=profile_name))
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)

    def on_add_application_clicked(self, btn):
        dialog = AddAppDialog(self, self.on_apps_added)
        dialog.present()

    def on_apps_added(self, selected_apps):
        current_apps = self.profiles_data.get("apps", [])
        current_names = {a["name"] for a in current_apps}

        for app in selected_apps:
            if app["name"] not in current_names:
                current_apps.append(app)

        self.profiles_data["apps"] = current_apps
        if selected_apps:
            self.active_profile = selected_apps[-1]["name"]
            self.profiles_data["active_profile"] = self.active_profile

        AppManager.save_profiles(self.profiles_data)
        self.render_app_profiles_bar()

        toast = Adw.Toast.new(_("✅ {count} application(s) added successfully!").format(count=len(selected_apps)))
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)

    def on_window_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            if hasattr(self, "buttons_view") and self.buttons_view.drawer_box.get_visible():
                self.buttons_view.close_drawer()
                return Gdk.EVENT_STOP
            if hasattr(self, "point_scroll_view") and self.point_scroll_view.drawer_box.get_visible():
                self.point_scroll_view.close_drawer()
                return Gdk.EVENT_STOP
            self.close()
            return Gdk.EVENT_STOP
        if (state & Gdk.ModifierType.CONTROL_MASK) and (keyval == Gdk.KEY_q or keyval == Gdk.KEY_Q):
            self.close()
            return Gdk.EVENT_STOP
        return Gdk.EVENT_PROPAGATE

    def on_back_nav_clicked(self, btn):
        if hasattr(self, "buttons_view") and self.buttons_view.drawer_box.get_visible():
            self.buttons_view.close_drawer()
        if hasattr(self, "point_scroll_view") and self.point_scroll_view.drawer_box.get_visible():
            self.point_scroll_view.close_drawer()

    def create_nav_callback(self, tab_id):
        def cb(button):
            self.switch_tab(tab_id)
        return cb

    def switch_tab(self, tab_id):
        if hasattr(self, "buttons_view"):
            self.buttons_view.close_drawer()
        if hasattr(self, "point_scroll_view"):
            self.point_scroll_view.close_drawer()

        self.view_stack.set_visible_child_name(tab_id)
        for tid, btn in self.tab_buttons.items():
            if tid == tab_id:
                btn.add_css_class("active")
            else:
                btn.remove_css_class("active")

    def on_config_modified(self):
        if hasattr(self, "buttons_view") and hasattr(self.buttons_view, "mouse_canvas"):
            self.buttons_view.mouse_canvas.update_subtitles()
        if hasattr(self, "point_scroll_view") and hasattr(self.point_scroll_view, "mouse_canvas"):
            self.point_scroll_view.mouse_canvas.update_subtitles()

    def on_apply_clicked(self, btn):
        self.apply_btn.set_sensitive(False)
        self.apply_btn.set_label(_("Applying..."))

        cfg_str = self.config.generate_config_string()
        success, msg = SystemService.apply_config(cfg_str)
        
        self.apply_btn.set_sensitive(True)
        self.apply_btn.set_label(_("Apply to System"))

        if success:
            toast = Adw.Toast.new(_("✅ Settings applied successfully to logid!"))
            toast.set_timeout(3)
            self.toast_overlay.add_toast(toast)
        else:
            err_text = msg[:60] if msg else _("Cancelled")
            toast = Adw.Toast.new(_("⚠️ Error applying: {error}").format(error=err_text))
            toast.set_timeout(4)
            self.toast_overlay.add_toast(toast)

    def on_drawer_toggled(self, is_open):
        if hasattr(self, "sidebar") and self.sidebar:
            self.sidebar.set_visible(not is_open)
        if hasattr(self, "back_nav_btn") and self.back_nav_btn:
            self.back_nav_btn.set_visible(is_open)

    def update_battery_status(self, user_initiated=False):
        bat_info = SystemService.get_battery_info()
        if bat_info.get("connected") and bat_info.get("percentage"):
            pct = bat_info["percentage"]
            icon_conn = "⚡" if bat_info.get("is_charging") else "ᛒ"
            self.bat_lbl.set_label(f"{pct}  🔋  {icon_conn}")
            self.bat_box.remove_css_class("offline")
            if bat_info.get("is_charging"):
                self.bat_box.add_css_class("charging")
            else:
                self.bat_box.remove_css_class("charging")
            self.bat_box.set_tooltip_text(_("Battery: {pct} • State: {st}\nClick to re-scan devices").format(
                pct=pct, st=bat_info.get("state", "Connected")
            ))
            if user_initiated:
                toast = Adw.Toast.new(_("✅ Mouse detected ({pct})").format(pct=pct))
                toast.set_timeout(2)
                self.toast_overlay.add_toast(toast)
        else:
            self.bat_lbl.set_label(_("Disconnected 🔴"))
            self.bat_box.add_css_class("offline")
            self.bat_box.remove_css_class("charging")
            self.bat_box.set_tooltip_text(_("Mouse disconnected\nClick to re-scan devices"))
            if user_initiated:
                toast = Adw.Toast.new(_("⚠️ Mouse not found. Please check connection."))
                toast.set_timeout(2)
                self.toast_overlay.add_toast(toast)
        return True
