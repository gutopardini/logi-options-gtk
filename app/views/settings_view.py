"""
Visualização de Ajustes e Diagnósticos do Sistema (GTK4 / Libadwaita)
Exibe informações reais do daemon logid, status de bateria via UPower e reset de configurações.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

from ..i18n import _
from ..backend.system_service import SystemService


class SettingsView(Gtk.Box):
    def __init__(self, config_manager, on_config_changed_cb):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.config = config_manager
        self.on_changed = on_config_changed_cb

        # Scrolled Window Principal
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # Container Clamped para centralização elegante
        clamp = Adw.Clamp()
        clamp.set_maximum_size(860)
        clamp.set_tightening_threshold(600)

        main_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_content.set_margin_top(28)
        main_content.set_margin_bottom(36)
        main_content.set_margin_start(24)
        main_content.set_margin_end(24)

        # -------------------------------------------------------------
        # 1. Seção BACKEND & DRIVER SYSTEMD (Real)
        # -------------------------------------------------------------
        lbl_backend = Gtk.Label(label=_("SYSTEM & DRIVER"))
        lbl_backend.add_css_class("category-header-label")
        lbl_backend.set_halign(Gtk.Align.START)
        main_content.append(lbl_backend)

        # Status do logid.service
        is_running = SystemService.is_logid_running()
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        status_box.add_css_class("card")
        status_box.set_margin_bottom(4)

        vbox_st = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox_st.set_hexpand(True)
        vbox_st.set_valign(Gtk.Align.CENTER)

        lbl_daemon_title = Gtk.Label(label=_("Daemon logid.service"))
        lbl_daemon_title.add_css_class("heading")
        lbl_daemon_title.set_halign(Gtk.Align.START)
        vbox_st.append(lbl_daemon_title)

        status_text = _("Active (Running)") if is_running else _("Inactive / Stopped")
        status_color = "#00e5c9" if is_running else "#ff5555"
        self.lbl_status_desc = Gtk.Label(
            label=f"<span foreground='{status_color}'>● {status_text}</span> • /etc/logid.cfg"
        )
        self.lbl_status_desc.set_use_markup(True)
        self.lbl_status_desc.add_css_class("callout-sub")
        self.lbl_status_desc.set_halign(Gtk.Align.START)
        vbox_st.append(self.lbl_status_desc)

        status_box.append(vbox_st)
        main_content.append(status_box)

        # -------------------------------------------------------------
        # 2. Seção DISPOSITIVO & BATERIA (UPower Real)
        # -------------------------------------------------------------
        lbl_dev_sec = Gtk.Label(label=_("DEVICE & POWER"))
        lbl_dev_sec.add_css_class("category-header-label")
        lbl_dev_sec.set_halign(Gtk.Align.START)
        main_content.append(lbl_dev_sec)

        bat_info = SystemService.get_battery_info()
        dev_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        dev_box.add_css_class("card")

        vbox_dev = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox_dev.set_hexpand(True)
        vbox_dev.set_valign(Gtk.Align.CENTER)

        lbl_dev_name = Gtk.Label(label=bat_info.get("model", "Logitech MX Master 3S"))
        lbl_dev_name.add_css_class("heading")
        lbl_dev_name.set_halign(Gtk.Align.START)
        vbox_dev.append(lbl_dev_name)

        pct = bat_info.get("percentage", "85%")
        st = bat_info.get("state", _("Connected"))
        lbl_dev_sub = Gtk.Label(label=f"{_('Battery')}: {pct} • {_('Status')}: {st}")
        lbl_dev_sub.add_css_class("callout-sub")
        lbl_dev_sub.set_halign(Gtk.Align.START)
        vbox_dev.append(lbl_dev_sub)

        dev_box.append(vbox_dev)
        main_content.append(dev_box)

        # -------------------------------------------------------------
        # 3. Seção RESTAURAR PADRÕES (Real)
        # -------------------------------------------------------------
        lbl_res_sec = Gtk.Label(label=_("CONFIGURATION"))
        lbl_res_sec.add_css_class("category-header-label")
        lbl_res_sec.set_halign(Gtk.Align.START)
        main_content.append(lbl_res_sec)

        reset_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        lbl_res = Gtk.Label(label=_("Restore to Default"))
        lbl_res.add_css_class("heading")
        lbl_res.set_halign(Gtk.Align.START)
        reset_box.append(lbl_res)

        lbl_res_d = Gtk.Label(label=_("Restore user device settings and key mappings to their default factory values."))
        lbl_res_d.add_css_class("callout-sub")
        lbl_res_d.set_halign(Gtk.Align.START)
        reset_box.append(lbl_res_d)

        btn_reset = Gtk.Button(label=_("RESET TO DEFAULT SETTINGS"))
        btn_reset.add_css_class("action-assign-btn")
        btn_reset.set_halign(Gtk.Align.START)
        btn_reset.connect("clicked", self.on_reset_defaults)
        reset_box.append(btn_reset)
        main_content.append(reset_box)

        # -------------------------------------------------------------
        # 4. Seção SOBRE O APLICATIVO
        # -------------------------------------------------------------
        lbl_about_sec = Gtk.Label(label=_("ABOUT"))
        lbl_about_sec.add_css_class("category-header-label")
        lbl_about_sec.set_halign(Gtk.Align.START)
        main_content.append(lbl_about_sec)

        about_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl_app_name = Gtk.Label(label="Logi Options+ for Linux v1.0.0")
        lbl_app_name.add_css_class("heading")
        lbl_app_name.set_halign(Gtk.Align.START)
        about_box.append(lbl_app_name)

        lbl_app_desc = Gtk.Label(label=_("Native GTK4 / Libadwaita frontend for Logitech MX Master 3S and logiops daemon."))
        lbl_app_desc.add_css_class("callout-sub")
        lbl_app_desc.set_halign(Gtk.Align.START)
        about_box.append(lbl_app_desc)
        main_content.append(about_box)

        clamp.set_child(main_content)
        scroll.set_child(clamp)
        self.append(scroll)

    def on_reset_defaults(self, btn):
        self.config.__init__()
        if self.on_changed:
            self.on_changed()
