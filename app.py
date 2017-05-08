#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import os
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import lecture
import son_en_liste
import player
import window

class Main:
	def __init__(self):
		self.window = window.Window(parent=self)
		self.lecture = lecture.Lecture()
		self.player = player.Player()
		self.songs = []
		self.filepath = False

		self.window.setContent(self.lecture)
		self.lecture.setPlayer(self.player)
		self.window.show()

	def openFile(self, filepath):
		if self.filepath:
			self.closeFile()
		if os.path.exists(filepath):
			self.filepath = os.path.realpath(filepath)
			with open(self.filepath, "r") as file:
				self.project = json.load(file)
				if not "path" in self.project:
					self.project["path"] = os.path.dirname(self.filepath)
				self.lecture.openProj(self.project)

	def closeFile(self):
		pass


if __name__ == '__main__':
	Main()
	Gtk.main()
