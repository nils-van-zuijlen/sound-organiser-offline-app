#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
from os.path import realpath
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import parse_to_pango as ptp
from song_list_item import SongListItem

class Lecture:
	"""Playing GUI"""

	def __init__(self, player=None):
		# Class vars
		self.player = None
		self.songs = []
		self.project = None

		# Loading the GUI from file
		interface = Gtk.Builder()
		interface.add_from_file(realpath('glade_windows/lecture.glade'))

		interface.connect_signals(self)

		# Setting the GUI vars
		self.main_widget = interface.get_object('lecture')
		self.proj_title = interface.get_object('proj_title')
		self._current_title = interface.get_object('current_title')
		self._current_descr = interface.get_object('current_descr')
		self._current_trans = interface.get_object('current_trans')
		self._next_song = interface.get_object('next_song_box')
		self._next_title = interface.get_object('next_title')
		self._next_descr = interface.get_object('next_descr')
		self._next_trans = interface.get_object('next_trans')
		self._player_zone = interface.get_object('player_zone')

		self.song_list = Gtk.Box.new(Gtk.Orientation.VERTICAL, 3)
		interface.get_object('song_scroll').add(self.song_list)
		self.song_list.show()
		

		# Setting the audio player
		if player:
			self.set_player(player)

	def add_song_to_list(self, song):
		"""
		Adds a song to the song_list

		`song` is a SongListItem
		"""
		self.song_list.pack_start(song.main_widget, False, False, 0)
		self.songs.append(song)

	def set_player(self, player):
		"""
		Sets the player

		`player` may be a Player defined in player.py
		"""
		if self.player:
			for key, widget in enumerate(self._player_zone.get_children()):
				self._player_zone.remove(widget)
		self._player_zone.pack_start(player.main_widget, True, True, 0)
		self.player = player

	def _set_trans(self, where, trans):
		"""
		Sets the transition for the 'current' or 'next' song.

		`trans` must be an array allowed by parse_to_pango.parse_trans
		"""
		if where == "current":
			self._current_trans.set_text(ptp.parse_trans(trans))
			self._current_trans.set_use_markup(True)
		elif where == "next":
			self._next_trans.set_text(ptp.parse_trans(trans))
			self._next_trans.set_use_markup(True)

	def set_proj_title(self, proj_title):
		"""Sets the GUI project title"""
		self.proj_title.set_text(proj_title)

	def set_current_song(self, song):
		"""
		Sets the current song

		Stops the previous song and loads the new song in the player
		Shows its characteristics in the GUI
		"""
		self._set_trans("current", song["trans"])
		self._current_title.set_text(song["name"])
		self._current_descr.set_text(song["descr"])
		if self.player:
			self.player.stop()
			self.player.set_filepath(self.project["path"], song["file"])
			self.player.set_volume(song["vol"])

	def set_next_song(self, song=None):
		"""
		Sets the next song.

		Shows its characteristics in the GUI.
		If `song == None`, the GUI labels are cleared.
		"""
		if song:
			self._set_trans("next", song["trans"])
			self._next_title.set_text(song["name"])
			self._next_descr.set_text(song["descr"])
		else:
			self._next_trans.set_text("")
			self._next_title.set_text("")
			self._next_descr.set_text("")

	def select_song(self, song_dict):
		"""
		Selects song with its dictionary

		Sets the current and next song if possible.
		"""
		songs = self.project["songs"]
		if songs.count(song_dict) > 0:
			index = songs.index(song_dict)
			self.set_current_song(songs[index])
			if len(songs) > index+1:
				self.set_next_song(songs[index+1])
			else:
				self.set_next_song(None)

	def open_project(self, project):
		"""
		Opens a project when its dictionary is passed as argument
		"""
		self.project = project
		self.set_proj_title(project["name"])
		for song in project["songs"]:
			self.add_song_to_list(SongListItem(song, self))
		if len(project["songs"]) > 0:
			self.set_current_song(project["songs"][0])
			if len(project["songs"]) > 1:
				self.set_next_song(project["songs"][1])
			else:
				self.set_next_song(None)

	def close_project(self):
		self.player.reset()
		self.project = None
		for child in self.song_list.get_children():
			child.destroy()
		self.songs = []
		self.set_proj_title("")
		self._current_trans.set_text("")
		self._current_title.set_text("")
		self._current_descr.set_text("")
		self._next_trans.set_text("")
		self._next_title.set_text("")
		self._next_descr.set_text("")

if __name__ == "__main__":
	from window import Window
	lecture = Lecture()
	window = Window()
	window.setContent(lecture)
	lecture._set_trans("current", ["&", "", "ln"])
	lecture._set_trans("next", ["O", "n", "f"])
	Gtk.main()
