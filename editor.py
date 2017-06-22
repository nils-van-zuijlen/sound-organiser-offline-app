#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from parse_to_pango import parse_trans
from song_list_item import SongListItem

class Editor:
    """Project editing interface."""
    def __init__(self):
        # Creating some vars
        self.songs = []
        self.project = {}
        self.parent = None

        # Loading the GUI from file
        interface = Gtk.Builder()
        interface.add_from_file(os.path.realpath("glade_windows/editor.glade"))

        interface.connect_signals(self)

        # Setting the GUI vars
        self.main_widget = interface.get_object("editor")
        self.projecttitle_buffer = interface.get_object(
            "projecttitle_entrybuffer")
        self.songdescription_buffer = interface.get_object(
            "songdescription_entrybuffer")
        self.songtitle_buffer = interface.get_object(
            "songtitle_entrybuffer")
        self.songtransition_label = interface.get_object("transition_label")
        self.songvolume_adjustment = interface.get_object(
            "songvolume_adjustment")
        self.songfilechooser = interface.get_object("songfile_filechooserbutton")

        self.song_list = Gtk.Box.new(Gtk.Orientation.VERTICAL, 3)
        interface.get_object("song_scroll").add(self.song_list)
        self.song_list.show()

    def on_projtitle_changed(self, widget):
        """Called when the user edits the project's title"""
        self.project["name"] = widget.get_text()

    def on_transition_edit(self, widget):
        """When the edit transition button is activated."""
        interface = Gtk.Builder()
        interface.add_from_file(
            os.path.realpath("glade_windows/transition_dialog.glade"))
        interface.connect_signals(self)

        dialog = interface.get_object("transition_dialog")
        ttype = interface.get_object("type_comboboxtext")
        trans1 = interface.get_object("transition1_comboboxtext")
        trans2 = interface.get_object("transition2_comboboxtext")
        autonext1 = interface.get_object("autonext1_switch")
        autonext2 = interface.get_object("autonext2_switch")
        dialog.set_transient_for(self.parent.main_widget)

        # setting the dialog with the current transition
        cur_trans = self.current_song.song_dict["trans"]
        ttype.set_active_id(cur_trans[0])
        if len(cur_trans[1]) == 2 or (len(cur_trans[1]) == 1 and
          cur_trans[1] != "n"):
            trans1.set_active_id(cur_trans[1][0])
        trans2.set_active_id(cur_trans[2][0])
        autonext1.set_active(bool(~cur_trans[1].find("n")))
        autonext2.set_active(bool(~cur_trans[2].find("n")))

        ans = dialog.run()
        try:
            if ans == Gtk.ResponseType.OK:
                new_trans = []
                # testing if the type is valid or fallback to One
                if ttype.get_active_id():
                    new_trans.append(ttype.get_active_id())
                else:
                    new_trans.append("1")
                # testing if there are any trans1
                if trans1.get_active_id():
                    new_trans.append(trans1.get_active_id())
                else:
                    new_trans.append("")
                # testing if the trans2 is valid or fallback to Raw
                if trans2.get_active_id():
                    new_trans.append(trans2.get_active_id())
                else:
                    new_trans.append("r")
                # adding the autonexts if necessary
                if autonext1.get_active():
                    new_trans[1] += "n"
                if autonext2.get_active():
                    new_trans[2] += "n"
                # setting the new transition
                self.set_trans(new_trans)
        finally:
            dialog.destroy()

    def on_trans_ok_clicked(self, widget):
        """Send an OK response to the widget"""
        widget.response(Gtk.ResponseType.OK)

    def on_trans_cancel_clicked(self, widget):
        """Send a CANCEL response to the widget"""
        widget.response(Gtk.ResponseType.CANCEL)

    def on_filepath_changed(self, widget):
        """Called when the user changes the filepath in the selector."""
        self.set_file(widget.get_filename())

    def on_songtitle_changed(self, widget):
        """Called when the user edits the current song's title"""
        self.current_song.set_title(widget.get_text())

    def on_songdescr_changed(self, widget):
        """Called when the user edits the current song's description"""
        self.current_song.set_descr(widget.get_text())

    def on_songvol_changed(self, widget):
        """Called when the user edits the current song's volume"""
        self.current_song.song_dict["vol"] = widget.get_value()

    def add_song_to_list(self, song):
        """
        Adds a song to the song_list

        `song` is a SongListItem
        """
        self.song_list.pack_start(song.main_widget, False, False, 0)
        self.songs.append(song)

    def set_trans(self, transition):
        """Set the current song's transition."""
        self.current_song.set_trans(transition)
        self._set_trans(transition)

    def _set_trans(self, transition):
        """
        Set the transition in the label.

        Does not change the current song's transition.
        Please use `set_trans` for that.
        """
        self.songtransition_label.set_markup(parse_trans(transition))

    def set_file(self, filepath):
        """
        Set the current song's filepath

        Does not change the filepath in the filechooser.
        Please use `_set_file` for that.
        """
        self.current_song.song_dict["file"] = filepath

    def _set_file(self, filepath):
        """
        Set the filepath in the filechooser.

        Does not change the current song's filename.
        Please use `set_file` for that.
        """
        filepath = os.path.join(self.project["path"], filepath)
        if os.path.exists(filepath):
            self.songfilechooser.set_filename(filepath)
        else:
            self.songfilechooser.unselect_all()

    def _set_proj_title(self, projtitle):
        """
        Set the projtitle in its entrybuffer.

        Doesn't edit the project's dictionnary.
        """
        self.projecttitle_buffer.set_text(projtitle, -1)

    def select_song(self, song):
        """Select the given song for editing."""
        self.current_song = song
        song_dict = song.song_dict
        self._set_trans(song_dict["trans"])
        self.songtitle_buffer.set_text(song_dict["name"], -1)
        self.songdescription_buffer.set_text(song_dict["descr"], -1)
        self._set_file(song_dict["file"])
        self.songvolume_adjustment.set_value(song_dict["vol"])

    def open_project(self, project):
        """
        Open the given project.

        `project` is a dictionnary
        """
        self.project = project
        self._set_proj_title(project["name"])
        for song in project["songs"]:
            self.add_song_to_list(SongListItem(song, self))
        if len(project["songs"]) > 0:
            self.select_song(self.songs[0])

if __name__ == "__main__":
    from window import Window
    editor = Editor()
    window = Window()
    window.set_content(editor)
    editor.project = {"path": "/", "name": "Project's title"}
    song = SongListItem({"name": "Titre du son", "file": "home/user/test.mp3",
        "vol": 0.7, "trans": ["&", "", "ln"], "descr": "Une petite description"
        }, editor)
    editor.add_song_to_list(song)
    editor.select_song(song)
    window.show()
    Gtk.main()
