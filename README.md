# SoundOrganiser's offline app

[![Build Status](https://travis-ci.org/nils-van-zuijlen/sound-organiser-offline-app.svg?branch=master)](https://travis-ci.org/nils-van-zuijlen/sound-organiser-offline-app) [![Code Health](https://landscape.io/github/nils-van-zuijlen/sound-organiser-offline-app/master/landscape.svg?style=flat)](https://landscape.io/github/nils-van-zuijlen/sound-organiser-offline-app/master) [![Dependency Status](https://gemnasium.com/badges/github.com/nils-van-zuijlen/sound-organiser-offline-app.svg)](https://gemnasium.com/github.com/nils-van-zuijlen/sound-organiser-offline-app)


Here is [SoundOrganiser](//github.com/nils-van-zuijlen/sound-organiser). It's an
audio player to use in plays.

## Requirements

- Python 3
- GObject binding for Python 3 : python-gi
  - Gtk+ 3.0
  - Gst 1.0

## Testing

To get an overview of the GUI, run `python3 son_en_liste.py`
and `python3 lecture.py`.

To see how it sounds while playing, run
`python3 player.py /foo/bar/baz/a_music_file.<extension>`.
`<extension>` could be mp3, ogg, wav, flac, or any supported by the `decodebin`
element from GStreamer.
