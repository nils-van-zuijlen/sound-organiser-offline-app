#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
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
		interface.add_from_file(os.path.realpath('glade_windows/player.glade'))

		interface.connect_signals(self)

		self.mainWidget = interface.get_object('player')
		self.playButton = interface.get_object('playButton')
		self.adjustmentVolume = interface.get_object('adjustmentVolume')
		self.adjustmentPlayer = interface.get_object('adjustmentPlayer')
		self.timeLabel = interface.get_object('timeLabel')

		# Creating the GStreamer pipeline and filling it.
		Gst.init_check()
		self._pipeline = Gst.Pipeline.new("pipeline")

		self._file_source = Gst.ElementFactory.make('filesrc', 'file-source')
		self._pipeline.add(self._file_source)

		self._decoder = Gst.ElementFactory.make('decodebin', 'decoder')
		self._pipeline.add(self._decoder)

		self._queue = Gst.ElementFactory.make('queue', 'queue')
		self._pipeline.add(self._queue)

		self._converter = Gst.ElementFactory.make('audioconvert', 'converter')
		self._pipeline.add(self._converter)

		self._volume = Gst.ElementFactory.make('volume', 'volume')
		self._pipeline.add(self._volume)

		self._output = Gst.ElementFactory.make('autoaudiosink', 'output')
		self._pipeline.add(self._output)

		self._file_source.link(self._decoder)
		self._decoder.connect("pad-added", self.on_decoder_addPad)
		self._queue.link(self._converter)
		self._converter.link(self._volume)
		self._volume.link(self._output)

		bus = self._pipeline.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_pipeline_message)

	def setFilepath(self, *filepath):
		"""Sets the filepath of the file to be read"""
		
		if len(filepath) == 1:
			filepath = filepath[0]
		else:
			filepath = os.path.join(*filepath)

		if os.path.exists(filepath):
			filepath = os.path.realpath(filepath)
			self.stop()
			self._file_source.set_property("location", filepath)
			self.stop()

	def setVolume(self, volume):
		"""Sets the volume of the stream"""

		self._volume.set_property("volume", float(volume))
		self.adjustmentVolume.set_value(volume)

	def play(self):
		"""Starts the reading of the file"""
		
		if not self.playing:
			self._pipeline.set_state(Gst.State.PLAYING)
			self._switchPlayButton("pause")
			self.playing = True

	def pause(self):
		"""Pauses the stream"""

		if self.playing:
			self._pipeline.set_state(Gst.State.PAUSED)
			self._switchPlayButton("play")
			self.playing = False

	def stop(self):
		"""Stops the reading of the file"""

		self._pipeline.set_state(Gst.State.READY)
		self._switchPlayButton("play")
		self.playing = False

	def on_playButton_clicked(self, button):
		"""When the play/pause button is clicked"""

		if self.playing:
			self.pause()
		else:
			self.play()

	def on_adjustmentVolume_changed(self, adjustment):
		"""When the user changes the volume via the GUI"""

		self._volume.set_property("volume", float(adjustment.get_value()))

	def on_decoder_addPad(self, bin, pad):
		"""When the stream's decoder has an available pad"""

		sink = self._queue.get_static_pad("sink")
		pad.link(sink)

	def on_pipeline_message(self, bus, message):
		"""When the pipeline emits messages via its bus"""

		msgType = message.type
		if msgType == Gst.MessageType.EOS:
			self.stop()

	def _switchPlayButton(self, state="default"):
		"""
		Changes the state of the GUI's play button.

		If you want to do it externally, please call the `play`, `pause` or
		`stop` method instead.
		"""

		label = self.playButton.get_children()[0]
		if state == "default":
			if label.get_text() == '⏸':
				label.set_text('⏵')
			else:
				label.set_text('⏸')
		elif state == "play":
			label.set_text('⏵')
		elif state == "pause":
			label.set_text('⏸')

if __name__ == '__main__':
	import sys
	from window import Window
	from lecture import Lecture
	player = Player()
	lecture = Lecture(player)
	window = Window()
	window.setContent(lecture)
	Gtk.main()
