#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from trans import parseTrans

class SonEnListe:
	"""Ligne de la liste des sons."""

	def __init__(self, uri, trans):
		""""""

		interface = Gtk.Builder()
		interface.add_from_file('glade_windows/son_en_liste.glade')

		interface.connect_signals(self)

		self.mainWidget = interface.get_object('song')
		self.songTitle = interface.get_object('songTitle')
		self.songDescr = interface.get_object('songDescr')
		self.songTrans = interface.get_object('songTrans')

		self.uri = int(uri)
		self.setTrans(trans)

	def on_song_clicked(self, label):
		""""""

		print("song {} clicked.".format(self.uri))

	def setTrans(self, trans):
		"""
		Sets the transition of the song
		
		trans is an array with 3 transcodes
		"""

		self.songTrans.set_text(parseTrans(trans))
		self.songTrans.set_use_markup(True)

if __name__ == "__main__":
	from window import Window
	from lecture import Lecture
	from player import Player
	lecture = Lecture(Player())
	window = Window()
	lecture.addSongToList(SonEnListe(1, ["#", "!ln", "!s"]))
	lecture.addSongToList(SonEnListe(2, ["1", "!q", "!ns"]))
	window.setContent(lecture)
	Gtk.main()
