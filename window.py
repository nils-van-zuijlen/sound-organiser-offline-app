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
	Classe de la fenêtre principale

	Attributs:
	- mainBox:
		GtkBox principale, c'est elle qui contiendra la barre de menu et le
		contenu
	- mainWidget:
		GtkWindow principale, il s'agit de la fenêtre de l'application
	- parent:
		Null ou application.
		Possède une méthode `openFile(filepath)`.
	"""

	def __init__(self, parent=None):
		"""
		Récupération et instanciation d'une GtkWindow en fonction du template
		principal
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
		Définit le contenu principal de la fenêtre

		Peut être l'interface de lecture ou d'édition
		"""

		children = self.mainBox.get_children()
		if len(children) != 1:
			self.mainBox.remove(children[1])
		self.mainBox.pack_start(content.mainWidget, True, True, 0)

	def show(self):
		self.mainWidget.show_all()

	def on_mainWidget_destroy(self, widget):
		"""
		Gestion de l'évenement 'destruction' de la fenêtre

		Quitte la boucle principale de Gtk
		"""

		Gtk.main_quit()

	def on_fullScreen_toggled(self, checkMenuItem):
		"""
		Passage ou sortie du plein écran en fonction de l'état du checkMenuItem
		"""

		if checkMenuItem.get_active():
			self.mainWidget.fullscreen()
		else:
			self.mainWidget.unfullscreen()

	def on_openFile_activate(self, imageMenuItem):
		"""
		Ouverture d'un fichier
		"""

		dialog = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN)
		dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
		dialog.set_transient_for(self.mainWidget)
		fileFilter = Gtk.FileFilter()
		fileFilter.add_pattern("*.theatre")
		dialog.add_filter(fileFilter)
		dialog.modal = True
		reponse = dialog.run()
		if reponse == Gtk.ResponseType.OK:
			self._openFileCallback(dialog.get_filename())
		dialog.destroy()

	def on_recentChooserMenu_item_activated(self, recentChooserMenu):
		"""
		Ouverture d'un fichier récent
		"""

		uri = recentChooserMenu.get_current_uri()
		print("uri: ", uri)
		filepath = parse.unquote(parse.urlsplit(uri).path)
		print("filepath: ", filepath)
		self._openFileCallback(filepath)

	def on_credits_activate(self, aboutDialog):
		aboutDialog.run()
		aboutDialog.hide()

	def _openFileCallback(self, filepath):
		"""
		Ouvre le fichier `filepath`.
		"""

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
