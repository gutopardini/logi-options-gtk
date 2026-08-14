#!/usr/bin/env python3
"""
Logi Options+ para Linux (GTK4 + Libadwaita)
Ponto de Entrada Principal
"""

import sys
import os
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk, GLib

from app.window import MainWindow

APP_ID = "io.github.pixlone.logioptions.gtk"


class LogiOptionsApp(Adw.Application):
    def __init__(self):
        GLib.set_prgname("io.github.pixlone.logioptions.gtk")
        GLib.set_application_name("Logi Options+")
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

    def do_startup(self):
        Adw.Application.do_startup(self)
        self.load_custom_css()
        self.load_custom_icons()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
            win.set_icon_name("logi-options-plus")
        win.present()

    def load_custom_icons(self):
        assets_dir = Path(__file__).parent / "app" / "assets"
        display = Gdk.Display.get_default()
        if display:
            theme = Gtk.IconTheme.get_for_display(display)
            theme.add_search_path(str(assets_dir))

    def load_custom_css(self):
        css_path = Path(__file__).parent / "app" / "assets" / "style.css"
        if css_path.exists():
            provider = Gtk.CssProvider()
            provider.load_from_path(str(css_path))
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )


def main():
    app = LogiOptionsApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
