pypitv
==========================================================================

**pypitv** is a python script to parse iptv m3u playlists and play live streams on a Raspberry Pi using [omxplayer](https://www.raspberrypi.org/documentation/raspbian/applications/omxplayer.md). **pypitv** can be run from any terminal, but send the live stream to the HDMI output. The original goal was to play iptv streams on a 'headless' Raspberry Pi with a connected HDMI monitor straight from an SSH terminal.

Additionally, **pypitv** can read a customized channel list from a file and allow the same playing functionality for those channels. See **customization** below for more details.

Dependencies
--------------------------------------------------------------------------

**pypitv** depends on the following packages to function:
* [omxplayer](https://www.raspberrypi.org/documentation/raspbian/applications/omxplayer.md)

Installation
--------------------------------------------------------------------------

If you don't already have omxplayer installed, you can use:
```
$ sudo apt-get install omxplayer
```

**pypitv.py** is a single python file, so simply place it in the directory of your choice. For quick access, simply place it in your home directory. If you would like to run it directly from the command line, without the python prefix, simply make it executable:
```
$ chmod +x ./pypitv.py
```

You can also rename the file to anything you find convenient.

Setup
--------------------------------------------------------------------------

**pypitv** has various settings, but the only one you really need to get started, is your iptv M3U URL. To get started, simply run:
```
$ ./pypitv.py
```
or if you haven't made the script executable:
```
$ python pypitv.py
```
You will then be asked to enter your iptv M3U URL, simply paste it and press return. Once complete, a settings file will be created and your M3U file downloaded and you're ready to go.

Usage
--------------------------------------------------------------------------

To use **pypitv** simply add the name of the station you would like to watch to the above command, like this:
```
$ python pypitv.py "channel name"
```
**pypitv** loads your channel file and searches for any matches of 'channel name'. If a match if found, you are asked if you wish to play the channel. Usually iptv subscriptions contain multiple streams of the same channel in various resolutions. Usually the best quality channels are listed first, so the first match will generally be the best. When a match if found you will see a confirmation in the form of:
```
Play CNN FHD US?
(S)kip, (Q)uit or (Return) to play: 
```
This allows you to simply press return to play this channel, **S** to skip it and search for the next match, or **Q** to quit.

omxplayer commands
--------------------------------------------------------------------------

Once a live TV stream has been launched, you will see the details from omxplayer:
```
Play CNN FHD US?
(S)kip, (Q)uit or (Return) to play: 
Video codec omx-h264 width 960 height 540 profile 77 fps 25.000000
Audio codec aac channels 2 samplerate 48000 bitspersample 16
Subtitle count: 0, state: off, index: 1, delay: 0
V:PortSettingsChanged: 960x540@25.00 interlace:0 deinterlace:0 anaglyph:0 par:1.00 display:5 layer:0 alpha:255 aspectMode:0
```
While in playing state, you can control **omxplayer** from the terminal window. Some example commands are:
* +: increase volume by 3.0dB
* -: decrease volume by 3.0dB
* q: quit omxplayer (and return to **pypitv**)

You can of course use all the [options available in omxplayer](https://www.raspberrypi.org/documentation/raspbian/applications/omxplayer.md) during playback.

Customization
--------------------------------------------------------------------------

To add your own, local channels to **pypitv**, simple create the following file in your working directory:
```
./.pypitv-custom-channels
```

This file shall contain your local channels and shall be formatted as name and URL pairs, seperated with a semi-colon:
```
channel name;channel_url
```

Once the file has been created and populated with channel name/url pairs, those channels will be included in channel searching and will take priority over iptv channels.
