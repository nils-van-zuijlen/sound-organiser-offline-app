#!/usr/bin/python3
# -*- coding:UTF-8 -*-

def parse_trans(trans):
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

	for char, escaped_char in enumerate(chars):
		splited = string.split(char)
		string = escaped_char.join(splited)

	return string
