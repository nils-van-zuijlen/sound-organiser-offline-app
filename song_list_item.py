#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
from os.path import realpath
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import parse_to_pango as ptp

class SongListItem:
	"""Song list item"""

	def __init__(self, song_dict, parent = None):
		self.parent = parent

		interface = Gtk.Builder()
		interface.add_from_file(realpath('glade_windows/song_list_item.glade'))

		interface.connect_signals(self)

		self.main_widget = interface.get_object('song')
		self.song_label = interface.get_object('label')

		self.song_dict = song_dict
		self.song_dict["parsed_trans"] = ptp.parse_trans(self.song_dict["trans"])
		self._set_label()

	def on_song_clicked(self, label):
		"""Loads the song in the player"""
		if self.parent:
			self.parent.select_song(self.song_dict)

	def on_song_destroy(self, widget):
		self.song_dict = {}
		self = None

	def set_trans(self, transition):
		"""
		Sets the transition of the song
		
		trans is an array allowed by parse_to_pango.parse_trans
		"""
		self.song_dict["parsed_trans"] = ptp.parse_trans(transition)
		self.song_dict["trans"] = transition

	def _set_label(self):
		"""
		Sets the GUI label

		With the vars `self.song_dict["name"]`, `self.song_dict["descr"]` and
		`self.song_dict["parsed_trans"]`.
		"""
		text = "<b>"
		text += ptp.escape_pango_chars(self.song_dict["name"])
		text += "</b> <i>"
		text += ptp.escape_pango_chars(self.song_dict["descr"])
		text += "</i> "
		text += self.song_dict["parsed_trans"]
		self.song_label.set_text(text)
		self.song_label.set_use_markup(True)

if __name__ == "__main__":
	from window import Window
	from lecture import Lecture
	lecture = Lecture()
	window = Window()
	song = {"name": "song_title", "descr": "song_descr", "trans": ["1", "", "s"]}
	lecture.add_song_to_list(SongListItem(song))
	window.set_content(lecture)
	Gtk.main()
