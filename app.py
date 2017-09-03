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
import editor

class Main(object):
	"""Main class for the app"""

	def __init__(self):
		self.window = window.Window(parent=self)
		self.lecture = lecture.Lecture()
		self.player = player.Player()
		self.editor = editor.Editor()
		self.songs = []
		self.project = {}
		self.filepath = ""
		self.current = self.lecture # the current mode

		self.lecture.set_player(self.player)

		self.window.set_content(self.lecture)
		self.window.set_content(self.editor)

		self.window.show()

	def open_file(self, filepath):
		"""Opens the file located at `filepath`"""
		if self.filepath:
			self.close_file()
		if os.path.exists(filepath):
			self.filepath = os.path.realpath(filepath)
			with open(self.filepath, "r") as file_queried:
				self.project = json.load(file_queried)
				if (not "path" in self.project) or (not self.project["path"]):
					self.project["path"] = os.path.dirname(self.filepath)
				self.current.open_project(self.project)

	def close_file(self):
		"""Will close the opened project"""
		self.current.close_project()
		self.filepath = ""

	def save_project(self, project, is_save_as=False):
		"""Save the project passed as argument"""
		if is_save_as or not self.filepath:
			file_filter = Gtk.FileFilter()
			file_filter.add_pattern("*.theatre")
			dialog = Gtk.FileChooserDialog(parent=window.main_widget,
				action=Gtk.FileChooserAction.SAVE, do_overwrite_confirmation=True,
				filter=file_filter)
			if is_save_as:
				dialog.set_filename(self.filepath)
			else:
				dialog.set_current_filename("Nouveau projet.theatre")
			dialog.run()
			self.filepath = os.path.realpath(dialog.get_filename())
			dialog.destroy()

		with open(self.filepath, "w") as file_queried:
			json.dump(project, file_queried)

	def switch_to_edit_mode(self):
		"""Switches the interface from playing mode to editing mode."""
		self.lecture.close_project()
		self.editor.open_project(self.project)
		self.current = self.editor

	def switch_to_playing_mode(self):
		"""Switches the interface from editing mode to playing mode."""
		self.editor.close_project()
		self.lecture.open_project(self.project)
		self.current = self.lecture

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		args = sys.argv[1:]
		filepath = os.path.join(os.getcwd(), args[-1])
		app = Main()
		try:
			app.open_file(filepath)
		except:
			print("Failed to open file {}".format(filepath))
			app.close_file()
		Gtk.main()
	else:
		Main()
		Gtk.main()
