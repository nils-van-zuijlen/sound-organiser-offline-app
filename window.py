#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
import json
from urllib import parse
from os.path import realpath
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from lecture import Lecture
from editor import Editor

class Window(object):
    """
    Main window's class

    Properties:
    - main_box:
        main GtkBox, it'll contain the menu bar and the playing or editing GUI
    - main_widget:
        main GtkWindow, the app's window
    - parent:
        Null or app defined in app.py
        Has method `openFile(filepath)`.
    """

    def __init__(self, parent=None):
        """
        Creates the main GtkWindow from template

        `parent` is the app stored in app.py
        """
        interface = Gtk.Builder()
        interface.add_from_file(realpath('glade_windows/window.glade'))

        interface.connect_signals(self)

        self.main_box = interface.get_object('main_box')
        self.main_widget = interface.get_object('main_window')
        self.lecture_placeholder = interface.get_object('lecture_placeholder')
        self.editor_placeholder = interface.get_object('editor_placeholder')
        self.close_with_edited_file_dialog = interface.get_object(
            'close_with_edited_file_dialog')

        self.main_widget.maximize()

        self.parent = parent

    def set_content(self, content):
        """
        Defines the main content of the window

        Can be the playing or editing GUI
        """
        if isinstance(content, Lecture):
            self.lecture_placeholder.pack_start(content.main_widget, True, True, 0)
            content.parent = self
        elif isinstance(content, Editor):
            self.editor_placeholder.pack_start(content.main_widget, True, True, 0)
            content.parent = self

    def show(self):
        self.main_widget.show_all()

    @staticmethod
    def on_close_without_saving_clicked(widget):
        """Send a REJECT response to the widget"""
        widget.response(Gtk.ResponseType.REJECT)

    @staticmethod
    def on_cancel_close_clicked(widget):
        """Send a CANCEL response to the widget"""
        widget.response(Gtk.ResponseType.CANCEL)

    @staticmethod
    def on_save_before_closing_clicked(widget):
        """Send a ACCEPT response to the widget"""
        widget.response(Gtk.ResponseType.ACCEPT)

    def on_main_widget_destroy(self, _):
        """Exits from GTK's main loop on window's destroying"""

        # internal calls to close properly the current opened project
        try:
            self.parent.close_file()
        finally:
            # Exits the program
            Gtk.main_quit()

    def on_gtk_close_activate(self, _):
        """Close the current project without exitting the app"""
        self.parent.close_file()

    def on_full_screen_toggled(self, check_menu_item):
        """(Un)Fullscreens the app when the check_menu_item changes state"""
        if check_menu_item.get_active():
            self.main_widget.fullscreen()
        else:
            self.main_widget.unfullscreen()

    def on_open_file_activate(self, _):
        """Opening of a file"""
        dialog = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog.set_transient_for(self.main_widget)
        file_filter = Gtk.FileFilter()
        file_filter.add_pattern("*.theatre")
        dialog.add_filter(file_filter)
        dialog.modal = True
        answer = dialog.run()
        try:
            if answer == Gtk.ResponseType.OK:
                self._open_file_callback(dialog.get_filename())
        finally:
            dialog.destroy()

    def on_recent_chooser_menu_item_activated(self, recent_chooser_menu):
        """Opening of a recent file"""
        uri = recent_chooser_menu.get_current_uri()
        print("uri: ", uri)
        filepath = parse.unquote(parse.urlsplit(uri).path)
        print("filepath: ", filepath)
        self._open_file_callback(filepath)

    @staticmethod
    def on_credits_activate(about_dialog):
        """Shows the about_dialog"""
        about_dialog.run()
        about_dialog.hide()

    def _open_file_callback(self, filepath):
        """Open file located at `filepath`"""
        if self.parent:
            self.parent.open_file(filepath)
        else:
            print("window callback")
            with open(filepath, "r") as file_queried:
                print(">>>")
                print(json.load(file_queried))
                print("<<<")

    def on_active_tab_changed(self, _, __, page_number):
        """When the user changes active tab"""
        if page_number:
            self.parent.switch_to_edit_mode()
        else:
            self.parent.switch_to_playing_mode()

if __name__ == "__main__":
    print("Please run app.py")
