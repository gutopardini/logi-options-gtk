"""
Canvas do MX Master 3S Oficial (1:1 com Logi Options+)
Render 3D em perspectiva, anéis de alvo circulares e callouts com ativação ciano
Suporta modo 'buttons' (6 pins de botões) e modo 'point_scroll' (3 pins: scroll, thumb, pointer).
"""

import os
import math
import cairo
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Gdk, GObject, GdkPixbuf

from ..i18n import _
from ..backend.keycodes import format_keys_display


class MouseCanvas(Gtk.Overlay):
    __gsignals__ = {
        'pin-selected': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, config_manager=None, mode="buttons"):
        super().__init__()
        self.config = config_manager
        self.mode = mode
        self.add_css_class("mouse-container")
        self.set_size_request(680, 560)
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.selected_pin = None

        # Carrega a Imagem 3D Oficial Transparente
        img_path = Path(__file__).parent.parent / "assets" / "mx_master_3s.png"
        if not img_path.exists():
            img_path = Path(__file__).parent.parent / "assets" / "mx_master_3s.jpg"
        
        self.pixbuf = None
        if img_path.exists():
            try:
                self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(img_path))
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")

        # Área de Desenho Cairo
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_draw_func(self.on_draw)
        self.set_child(self.drawing_area)

        # Definições de Callouts baseadas no modo
        if self.mode == "point_scroll":
            self.pins_def = {
                "scroll_wheel": {
                    "title": _("Scroll wheel"),
                    "default_sub": f"{_('Scroll direction')}: {_('Standard')}\n{_('Smooth scrolling')}: Off\nSmartShift: On",
                    "rx": 0.36, "ry": 0.22,
                    "tag_dx": 135, "tag_dy": -125
                },
                "thumb_wheel": {
                    "title": _("Thumb wheel"),
                    "default_sub": f"{_('Speed')}: 50%\n{_('Scroll direction')}: {_('Default')}",
                    "rx": 0.36, "ry": 0.47,
                    "tag_dx": -240, "tag_dy": 15
                },
                "pointer_speed": {
                    "title": _("Pointer speed"),
                    "default_sub": f"{_('Speed')}: 50%",
                    "rx": 0.48, "ry": 0.38,
                    "tag_dx": 135, "tag_dy": 25
                }
            }
        else:
            self.pins_def = {
                "btn_middle": {
                    "title": _("Middle button"),
                    "default_sub": _("Wheel button"),
                    "rx": 0.36, "ry": 0.22,
                    "tag_dx": 130, "tag_dy": -125
                },
                "btn_top": {
                    "title": _("Shift wheel mode"),
                    "default_sub": _("Top button"),
                    "rx": 0.48, "ry": 0.29,
                    "tag_dx": 135, "tag_dy": -55
                },
                "thumbwheel": {
                    "title": _("Horizontal scroll"),
                    "default_sub": _("Thumb wheel"),
                    "rx": 0.36, "ry": 0.47,
                    "tag_dx": 135, "tag_dy": 20
                },
                "btn_forward": {
                    "title": _("Forward"),
                    "default_sub": _("Forward button"),
                    "rx": 0.32, "ry": 0.51,
                    "tag_dx": -230, "tag_dy": -25
                },
                "btn_back": {
                    "title": _("Back"),
                    "default_sub": _("Back button"),
                    "rx": 0.39, "ry": 0.55,
                    "tag_dx": 20, "tag_dy": 110
                },
                "btn_gesture": {
                    "title": _("Gestures"),
                    "default_sub": f"{_('Virtual desktops')}\n{_('Thumb button')}",
                    "rx": 0.32, "ry": 0.73,
                    "tag_dx": -240, "tag_dy": 50
                },
            }

        # Layout Fixo para os botões de Callout
        self.fixed = Gtk.Fixed()
        self.add_overlay(self.fixed)

        self.callout_widgets = {}
        for pin_id, info in self.pins_def.items():
            btn = Gtk.Button()
            btn.add_css_class("callout-badge")
            
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            title_lbl = Gtk.Label(label=info["title"])
            title_lbl.add_css_class("callout-title")
            title_lbl.set_halign(Gtk.Align.START)
            box.append(title_lbl)

            sub_lbl = Gtk.Label(label=info["default_sub"])
            sub_lbl.add_css_class("callout-sub")
            sub_lbl.set_halign(Gtk.Align.START)
            box.append(sub_lbl)

            btn.set_child(box)
            btn.connect("clicked", self.create_pin_callback(pin_id))
            self.fixed.put(btn, 0, 0)
            self.callout_widgets[pin_id] = {
                "btn": btn,
                "title_lbl": title_lbl,
                "sub_lbl": sub_lbl
            }

        self.drawing_area.connect("resize", self.on_resize)
        self.update_subtitles()
        self.select_pin(None)

    def update_subtitles(self):
        if not self.config:
            return

        if self.mode == "point_scroll":
            # 1. Scroll wheel
            if "scroll_wheel" in self.callout_widgets:
                direction_str = _("Inverted") if self.config.hiresscroll_invert else _("Standard")
                smooth_str = "On" if self.config.hiresscroll_hires else "Off"
                smart_str = "On" if self.config.smartshift_on else "Off"
                self.callout_widgets["scroll_wheel"]["title_lbl"].set_label(_("Scroll wheel"))
                self.callout_widgets["scroll_wheel"]["sub_lbl"].set_label(
                    f"{_('Scroll direction')}: {direction_str}\n{_('Smooth scrolling')}: {smooth_str}\nSmartShift: {smart_str}"
                )

            # 2. Thumb wheel
            if "thumb_wheel" in self.callout_widgets:
                tdir_str = _("Inverted") if self.config.thumbwheel_invert else _("Default")
                tspeed_pct = int(round(100 - (self.config.thumbwheel_left_interval - 1) / 14.0 * 90))
                tspeed_pct = max(10, min(100, tspeed_pct))
                self.callout_widgets["thumb_wheel"]["title_lbl"].set_label(_("Thumb wheel"))
                self.callout_widgets["thumb_wheel"]["sub_lbl"].set_label(
                    f"{_('Speed')}: {tspeed_pct}%\n{_('Scroll direction')}: {tdir_str}"
                )

            # 3. Pointer speed
            if "pointer_speed" in self.callout_widgets:
                dpi_pct = int(round(self.config.dpi / 8000.0 * 100))
                dpi_pct = max(5, min(100, dpi_pct))
                self.callout_widgets["pointer_speed"]["title_lbl"].set_label(_("Pointer speed"))
                self.callout_widgets["pointer_speed"]["sub_lbl"].set_label(
                    f"{_('Speed')}: {dpi_pct}%"
                )
            return

        # Modo Buttons (Padrão)
        # Middle (Wheel button)
        if "btn_middle" in self.callout_widgets:
            if self.config.btn_middle_action == "ToggleSmartShift":
                self.callout_widgets["btn_middle"]["title_lbl"].set_label(_("Shift wheel mode"))
            elif not self.config.btn_middle_keys or self.config.btn_middle_action == "default":
                self.callout_widgets["btn_middle"]["title_lbl"].set_label(_("Middle button"))
            elif self.config.btn_middle_keys == ["KEY_LEFTMETA"]:
                self.callout_widgets["btn_middle"]["title_lbl"].set_label(_("Task view"))
            elif self.config.btn_middle_keys == ["KEY_LEFTMETA", "KEY_D"]:
                self.callout_widgets["btn_middle"]["title_lbl"].set_label(_("Show/hide desktop"))
            else:
                self.callout_widgets["btn_middle"]["title_lbl"].set_label(format_keys_display(self.config.btn_middle_keys))
            self.callout_widgets["btn_middle"]["sub_lbl"].set_label(_("Wheel button"))

        # Top Button
        if "btn_top" in self.callout_widgets:
            if self.config.btn_top_action == "ToggleSmartShift" or not self.config.btn_top_keys:
                self.callout_widgets["btn_top"]["title_lbl"].set_label(_("Shift wheel mode"))
            elif self.config.btn_top_keys == ["KEY_LEFTMETA"]:
                self.callout_widgets["btn_top"]["title_lbl"].set_label(_("Task view"))
            elif self.config.btn_top_keys == ["KEY_PRINT"]:
                self.callout_widgets["btn_top"]["title_lbl"].set_label(_("Print screen"))
            else:
                self.callout_widgets["btn_top"]["title_lbl"].set_label(format_keys_display(self.config.btn_top_keys))
            self.callout_widgets["btn_top"]["sub_lbl"].set_label(_("Top button"))

        # Thumbwheel
        if "thumbwheel" in self.callout_widgets:
            if not self.config.thumbwheel_divert:
                self.callout_widgets["thumbwheel"]["title_lbl"].set_label(_("Horizontal scroll"))
                self.callout_widgets["thumbwheel"]["sub_lbl"].set_label(_("Thumb wheel"))
            elif self.config.thumbwheel_right_keys == ["KEY_LEFTCTRL", "KEY_PAGEDOWN"]:
                self.callout_widgets["thumbwheel"]["title_lbl"].set_label(_("Navigate between tabs"))
                self.callout_widgets["thumbwheel"]["sub_lbl"].set_label(_("Thumb wheel"))
            elif self.config.thumbwheel_right_keys == ["KEY_VOLUMEUP"]:
                self.callout_widgets["thumbwheel"]["title_lbl"].set_label(_("Volume up/down"))
                self.callout_widgets["thumbwheel"]["sub_lbl"].set_label(_("Thumb wheel"))
            elif self.config.thumbwheel_right_keys == ["KEY_LEFTCTRL", "KEY_EQUAL"]:
                self.callout_widgets["thumbwheel"]["title_lbl"].set_label(_("Zoom in/out"))
                self.callout_widgets["thumbwheel"]["sub_lbl"].set_label(_("Thumb wheel"))
            else:
                left_str = format_keys_display(self.config.thumbwheel_left_keys) if self.config.thumbwheel_left_keys else _("None")
                right_str = format_keys_display(self.config.thumbwheel_right_keys) if self.config.thumbwheel_right_keys else _("None")
                self.callout_widgets["thumbwheel"]["title_lbl"].set_label(_("Keyboard shortcut"))
                self.callout_widgets["thumbwheel"]["sub_lbl"].set_label(f"{left_str}, {right_str}\n{_('Thumb wheel up')}, {_('Thumb wheel down')}")

        # Forward
        if "btn_forward" in self.callout_widgets:
            if self.config.btn_forward_keys == ["KEY_FORWARD"]:
                self.callout_widgets["btn_forward"]["title_lbl"].set_label(_("Forward"))
            elif self.config.btn_forward_keys == ["KEY_LEFTCTRL", "KEY_V"]:
                self.callout_widgets["btn_forward"]["title_lbl"].set_label(_("Paste"))
            elif self.config.btn_forward_keys == ["KEY_VOLUMEUP"]:
                self.callout_widgets["btn_forward"]["title_lbl"].set_label(_("Volume up"))
            elif self.config.btn_forward_keys == ["KEY_LEFTCTRL", "KEY_Y"]:
                self.callout_widgets["btn_forward"]["title_lbl"].set_label(_("Redo"))
            else:
                self.callout_widgets["btn_forward"]["title_lbl"].set_label(format_keys_display(self.config.btn_forward_keys))
            self.callout_widgets["btn_forward"]["sub_lbl"].set_label(_("Forward button"))

        # Back
        if "btn_back" in self.callout_widgets:
            if self.config.btn_back_keys == ["KEY_BACK"]:
                self.callout_widgets["btn_back"]["title_lbl"].set_label(_("Back"))
            elif self.config.btn_back_keys == ["KEY_LEFTCTRL", "KEY_C"]:
                self.callout_widgets["btn_back"]["title_lbl"].set_label(_("Copy"))
            elif self.config.btn_back_keys == ["KEY_VOLUMEDOWN"]:
                self.callout_widgets["btn_back"]["title_lbl"].set_label(_("Volume down"))
            elif self.config.btn_back_keys == ["KEY_LEFTCTRL", "KEY_Z"]:
                self.callout_widgets["btn_back"]["title_lbl"].set_label(_("Undo"))
            else:
                self.callout_widgets["btn_back"]["title_lbl"].set_label(format_keys_display(self.config.btn_back_keys))
            self.callout_widgets["btn_back"]["sub_lbl"].set_label(_("Back button"))

        # Gesture
        if "btn_gesture" in self.callout_widgets:
            if self.config.gesture_mode == "keypress":
                self.callout_widgets["btn_gesture"]["title_lbl"].set_label(_("Keyboard shortcut"))
                self.callout_widgets["btn_gesture"]["sub_lbl"].set_label(f"{format_keys_display(self.config.gesture_single_keys)}\n{_('Thumb button')}")
            else:
                preset_name = _("Virtual desktops")
                if self.config.gesture_up_keys == ["KEY_VOLUMEUP"]:
                    preset_name = _("Media controls")
                elif self.config.gesture_left_keys == ["KEY_LEFTMETA", "KEY_LEFT"]:
                    preset_name = _("Windows management")
                elif self.config.gesture_left_keys == ["KEY_LEFTALT", "KEY_LEFTSHIFT", "KEY_TAB"]:
                    preset_name = _("App navigation")
                elif self.config.gesture_up_keys == ["KEY_UP"]:
                    preset_name = _("Pan")
                
                self.callout_widgets["btn_gesture"]["title_lbl"].set_label(_("Gestures"))
                self.callout_widgets["btn_gesture"]["sub_lbl"].set_label(f"{preset_name}\n{_('Thumb button')}")

    def create_pin_callback(self, pin_id):
        def cb(button):
            self.select_pin(pin_id)
        return cb

    def select_pin(self, pin_id):
        self.selected_pin = pin_id
        for pid, data in self.callout_widgets.items():
            if pid == pin_id and pin_id is not None:
                data["btn"].add_css_class("active")
            else:
                data["btn"].remove_css_class("active")
        self.drawing_area.queue_draw()
        if pin_id is not None:
            self.emit('pin-selected', pin_id)

    def on_resize(self, area, width, height):
        cx = width * 0.48
        cy = height * 0.50
        scale = max(0.85, min(width, height) / 560.0)

        for pin_id, info in self.pins_def.items():
            data = self.callout_widgets[pin_id]
            px = int(cx + info["tag_dx"] * scale)
            py = int(cy + info["tag_dy"] * scale)
            self.fixed.move(data["btn"], px, py)

    def on_draw(self, area, cr, width, height):
        cr.set_source_rgb(0.055, 0.06, 0.07)
        cr.paint()

        cx = width * 0.48
        cy = height * 0.50
        img_size = min(width, height) * 0.88
        scale = img_size / 512.0

        # Desenha a Imagem 3D Oficial
        if self.pixbuf:
            scaled_pb = self.pixbuf.scale_simple(
                int(img_size), int(img_size), GdkPixbuf.InterpType.BILINEAR
            )
            if scaled_pb:
                Gdk.cairo_set_source_pixbuf(cr, scaled_pb, cx - img_size / 2, cy - img_size / 2)
                cr.paint()

        # Desenha Linhas e Anéis de Alvo Oficiais
        for pin_id, info in self.pins_def.items():
            is_active = (self.selected_pin == pin_id)
            
            target_x = cx - img_size / 2 + info["rx"] * img_size
            target_y = cy - img_size / 2 + info["ry"] * img_size

            tag_scale = max(0.85, min(width, height) / 560.0)
            tag_x = cx + info["tag_dx"] * tag_scale + (40 if info["tag_dx"] > 0 else 65)
            tag_y = cy + info["tag_dy"] * tag_scale + 18

            cr.save()

            if is_active:
                cr.set_source_rgba(0.0, 0.90, 0.79, 0.95)
                cr.set_line_width(2.0)
            else:
                cr.set_source_rgba(1.0, 1.0, 1.0, 0.45)
                cr.set_line_width(1.2)

            cr.move_to(target_x, target_y)
            mid_x = (target_x + tag_x) * 0.5
            cr.curve_to(mid_x, target_y, mid_x, tag_y, tag_x, tag_y)
            cr.stroke()

            # Anel Circular Oficial
            cr.arc(target_x, target_y, 7.5 if is_active else 6.0, 0, 2 * math.pi)
            if is_active:
                cr.set_source_rgba(0.0, 0.90, 0.79, 0.35)
                cr.fill_preserve()
                cr.set_source_rgb(0.0, 0.90, 0.79)
                cr.set_line_width(2.4)
            else:
                cr.set_source_rgba(0.0, 0.0, 0.0, 0.35)
                cr.fill_preserve()
                cr.set_source_rgb(1.0, 1.0, 1.0)
                cr.set_line_width(1.8)
            cr.stroke()

            cr.restore()
