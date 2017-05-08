#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
from os.path import realpath
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from trans import parseTrans

class SonEnListe:
	"""Ligne de la liste des sons."""

	def __init__(self, songDict, parent = None):
		self.parent = parent

		interface = Gtk.Builder()
		interface.add_from_file(realpath('glade_windows/son_en_liste.glade'))

		interface.connect_signals(self)

		self.mainWidget = interface.get_object('song')
		self.songLabel = interface.get_object('label')

		self.songDict = songDict
		self.songDict["parsedTrans"] = parseTrans(self.songDict["trans"])
		self._setLabel()

	def on_song_clicked(self, label):
		""""""

		print("song {} clicked.".format(self.songDict["name"]))
		if self.parent:
			self.parent.selectSong(self.songDict)

	def setTrans(self, transition):
		"""
		Sets the transition of the song
		
		trans is an array with 3 transcodes
		"""

		self.songDict["parsedTrans"] = parseTrans(transition)
		self.songDict["trans"] = transition

	def _setLabel(self):
		text = "<b>"
		text += self.songDict["name"]
		text += "</b> <i>"
		text += self.songDict["descr"]
		text += "</i> "
		text += self.songDict["parsedTrans"]
		self.songLabel.set_text(text)
		self.songLabel.set_use_markup(True)

if __name__ == "__main__":
	from window import Window
	from lecture import Lecture
	lecture = Lecture()
	window = Window()
	song = {"name": "songTitle", "descr": "songDescr", "trans": ["1", "", "s"]}
	lecture.addSongToList(SonEnListe(song))
	window.setContent(lecture)
	Gtk.main()
