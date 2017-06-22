#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
import json
import re
from urllib import parse
from os.path import realpath
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Window:
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

		self.main_widget.maximize()

		self.parent = parent

	def set_content(self, content):
		"""
		Defines the main content of the window

		Can be the playing or editing GUI
		"""
		children = self.main_box.get_children()
		if len(children) != 1:
			self.main_box.remove(children[1])
		self.main_box.pack_start(content.main_widget, True, True, 0)
		content.parent = self

	def show(self):
		self.main_widget.show_all()

	def on_main_widget_destroy(self, widget):
		"""Exits from GTK's main loop on window's destroying"""

		# internal calls to close properly the current opened project
		try:
			self.parent.close_file()
		finally:
			# Exits the program
			Gtk.main_quit()

	def on_gtk_close_activate(self, widget):
		"""Close the current project without exitting the app"""
		self.parent.close_file()

	def on_full_screen_toggled(self, check_menu_item):
		"""(Un)Fullscreens the app when the check_menu_item changes state"""
		if check_menu_item.get_active():
			self.main_widget.fullscreen()
		else:
			self.main_widget.unfullscreen()

	def on_open_file_activate(self, image_menu_item):
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
			with open(filepath, "r") as file:
				print(">>>")
				print(json.load(file))
				print("<<<")

if __name__ == "__main__":
	Window().show()
	Gtk.main()
