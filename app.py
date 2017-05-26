#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import os
import sys
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import lecture
import player
import window

class Main:
	"""Main class for the app"""

	def __init__(self):
		self.window = window.Window(parent=self)
		self.lecture = lecture.Lecture()
		self.player = player.Player()
		self.songs = []
		self.filepath = ""

		self.window.set_content(self.lecture)
		self.lecture.set_player(self.player)
		self.window.show()

	def open_file(self, filepath):
		"""Opens the file located at `filepath`"""
		if self.filepath:
			self.close_file()
		if os.path.exists(filepath):
			self.filepath = os.path.realpath(filepath)
			with open(self.filepath, "r") as file:
				self.project = json.load(file)
				if (not "path" in self.project) or (not self.project["path"]):
					self.project["path"] = os.path.dirname(self.filepath)
				self.lecture.open_project(self.project)

	def close_file(self):
		"""Will close the opened project"""
		self.lecture.close_project()
		self.filepath = ""

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		args = sys.argv[1:]
		filepath = os.path.join(os.getcwd(), args[-1])
		app = Main()
		try:
			app.open_file(filepath)
		except:
			print("Failed to open file {}".format(filepath))
		Gtk.main()
	else:
		Main()
		Gtk.main()
