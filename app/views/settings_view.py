"""
Visualização de Ajustes Oficial (1:1 com Logi Options+ Screenshot 5)
Fiel à hierarquia oficial de Firmware, Serial, Swap Buttons, Backup e Reset
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib

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
        # 1. Informações do Dispositivo e Firmware (Screenshot 5)
        # -------------------------------------------------------------
        firmware_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl_fw = Gtk.Label(label="Firmware version 22.0.3")
        lbl_fw.add_css_class("heading")
        lbl_fw.set_halign(Gtk.Align.START)
        firmware_box.append(lbl_fw)

        link_fw = Gtk.Label(label="<span foreground='#00e5c9' font_weight='bold'>CHECK FOR UPDATE</span>")
        link_fw.set_use_markup(True)
        link_fw.set_halign(Gtk.Align.START)
        firmware_box.append(link_fw)
        main_content.append(firmware_box)

        # Support
        support_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        lbl_sup_t = Gtk.Label(label="Support")
        lbl_sup_t.add_css_class("heading")
        lbl_sup_t.set_halign(Gtk.Align.START)
        support_box.append(lbl_sup_t)

        lbl_sup_desc = Gtk.Label(label="Visit <span foreground='#00e5c9'>MX Master 3S support page</span> for more information.")
        lbl_sup_desc.set_use_markup(True)
        lbl_sup_desc.add_css_class("callout-sub")
        lbl_sup_desc.set_halign(Gtk.Align.START)
        support_box.append(lbl_sup_desc)
        main_content.append(support_box)

        # Feature tour
        tour_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl_tr = Gtk.Label(label="Feature tour")
        lbl_tr.add_css_class("heading")
        lbl_tr.set_halign(Gtk.Align.START)
        tour_box.append(lbl_tr)

        link_tr = Gtk.Label(label="<span foreground='#00e5c9' font_weight='bold'>LAUNCH FEATURE TOUR</span>")
        link_tr.set_use_markup(True)
        link_tr.set_halign(Gtk.Align.START)
        tour_box.append(link_tr)
        main_content.append(tour_box)

        # -------------------------------------------------------------
        # 2. Seção GENERAL (Screenshot 5)
        # -------------------------------------------------------------
        lbl_gen = Gtk.Label(label="GENERAL")
        lbl_gen.add_css_class("category-header-label")
        lbl_gen.set_halign(Gtk.Align.START)
        main_content.append(lbl_gen)

        swap_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_swap = Gtk.Label(label="Swap left/right buttons")
        lbl_swap.add_css_class("heading")
        swap_row.append(lbl_swap)

        sp2 = Gtk.Box()
        sp2.set_hexpand(True)
        swap_row.append(sp2)

        sw_swap = Gtk.Switch()
        swap_row.append(sw_swap)
        main_content.append(swap_row)

        # -------------------------------------------------------------
        # 3. Seção OTHER (Screenshot 5)
        # -------------------------------------------------------------
        lbl_oth = Gtk.Label(label="OTHER")
        lbl_oth.add_css_class("category-header-label")
        lbl_oth.set_halign(Gtk.Align.START)
        main_content.append(lbl_oth)

        # Device Backup
        backup_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl_bk = Gtk.Label(label="Device backup")
        lbl_bk.add_css_class("heading")
        lbl_bk.set_halign(Gtk.Align.START)
        backup_box.append(lbl_bk)

        lbl_bk_d = Gtk.Label(label="Login to backup your device settings to the cloud so you can use the settings on another computer")
        lbl_bk_d.add_css_class("callout-sub")
        lbl_bk_d.set_wrap(True)
        lbl_bk_d.set_halign(Gtk.Align.START)
        backup_box.append(lbl_bk_d)

        link_login = Gtk.Label(label="<span foreground='#00e5c9' font_weight='bold'>LOGIN</span>")
        link_login.set_use_markup(True)
        link_login.set_halign(Gtk.Align.START)
        backup_box.append(link_login)
        main_content.append(backup_box)

        # Restore to Default
        reset_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl_res = Gtk.Label(label="Restore to Default")
        lbl_res.add_css_class("heading")
        lbl_res.set_halign(Gtk.Align.START)
        reset_box.append(lbl_res)

        lbl_res_d = Gtk.Label(label="Restore user device settings to their Default.")
        lbl_res_d.add_css_class("callout-sub")
        lbl_res_d.set_halign(Gtk.Align.START)
        reset_box.append(lbl_res_d)

        btn_reset = Gtk.Button(label="RESET TO DEFAULT SETTINGS")
        btn_reset.add_css_class("action-assign-btn")
        btn_reset.set_halign(Gtk.Align.START)
        btn_reset.connect("clicked", self.on_reset_defaults)
        reset_box.append(btn_reset)
        main_content.append(reset_box)

        # Remove Device
        rm_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lbl_rm = Gtk.Label(label="Remove device")
        lbl_rm.add_css_class("heading")
        lbl_rm.set_halign(Gtk.Align.START)
        rm_box.append(lbl_rm)

        lbl_rm_d = Gtk.Label(label="The device will not reconnect automatically. You will have to pair the device again to use it.")
        lbl_rm_d.add_css_class("callout-sub")
        lbl_rm_d.set_wrap(True)
        lbl_rm_d.set_halign(Gtk.Align.START)
        rm_box.append(lbl_rm_d)
        main_content.append(rm_box)

        clamp.set_child(main_content)
        scroll.set_child(clamp)
        self.append(scroll)

    def on_copy_serial(self, btn):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set("2228LZ53N1B8")
        btn.set_label("✅")
        GLib.timeout_add_seconds(2, lambda: btn.set_label("📋") or False)

    def on_reset_defaults(self, btn):
        self.config.__init__()
        if self.on_changed:
            self.on_changed()
