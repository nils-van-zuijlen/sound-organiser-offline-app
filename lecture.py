#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from trans import parseTrans

class Lecture:
	""""""

	def __init__(self):
		""""""

		interface = Gtk.Builder()
		interface.add_from_file('glade_windows/lecture.glade')

		interface.connect_signals(self)

		self.mainWidget = interface.get_object('lecture')
		self.soundList = interface.get_object('soundList')
		self.projTitle = interface.get_object('projTitle')
		self.currentTitle = interface.get_object('currentTitle')
		self.currentDescr = interface.get_object('currentDescr')
		self.currentTrans = interface.get_object('currentTrans')
		self.nextTitle = interface.get_object('nextTitle')
		self.nextDescr = interface.get_object('nextDescr')
		self.nextTrans = interface.get_object('nextTrans')

	def on_playButton_clicked(self, label):
		""""""

		if label.get_text() == '⏸':
			label.set_text('⏵')
		else:
			label.set_text('⏸')

	def addSongToList(self, song):
		""""""

		self.soundList.pack_start(song.mainWidget, False, False, 0)

	def setTrans(self, where, trans):
		""""""

		if where == "current":
			self.currentTrans.set_text(parseTrans(trans))
			self.currentTrans.set_use_markup(True)
		elif where == "next":
			self.nextTrans.set_text(parseTrans(trans))
			self.nextTrans.set_use_markup(True)


if __name__ == "__main__":
	from main import SoundOrganiser
	lecture = Lecture()
	window = SoundOrganiser()
	window.setContent(lecture)
	lecture.setTrans("current", ["&", "", "ln"])
	lecture.setTrans("next", ["O", "n", "f"])
	Gtk.main()

#⏵⏸
