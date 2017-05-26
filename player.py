#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
import os
gi.require_version("Gtk", "3.0")
gi.require_version("Gst", "1.0")
from gi.repository import Gtk, Gst

class Player:
	"""
	Audio player element.

	A GUI and streaming element.
	"""

	def __init__(self):
		# Creating normal vars
		self.playing = False

		# Creating the GUI
		interface = Gtk.Builder()
		interface.add_from_file(os.path.realpath("glade_windows/player.glade"))

		interface.connect_signals(self)

		self.main_widget = interface.get_object("player")
		self.play_button = interface.get_object("play_button")
		self.adjustment_volume = interface.get_object("adjustment_volume")
		self.adjustment_position = interface.get_object("adjustment_position")
		self.scale_position = interface.get_object("scale_position")
		self.time_label = interface.get_object("time_label")

		# Creating the GStreamer pipeline and filling it.
		Gst.init_check()
		self._pipeline = Gst.Pipeline.new("pipeline")

		self._file_source = Gst.ElementFactory.make("filesrc", "file-source")
		self._pipeline.add(self._file_source)

		self._decoder = Gst.ElementFactory.make("decodebin", "decoder")
		self._pipeline.add(self._decoder)

		self._queue = Gst.ElementFactory.make("queue", "queue")
		self._pipeline.add(self._queue)

		self._converter = Gst.ElementFactory.make("audioconvert", "converter")
		self._pipeline.add(self._converter)

		self._volume = Gst.ElementFactory.make("volume", "volume")
		self._pipeline.add(self._volume)

		self._output = Gst.ElementFactory.make("autoaudiosink", "output")
		self._pipeline.add(self._output)

		self._file_source.link(self._decoder)
		self._decoder.connect("pad-added", self.on_decoder_add_pad)
		self._queue.link(self._converter)
		self._converter.link(self._volume)
		self._volume.link(self._output)

		bus = self._pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_pipeline_message)

	def set_filepath(self, *filepath):
		"""Sets the filepath of the file to be read"""
		filepath = os.path.join(*filepath)

		self.reset()

		assert os.path.exists(filepath)

		filepath = os.path.realpath(filepath)
		self._file_source.set_property("location", filepath)
		self.load()

	def set_volume(self, volume):
		"""Sets the volume of the stream"""
		self._volume.set_property("volume", float(volume))
		self.adjustment_volume.set_value(volume)

	def play(self):
		"""Starts the reading of the file"""
		if not self.playing:
			self._pipeline.set_state(Gst.State.PLAYING)
			self._switch_play_button("pause")
			self.playing = True

	def pause(self):
		"""Pauses the stream"""
		if self.playing:
			self._pipeline.set_state(Gst.State.PAUSED)
			self._switch_play_button("play")
			self.playing = False

	def stop(self):
		"""
		Stops the reading of the file

		Once it's called, the stream will go to READY state
		"""
		self._pipeline.set_state(Gst.State.READY)
		self._switch_play_button("play")
		self.playing = False

	def reset(self):
		"""Reset the player values to None or equivalent"""
		self._pipeline.set_state(Gst.State.NULL)
		self.playing = False
		self.duration = Gst.CLOCK_TIME_NONE
		self.set_volume(0)
		self._file_source.set_property("location", None)
		self.adjustment_position.set_value(0)
		self.time_label.set_text("00:00 / 00:00")
		self._switch_play_button("play")

	def load(self):
		"""Load some current song metadata"""
		self._pipeline.set_state(Gst.State.READY)
		self.playing = False
		self._switch_play_button("play")
		_, self.duration = self._pipeline.query_duration(Gst.Format.TIME)

	def on_play_button_clicked(self, button):
		"""When the play/pause button is clicked"""
		if self.playing:
			self.pause()
		else:
			self.play()

	def on_adjustment_volume_changed(self, adjustment):
		"""When the user changes the volume via the GUI"""
		self._volume.set_property("volume", float(adjustment.get_value()))

	def on_decoder_add_pad(self, bin, pad):
		"""When the stream's decoder has an available pad"""
		sink = self._queue.get_static_pad("sink")
		pad.link(sink)

	def on_pipeline_message(self, bus, message):
		"""When the pipeline emits messages via its bus"""
		msg_type = message.type
		if msg_type == Gst.MessageType.EOS:
			self.stop()

	def _switch_play_button(self, state="default"):
		"""
		Changes the state of the GUI's play button.

		If you want to do it externally, please call the `play`, `pause` or
		`stop` method instead.

		`state` must be one of "default", "play" and "pause".
		"default" invert the actual state of the button.
		"play" and "pause" shows the symbol for play and pause, respectively.
		"""
		label = self.play_button.get_children()[0]
		if state == "default":
			if label.get_text() == "⏸":
				label.set_text("⏵")
			else:
				label.set_text("⏸")
		elif state == "play":
			label.set_text("⏵")
		elif state == "pause":
			label.set_text("⏸")

if __name__ == "__main__":
	import sys
	from window import Window
	from lecture import Lecture
	player = Player()
	lecture = Lecture(player)
	window = Window()
	window.set_content(lecture)
	Gtk.main()
