#!/usr/bin/python3
# -*- coding:utf-8 -*-

def parse_trans(trans):
	"""
	Parses the transition array in order to show the song's transition and type

	The transition array is like ["type", "transition1", "transition2"] where
	"transition1" can be empty, BUT not missing.

	"type" is in the form ^[1&#O]$
	"transition1" and "transition2" are in the form ^!?[qslfr]?n?$

	Calls _parse_song_trans_to_str in order to parse the transcodes
	"""
	transition = ""

	if trans[0] == '1':
		transition += "<span foreground=\"blue\">One</span>"
	elif trans[0] == "&":
		transition += "<span foreground=\"green\">Restart</span>"
	elif trans[0] == "#":
		transition += "<span foreground=\"red\">Random</span>"
	elif trans[0] == "O":
		transition += "<span foreground=\"purple\">Repeat</span>"
	else:
		transition += "Erreur"

	if len(trans[1]) > 0:
		transition += " (" + _parse_song_trans_to_str(trans[1]) + ")"

	transition += ", " + _parse_song_trans_to_str(trans[2])

	return transition

def _parse_song_trans_to_str(transcode):
	"""
	Parses a transcode.

	A transcode is in the form ^!?[qslfr]?n?$
	"""
	transition = ""

	if ~ transcode.find("q"):
		transition += "<span foreground=\"#6400FF\">Quickfadeout</span>"
	elif ~ transcode.find("s"):
		transition += "<span foreground=\"teal\">Fadeout</span>"
	elif ~ transcode.find("l"):
		transition += "<span foreground=\"blue\">Longfadeout</span>"
	elif ~ transcode.find("f"):
		transition += "<span foreground=\"red\">Full</span>"
	elif ~ transcode.find("r"):
		transition += "<span foreground=\"maroon\">Raw</span>"
	elif not ~ transcode.find("n"):
		transition += "Erreur"
	
	if ~ transcode.find("n"):
		transition += " <span foreground=\"fuchsia\">Autonext</span>"

	return transition

def escape_pango_chars(string):
	"""Escapes chars used in Pango markup like `&><`"""
	chars = {"&": "&amp;", ">": "&lt;", "<": "&gt;"}

	for char, escaped_char in chars.items():
		splited = string.split(str(char))
		string = escaped_char.join(splited)

	return string
