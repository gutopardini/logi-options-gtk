"""
Janela Principal do Logi Options+ (Design 1:1 Oficial da Logitech em GTK4 / Libadwaita)
Fiel às capturas de tela oficiais com perfis de aplicativos reais (+ ADD APPLICATION)
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from .backend.config_manager import LogidConfig
from .backend.system_service import SystemService
from .backend.app_manager import AppManager
from .views.buttons_view import ButtonsView
from .views.point_scroll_view import PointScrollView
from .views.easy_switch_view import EasySwitchView
from .views.settings_view import SettingsView
from .widgets.add_app_dialog import AddAppDialog


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Logi Options+ (MX Master 3S)")
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
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        sidebar.add_css_class("sidebar-container")
        sidebar.set_size_request(220, -1)
        root_box.append(sidebar)

        top_spacer = Gtk.Box()
        top_spacer.set_size_request(-1, 85)
        sidebar.append(top_spacer)

        self.tab_buttons = {}
        nav_items = [
            ("buttons", "BUTTONS", "input-mouse-symbolic"),
            ("scroll", "POINT AND SCROLL", "preferences-desktop-peripherals-symbolic"),
            ("easy_switch", "EASY-SWITCH", "video-display-symbolic"),
            ("settings", "SETTINGS", "emblem-system-symbolic"),
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
            sidebar.append(btn)
            self.tab_buttons[tab_id] = btn

        bottom_spacer = Gtk.Box()
        bottom_spacer.set_vexpand(True)
        sidebar.append(bottom_spacer)

        # Badge de Bateria Real
        bat_info = SystemService.get_battery_info()
        self.bat_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.bat_box.add_css_class("official-battery-badge")
        self.bat_lbl = Gtk.Label(label=f"{bat_info['percentage']}  🔋  ⚡")
        self.bat_box.append(self.bat_lbl)
        sidebar.append(self.bat_box)

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

        # Título do Mouse com Botão Voltar (← MX Master 3S)
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        
        self.back_btn = Gtk.Button(label="←")
        self.back_btn.add_css_class("back-nav-btn")
        self.back_btn.set_tooltip_text("Voltar")
        self.back_btn.connect("clicked", self.on_back_btn_clicked)
        title_box.append(self.back_btn)

        dev_title = Gtk.Label(label="MX Master 3S")
        dev_title.add_css_class("device-title")
        title_box.append(dev_title)
        header_bar.append(title_box)

        # Espaçador Central
        header_spacer = Gtk.Box()
        header_spacer.set_hexpand(True)
        header_bar.append(header_spacer)

        # Barra de Perfis de Aplicativos (Temporariamente desativada a pedido do usuário)
        # self.profiles_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        # header_bar.append(self.profiles_box)
        # self.render_app_profiles_bar()

        # Botão Aplicar no Sistema
        self.apply_btn = Gtk.Button(label="Aplicar no Sistema")
        self.apply_btn.add_css_class("official-apply-btn")
        self.apply_btn.connect("clicked", self.on_apply_clicked)
        header_bar.append(self.apply_btn)

        # Botão Fechar Oficial (Apenas '✕')
        close_btn = Gtk.Button(label="✕")
        close_btn.add_css_class("close-nav-btn")
        close_btn.set_tooltip_text("Fechar o Logi Options+")
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
        self.point_scroll_view = PointScrollView(self.config, self.on_config_modified)
        self.easy_switch_view = EasySwitchView(self.config, self.on_config_modified)
        self.settings_view = SettingsView(self.config, self.on_config_modified)

        self.view_stack.add_named(self.buttons_view, "buttons")
        self.view_stack.add_named(self.point_scroll_view, "scroll")
        self.view_stack.add_named(self.easy_switch_view, "easy_switch")
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
            btn_global.set_tooltip_text("Configurações Globais (Ativo)")
        else:
            btn_global.remove_css_class("global-app-btn")
            btn_global.add_css_class("add-app-btn")
            btn_global.set_tooltip_text("Alternar para Configurações Globais")
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
            app_btn.set_tooltip_text(f"Perfil de: {app['name']}")
            app_btn.connect("clicked", self.create_app_profile_cb(app["name"]))
            self.profiles_box.append(app_btn)

        # 3. Botão "+ ADD APPLICATION"
        add_app_btn = Gtk.Button(label="+ ADD APPLICATION")
        add_app_btn.add_css_class("add-app-btn")
        add_app_btn.set_tooltip_text("Adicionar perfil para software instalado")
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

        toast = Adw.Toast.new(f"📌 Perfil ativo: {profile_name}")
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

        toast = Adw.Toast.new(f"✅ {len(selected_apps)} aplicativo(s) adicionado(s) com sucesso!")
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)

    def on_window_key_pressed(self, controller, keyval, keycode, state):
        if keyval == Gdk.KEY_Escape:
            self.close()
            return Gdk.EVENT_STOP
        if (state & Gdk.ModifierType.CONTROL_MASK) and (keyval == Gdk.KEY_q or keyval == Gdk.KEY_Q):
            self.close()
            return Gdk.EVENT_STOP
        return Gdk.EVENT_PROPAGATE

    def create_nav_callback(self, tab_id):
        def cb(button):
            self.switch_tab(tab_id)
        return cb

    def switch_tab(self, tab_id):
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
        self.apply_btn.set_label("Aplicando...")

        cfg_str = self.config.generate_config_string()
        success, msg = SystemService.apply_config(cfg_str)
        
        self.apply_btn.set_sensitive(True)
        self.apply_btn.set_label("Aplicar no Sistema")

        if success:
            toast = Adw.Toast.new("✅ Configurações aplicadas com sucesso no logid!")
            toast.set_timeout(3)
            self.toast_overlay.add_toast(toast)
        else:
            toast = Adw.Toast.new(f"⚠️ Erro ao aplicar: {msg[:60] if msg else 'Cancelado'}")
            toast.set_timeout(4)
            self.toast_overlay.add_toast(toast)

    def on_drawer_toggled(self, is_open):
        self.sidebar.set_visible(not is_open)

    def on_back_btn_clicked(self, btn):
        if hasattr(self, "buttons_view") and self.buttons_view.current_pin:
            self.buttons_view.close_drawer()
        else:
            self.close()
