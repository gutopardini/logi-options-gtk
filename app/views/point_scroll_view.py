"""
Visualização de Apontar e Rolar Oficial (1:1 com Logi Options+ Screenshot 0, 1, 2, 3)
Canvas do mouse com os 3 callouts oficiais (Scroll wheel, Thumb wheel, Pointer speed)
e Gaveta Lateral Aberta sob demanda com os sliders calibrados de acordo com o backend logiops.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from ..i18n import _
from ..widgets.mouse_canvas import MouseCanvas


class PointScrollView(Gtk.Box):
    def __init__(self, config_manager, on_config_changed_cb, on_drawer_toggle_cb=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.config = config_manager
        self.on_changed = on_config_changed_cb
        self.on_drawer_toggle = on_drawer_toggle_cb
        self.selected_subtab = "scroll_wheel"
        self.extend_8k = (self.config.dpi > 4000)

        # 1. Canvas do Mouse Central no modo point_scroll (3 callouts oficiais)
        self.mouse_canvas = MouseCanvas(self.config, mode="point_scroll")
        self.mouse_canvas.connect('pin-selected', self.on_pin_clicked)
        self.append(self.mouse_canvas)

        # 2. Drawer Lateral Direito (Inicia oculto como na visão geral - Imagem 0)
        self.drawer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.drawer_box.add_css_class("actions-drawer-container")
        self.drawer_box.set_size_request(400, -1)
        self.drawer_box.set_vexpand(True)
        self.drawer_box.set_visible(False)

        # Header do Drawer com Título e Botão Fechar Oficial
        d_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.drawer_title = Gtk.Label(label=_("Scroll wheel"))
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

        # Container Rolável do Conteúdo do Drawer
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.drawer_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        scroll.set_child(self.drawer_content)
        self.drawer_box.append(scroll)

        self.append(self.drawer_box)

    def on_pin_clicked(self, canvas, pin_id):
        if pin_id == "scroll_wheel":
            self.selected_subtab = "scroll_wheel"
        elif pin_id == "thumb_wheel":
            self.selected_subtab = "thumb_wheel"
        elif pin_id == "pointer_speed":
            self.selected_subtab = "pointer_speed"
        else:
            return

        self.drawer_box.set_visible(True)
        if self.on_drawer_toggle:
            self.on_drawer_toggle(True)
        self.update_drawer()

    def close_drawer(self):
        self.drawer_box.set_visible(False)
        self.mouse_canvas.select_pin(None)
        if self.on_drawer_toggle:
            self.on_drawer_toggle(False)

    def update_drawer(self):
        while self.drawer_content.get_first_child():
            self.drawer_content.remove(self.drawer_content.get_first_child())

        if self.selected_subtab == "scroll_wheel":
            self.render_scroll_wheel_drawer()
        elif self.selected_subtab == "thumb_wheel":
            self.render_thumb_wheel_drawer()
        else:
            self.render_pointer_speed_drawer()

    def render_scroll_wheel_drawer(self):
        """1:1 com Screenshot 3: Scroll wheel"""
        self.drawer_title.set_label(_("Scroll wheel"))

        # 1. Scroll direction
        sec_dir = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        lbl_dir = Gtk.Label(label=_("Scroll direction"))
        lbl_dir.add_css_class("category-header-label")
        lbl_dir.set_halign(Gtk.Align.START)
        sec_dir.append(lbl_dir)

        # Inverted Radio
        btn_inv = Gtk.Button()
        btn_inv.add_css_class("action-radio-row")
        if self.config.hiresscroll_invert:
            btn_inv.add_css_class("selected")
        b_inv = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        b_inv.append(Gtk.Label(label="●" if self.config.hiresscroll_invert else "○"))
        b_inv.append(Gtk.Label(label=_("Inverted")))
        btn_inv.set_child(b_inv)
        btn_inv.connect("clicked", lambda b: self.set_wheel_direction(True))
        sec_dir.append(btn_inv)

        # Standard Radio
        btn_std = Gtk.Button()
        btn_std.add_css_class("action-radio-row")
        if not self.config.hiresscroll_invert:
            btn_std.add_css_class("selected")
        b_std = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        b_std.append(Gtk.Label(label="●" if not self.config.hiresscroll_invert else "○"))
        b_std.append(Gtk.Label(label=_("Standard")))
        btn_std.set_child(b_std)
        btn_std.connect("clicked", lambda b: self.set_wheel_direction(False))
        sec_dir.append(btn_std)

        self.drawer_content.append(sec_dir)

        # 2. Smooth scrolling
        sec_smooth = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        row_smooth = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_smooth = Gtk.Label(label=_("Smooth scrolling"))
        lbl_smooth.add_css_class("heading")
        lbl_smooth.set_halign(Gtk.Align.START)
        row_smooth.append(lbl_smooth)

        sp = Gtk.Box()
        sp.set_hexpand(True)
        row_smooth.append(sp)

        sw_smooth = Gtk.Switch()
        sw_smooth.set_active(self.config.hiresscroll_hires)
        sw_smooth.connect("notify::active", self.on_smooth_toggle)
        row_smooth.append(sw_smooth)
        sec_smooth.append(row_smooth)

        desc_smooth = Gtk.Label(label=_("With smooth scrolling, web pages glide across your screen smoothly making it easy to read and navigate them."))
        desc_smooth.set_wrap(True)
        desc_smooth.add_css_class("callout-sub")
        desc_smooth.set_halign(Gtk.Align.START)
        sec_smooth.append(desc_smooth)
        self.drawer_content.append(sec_smooth)

        # 3. SmartShift
        sec_ss = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        row_ss = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_ss = Gtk.Label(label=_("SmartShift"))
        lbl_ss.add_css_class("heading")
        lbl_ss.set_halign(Gtk.Align.START)
        row_ss.append(lbl_ss)

        sp2 = Gtk.Box()
        sp2.set_hexpand(True)
        row_ss.append(sp2)

        sw_ss = Gtk.Switch()
        sw_ss.set_active(self.config.smartshift_on)
        sw_ss.connect("notify::active", self.on_smartshift_toggle)
        row_ss.append(sw_ss)
        sec_ss.append(row_ss)

        desc_ss = Gtk.Label(label=_("Automatically switches the scroll wheel from line-by-line scrolling to hyper-fast scrolling when you scroll faster."))
        desc_ss.set_wrap(True)
        desc_ss.add_css_class("callout-sub")
        desc_ss.set_halign(Gtk.Align.START)
        sec_ss.append(desc_ss)

        if self.config.smartshift_on:
            sens_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            sens_box.set_margin_top(12)

            sens_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            sens_lbl = Gtk.Label(label=_("SENSITIVITY VALUE"))
            sens_lbl.add_css_class("category-header-label")
            sens_lbl.set_halign(Gtk.Align.START)
            sens_header.append(sens_lbl)

            sp_s = Gtk.Box()
            sp_s.set_hexpand(True)
            sens_header.append(sp_s)

            # 5 (High/Fast) -> 100%, 50 (Low) -> 10%
            current_sens_pct = int(round(100 - (self.config.smartshift_threshold - 5) / 45.0 * 90))
            current_sens_pct = max(10, min(100, current_sens_pct))
            self.sens_val_lbl = Gtk.Label(label=f"{current_sens_pct}%")
            self.sens_val_lbl.add_css_class("callout-sub")
            sens_header.append(self.sens_val_lbl)
            sens_box.append(sens_header)

            sens_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 10, 100, 1)
            sens_scale.set_value(current_sens_pct)
            sens_scale.add_css_class("logi-scale")
            sens_scale.connect("value-changed", self.on_smartshift_sens_changed)
            sens_box.append(sens_scale)
            sec_ss.append(sens_box)
        else:
            sub_ss = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            sub_ss.set_margin_top(10)

            btn_r = Gtk.Button()
            btn_r.add_css_class("action-radio-row")
            btn_r.add_css_class("selected")
            b_r = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            b_r.append(Gtk.Label(label="●"))
            b_r.append(Gtk.Label(label=_("Ratchet (Line-by-line scroll)")))
            btn_r.set_child(b_r)
            sub_ss.append(btn_r)

            btn_f = Gtk.Button()
            btn_f.add_css_class("action-radio-row")
            b_f = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            b_f.append(Gtk.Label(label="○"))
            b_f.append(Gtk.Label(label=_("Free spin (Hyper-fast)")))
            btn_f.set_child(b_f)
            sub_ss.append(btn_f)
            sec_ss.append(sub_ss)

        self.drawer_content.append(sec_ss)

    def render_thumb_wheel_drawer(self):
        """1:1 com Screenshot 1: Thumb wheel"""
        self.drawer_title.set_label(_("Thumb wheel"))

        # 1. Thumb wheel speed
        sec_speed = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        hdr_speed = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_s = Gtk.Label(label=_("Thumb wheel speed"))
        lbl_s.add_css_class("heading")
        lbl_s.set_halign(Gtk.Align.START)
        hdr_speed.append(lbl_s)

        sp = Gtk.Box()
        sp.set_hexpand(True)
        hdr_speed.append(sp)

        speed_pct = int(round(100 - (self.config.thumbwheel_left_interval - 1) / 14.0 * 90))
        speed_pct = max(10, min(100, speed_pct))
        self.speed_val_lbl = Gtk.Label(label=f"{speed_pct}%")
        self.speed_val_lbl.add_css_class("heading")
        hdr_speed.append(self.speed_val_lbl)
        sec_speed.append(hdr_speed)

        scale_speed = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 10, 100, 1)
        scale_speed.set_value(speed_pct)
        scale_speed.add_css_class("logi-scale")
        scale_speed.connect("value-changed", self.on_thumb_speed_changed)
        sec_speed.append(scale_speed)
        self.drawer_content.append(sec_speed)

        # 2. Thumb wheel direction
        sec_tdir = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        lbl_tdir = Gtk.Label(label=_("Thumb wheel direction"))
        lbl_tdir.add_css_class("category-header-label")
        lbl_tdir.set_halign(Gtk.Align.START)
        sec_tdir.append(lbl_tdir)

        # Default Radio
        btn_def = Gtk.Button()
        btn_def.add_css_class("action-radio-row")
        if not self.config.thumbwheel_invert:
            btn_def.add_css_class("selected")
        b_def = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        b_def.append(Gtk.Label(label="●" if not self.config.thumbwheel_invert else "○"))
        b_def.append(Gtk.Label(label=_("Default")))
        btn_def.set_child(b_def)
        btn_def.connect("clicked", lambda b: self.set_thumb_direction(False))
        sec_tdir.append(btn_def)

        # Inverted Radio
        btn_tinv = Gtk.Button()
        btn_tinv.add_css_class("action-radio-row")
        if self.config.thumbwheel_invert:
            btn_tinv.add_css_class("selected")
        b_tinv = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        b_tinv.append(Gtk.Label(label="●" if self.config.thumbwheel_invert else "○"))
        b_tinv.append(Gtk.Label(label=_("Inverted")))
        btn_tinv.set_child(b_tinv)
        btn_tinv.connect("clicked", lambda b: self.set_thumb_direction(True))
        sec_tdir.append(btn_tinv)

        self.drawer_content.append(sec_tdir)

    def render_pointer_speed_drawer(self):
        """1:1 com Screenshot 2: Pointer speed"""
        self.drawer_title.set_label(_("Pointer speed"))

        # Descrição oficial
        desc_lbl = Gtk.Label(label=_("Work faster and more precisely with an 8K DPI sensor, allowing to adjust pointer speed and precision to match high resolution monitors."))
        desc_lbl.set_wrap(True)
        desc_lbl.add_css_class("callout-sub")
        desc_lbl.set_halign(Gtk.Align.START)
        self.drawer_content.append(desc_lbl)

        # Switch para estender alcance até 8K DPI
        row_8k = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_8k = Gtk.Label(label=_("Extend sensor range to 8K DPI"))
        lbl_8k.add_css_class("heading")
        lbl_8k.set_halign(Gtk.Align.START)
        row_8k.append(lbl_8k)

        sp_8k = Gtk.Box()
        sp_8k.set_hexpand(True)
        row_8k.append(sp_8k)

        sw_8k = Gtk.Switch()
        sw_8k.set_active(self.extend_8k)
        sw_8k.connect("notify::active", self.on_extend_8k_toggle)
        row_8k.append(sw_8k)
        self.drawer_content.append(row_8k)

        # Slider de Pointer speed
        sec_dpi = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        hdr_dpi = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        lbl_d = Gtk.Label(label=_("Pointer speed"))
        lbl_d.add_css_class("heading")
        lbl_d.set_halign(Gtk.Align.START)
        hdr_dpi.append(lbl_d)

        sp = Gtk.Box()
        sp.set_hexpand(True)
        hdr_dpi.append(sp)

        max_dpi = 8000 if self.extend_8k else 4000
        dpi_pct = int(round(self.config.dpi / float(max_dpi) * 100))
        dpi_pct = max(5, min(100, dpi_pct))

        self.dpi_pct_lbl = Gtk.Label(label=f"{dpi_pct}%")
        self.dpi_pct_lbl.add_css_class("heading")
        hdr_dpi.append(self.dpi_pct_lbl)
        sec_dpi.append(hdr_dpi)

        scale_dpi = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 200, max_dpi, 50)
        scale_dpi.set_value(min(self.config.dpi, max_dpi))
        scale_dpi.add_css_class("logi-scale")
        scale_dpi.connect("value-changed", self.on_dpi_scale_changed)
        sec_dpi.append(scale_dpi)
        self.drawer_content.append(sec_dpi)

    def on_extend_8k_toggle(self, switch, pspec):
        self.extend_8k = switch.get_active()
        self.update_drawer()

    def set_wheel_direction(self, invert: bool):
        self.config.hiresscroll_invert = invert
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()
        self.update_drawer()

    def set_thumb_direction(self, invert: bool):
        self.config.thumbwheel_invert = invert
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()
        self.update_drawer()

    def on_smooth_toggle(self, switch, pspec):
        self.config.hiresscroll_hires = switch.get_active()
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()

    def on_smartshift_toggle(self, switch, pspec):
        self.config.smartshift_on = switch.get_active()
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()
        self.update_drawer()

    def on_smartshift_sens_changed(self, scale):
        pct = int(scale.get_value())
        threshold = max(5, min(50, int(round(5 + (100 - pct) / 90.0 * 45))))
        self.config.smartshift_threshold = threshold
        if hasattr(self, 'sens_val_lbl'):
            self.sens_val_lbl.set_label(f"{pct}%")
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()

    def on_thumb_speed_changed(self, scale):
        pct = int(scale.get_value())
        interval = max(1, min(15, int(round(1 + (100 - pct) / 90.0 * 14))))
        self.config.thumbwheel_left_interval = interval
        self.config.thumbwheel_right_interval = interval
        if hasattr(self, 'speed_val_lbl'):
            self.speed_val_lbl.set_label(f"{pct}%")
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()

    def on_dpi_scale_changed(self, scale):
        val = int(scale.get_value())
        self.config.dpi = val
        max_dpi = 8000 if self.extend_8k else 4000
        pct = int(round(val / float(max_dpi) * 100))
        if hasattr(self, 'dpi_pct_lbl'):
            self.dpi_pct_lbl.set_label(f"{pct}%")
        self.mouse_canvas.update_subtitles()
        if self.on_changed:
            self.on_changed()
