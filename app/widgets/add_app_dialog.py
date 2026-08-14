"""
Diálogo Oficial de Seleção de Aplicativos (+ ADD APPLICATION)
Fiel aos Screenshots 3 e 5 da Logitech
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from ..backend.app_manager import AppManager


class AddAppDialog(Gtk.Window):
    def __init__(self, parent_window, on_apps_selected_cb):
        super().__init__(transient_for=parent_window, modal=True)
        self.set_title("Select Applications")
        self.set_default_size(520, 680)
        self.on_selected_cb = on_apps_selected_cb

        # Layout Principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        main_box.add_css_class("actions-drawer-container")
        self.set_child(main_box)

        # Cabeçalho
        title_lbl = Gtk.Label(label="Select Applications")
        title_lbl.add_css_class("drawer-title")
        title_lbl.set_halign(Gtk.Align.START)
        main_box.append(title_lbl)

        sub_lbl = Gtk.Label(label="Customize the buttons for your favorite applications to be even more efficient.")
        sub_lbl.add_css_class("callout-sub")
        sub_lbl.set_wrap(True)
        sub_lbl.set_halign(Gtk.Align.START)
        main_box.append(sub_lbl)

        # Campo de Busca
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.add_css_class("official-search-entry")
        self.search_entry.set_placeholder_text("Search applications...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        main_box.append(self.search_entry)

        # Scrolled Window para a Lista de Apps
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.apps_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        scroll.set_child(self.apps_container)
        main_box.append(scroll)

        # Carrega Aplicativos Instalados
        self.installed_apps = AppManager.get_installed_apps()
        self.selected_apps = {}
        self.checkbox_map = {}

        self.render_apps_list()

        # Botões Inferiores (CONFIRM e DISCARD)
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        btn_box.set_margin_top(8)

        confirm_btn = Gtk.Button(label="CONFIRM")
        confirm_btn.add_css_class("official-apply-btn")
        confirm_btn.connect("clicked", self.on_confirm_clicked)
        btn_box.append(confirm_btn)

        discard_btn = Gtk.Button(label="DISCARD")
        discard_btn.add_css_class("close-nav-btn")
        discard_btn.connect("clicked", lambda b: self.close())
        btn_box.append(discard_btn)

        main_box.append(btn_box)

    def render_apps_list(self, filter_text=""):
        while self.apps_container.get_first_child():
            self.apps_container.remove(self.apps_container.get_first_child())

        query = filter_text.strip().lower()

        # Categoria: Available Applications
        cat_lbl = Gtk.Label(label="INSTALLED APPLICATIONS")
        cat_lbl.add_css_class("category-header-label")
        cat_lbl.set_halign(Gtk.Align.START)
        self.apps_container.append(cat_lbl)

        for app in self.installed_apps:
            if query and query not in app["name"].lower():
                continue

            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.add_css_class("gesture-subrow")
            row.set_margin_top(2)
            row.set_margin_bottom(2)

            chk = Gtk.CheckButton()
            chk.set_active(app["name"] in self.selected_apps)
            chk.connect("toggled", self.create_chk_callback(app))
            self.checkbox_map[app["name"]] = chk
            row.append(chk)

            # Ícone do App
            if app["icon"].startswith("/"):
                img = Gtk.Image.new_from_file(app["icon"])
                img.set_pixel_size(24)
            else:
                img = Gtk.Image.new_from_icon_name(app["icon"])
                img.set_pixel_size(24)
            row.append(img)

            name_lbl = Gtk.Label(label=app["name"])
            name_lbl.add_css_class("heading")
            name_lbl.set_halign(Gtk.Align.START)
            row.append(name_lbl)

            self.apps_container.append(row)

    def create_chk_callback(self, app):
        def cb(chk):
            if chk.get_active():
                self.selected_apps[app["name"]] = app
            else:
                self.selected_apps.pop(app["name"], None)
        return cb

    def on_search_changed(self, entry):
        self.render_apps_list(entry.get_text())

    def on_confirm_clicked(self, btn):
        if self.on_selected_cb:
            self.on_selected_cb(list(self.selected_apps.values()))
        self.close()
