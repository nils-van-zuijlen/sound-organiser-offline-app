#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from trans import parseTrans

class Lecture:
	""""""

	def __init__(self, player):
		# Class vars
		self.player = None

		# Loading the GUI from file
		interface = Gtk.Builder()
		interface.add_from_file('glade_windows/lecture.glade')

		interface.connect_signals(self)

		# Setting the GUI vars
		self.mainWidget = interface.get_object('lecture')
		self.soundList = interface.get_object('soundList')
		self.projTitle = interface.get_object('projTitle')
		self.currentTitle = interface.get_object('currentTitle')
		self.currentDescr = interface.get_object('currentDescr')
		self._currentTrans = interface.get_object('currentTrans')
		self.nextTitle = interface.get_object('nextTitle')
		self.nextDescr = interface.get_object('nextDescr')
		self._nextTrans = interface.get_object('nextTrans')
		self._playerZone = interface.get_object('playerZone')

		# Setting the audio player
		self.setPlayer(player)

	def addSongToList(self, song):
		""""""

		self.soundList.pack_start(song.mainWidget, False, False, 0)

	def setPlayer(self, player):
		if self.player:
			for key, widget in enumerate(self._playerZone.get_children()):
				self._playerZone.remove(widget)
		self._playerZone.pack_start(player.mainWidget, True, True, 0)
		self.player = player

	def setTrans(self, where, trans):
		"""
		Sets the transition for the 'current' or 'next' song.

		`trans` must be an array allowed by trans.parseTrans
		"""

		if where == "current":
			self._currentTrans.set_text(parseTrans(trans))
			self._currentTrans.set_use_markup(True)
		elif where == "next":
			self._nextTrans.set_text(parseTrans(trans))
			self._nextTrans.set_use_markup(True)


if __name__ == "__main__":
	from window import Window
	from player import Player
	lecture = Lecture(Player())
	window = Window()
	window.setContent(lecture)
	lecture.setTrans("current", ["&", "", "ln"])
	lecture.setTrans("next", ["O", "n", "f"])
	Gtk.main()

#⏵⏸
