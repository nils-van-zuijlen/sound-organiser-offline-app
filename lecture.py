#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
from os.path import realpath
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from trans import parseTrans
from son_en_liste import SonEnListe

class Lecture:
	""""""

	def __init__(self, player=None):
		# Class vars
		self.player = None

		# Loading the GUI from file
		interface = Gtk.Builder()
		interface.add_from_file(realpath('glade_windows/lecture.glade'))

		interface.connect_signals(self)

		# Setting the GUI vars
		self.mainWidget = interface.get_object('lecture')
		self.projTitle = interface.get_object('projTitle')
		self._currentTitle = interface.get_object('currentTitle')
		self._currentDescr = interface.get_object('currentDescr')
		self._currentTrans = interface.get_object('currentTrans')
		self._nextSong = interface.get_object('nextSongBox')
		self._nextTitle = interface.get_object('nextTitle')
		self._nextDescr = interface.get_object('nextDescr')
		self._nextTrans = interface.get_object('nextTrans')
		self._playerZone = interface.get_object('playerZone')

		self.songList = Gtk.Box.new(Gtk.Orientation.VERTICAL, 3)
		interface.get_object('songScroll').add(self.songList)
		self.songList.show()
		

		# Setting the audio player
		if player:
			self.setPlayer(player)

	def addSongToList(self, song):
		""""""

		self.songList.pack_start(song.mainWidget, False, False, 0)

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

	def setProjTitle(self, projTitle):
		self.projTitle.set_text(projTitle)

	def setCurrentSong(self, song):
		self.setTrans("current", song["trans"])
		self._currentTitle.set_text(song["name"])
		self._currentDescr.set_text(song["descr"])
		if self.player:
			self.player.stop()
			self.player.setFilepath(self.project["path"], song["file"])
			self.player.setVolume(song["vol"])

	def setNextSong(self, song=None):
		if song:
			self.setTrans("next", song["trans"])
			self._nextTitle.set_text(song["name"])
			self._nextDescr.set_text(song["descr"])
		else:
			self._nextTrans.set_text("")
			self._nextTitle.set_text("")
			self._nextDescr.set_text("")

	def selectSong(self, songDict):
		songs = self.project["songs"]
		if songs.count(songDict) > 0:
			index = songs.index(songDict)
			self.setCurrentSong(songs[index])
			if len(songs) > index+1:
				self.setNextSong(songs[index+1])
			else:
				self.setNextSong(None)

	def openProj(self, project):
		self.project = project
		self.setProjTitle(project["name"])
		for song in project["songs"]:
			self.addSongToList(SonEnListe(song, self))
		if len(project["songs"]) > 0:
			self.setCurrentSong(project["songs"][0])
			if len(project["songs"]) > 1:
				self.setNextSong(project["songs"][1])


if __name__ == "__main__":
	from window import Window
	lecture = Lecture()
	window = Window()
	window.setContent(lecture)
	lecture.setTrans("current", ["&", "", "ln"])
	lecture.setTrans("next", ["O", "n", "f"])
	Gtk.main()
