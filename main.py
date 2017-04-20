#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SoundOrganiser:
	"""
	Classe de la fenêtre principale

	Attributs:
	- mainBox:
		GtkBox principale, c'est elle qui contiendra la barre de menu et le contenu
	- mainWidget:
		GtkWindow principale, il s'agit de la fenêtre de l'application
	"""

	def __init__(self):
		"""Récupération et instanciation d'une GtkWindow en fonction du template principal"""

		interface = Gtk.Builder()
		interface.add_from_file('glade_windows/principale.glade')

		interface.connect_signals(self)

		self.mainBox = interface.get_object('mainBox')
		self.mainWidget = interface.get_object('mainWindow')

	def setContent(self, content):
		"""
		Définit le contenu principal de la fenêtre

		Peut être l'interface de lecture ou d'édition
		"""

		children = self.mainBox.get_children()
		if len(children) != 1:
			self.mainBox.remove(children[1])
		self.mainBox.pack_start(content.mainWidget, True, True, 0)

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

if __name__ == "__main__":
	SoundOrganiser()
	Gtk.main()
