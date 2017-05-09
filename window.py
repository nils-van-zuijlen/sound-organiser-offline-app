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
	- mainBox:
		main GtkBox, it'll contain the menu bar and the playing or editing GUI
	- mainWidget:
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
		interface.add_from_file(realpath('glade_windows/principale.glade'))

		interface.connect_signals(self)

		self.mainBox = interface.get_object('mainBox')
		self.mainWidget = interface.get_object('mainWindow')

		self.mainWidget.maximize()

		self.parent = parent

	def setContent(self, content):
		"""
		Defines the main content of the window

		Can be the playing or editing GUI
		"""

		children = self.mainBox.get_children()
		if len(children) != 1:
			self.mainBox.remove(children[1])
		self.mainBox.pack_start(content.mainWidget, True, True, 0)

	def show(self):
		self.mainWidget.show_all()

	def on_mainWidget_destroy(self, widget):
		"""Exits from GTK's main loop on window's destroying"""

		# internal calls to close properly the current opened project
		self.parent.closeFile()

		# Exits the program
		Gtk.main_quit()

	def on_fullScreen_toggled(self, checkMenuItem):
		"""(Un)Fullscreens the app when the checkMenuItem changes state"""

		if checkMenuItem.get_active():
			self.mainWidget.fullscreen()
		else:
			self.mainWidget.unfullscreen()

	def on_openFile_activate(self, imageMenuItem):
		"""Opening of a file"""

		dialog = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN)
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
		dialog.set_transient_for(self.mainWidget)
		fileFilter = Gtk.FileFilter()
		fileFilter.add_pattern("*.theatre")
		dialog.add_filter(fileFilter)
		dialog.modal = True
		reponse = dialog.run()
		try:
			if reponse == Gtk.ResponseType.OK:
				self._openFileCallback(dialog.get_filename())
		finally:
			dialog.destroy()

	def on_recentChooserMenu_item_activated(self, recentChooserMenu):
		"""Opening of a recent file"""

		uri = recentChooserMenu.get_current_uri()
		print("uri: ", uri)
		filepath = parse.unquote(parse.urlsplit(uri).path)
		print("filepath: ", filepath)
		self._openFileCallback(filepath)

	def on_credits_activate(self, aboutDialog):
		"""Shows the aboutDialog"""

		aboutDialog.run()
		aboutDialog.hide()

	def _openFileCallback(self, filepath):
		"""Open file located at `filepath`"""

		if self.parent:
			self.parent.openFile(filepath)
		else:
			print("window callback")
			with open(filepath, "r") as file:
				print(">>>")
				print(json.load(file))
				print("<<<")

if __name__ == "__main__":
	Window()
	Gtk.main()
