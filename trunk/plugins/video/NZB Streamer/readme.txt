NZB Streamer XBMC plugin
v0.1

Instructions
================
0) Be using Windows (the par2 binary is currently just for Windows, but other platforms will be added later)
1) Extract to XBMC\plugins\Video
2) Open the plugin, and right click/info button on one of the items, choose "Plugin Settings"
3) Enter your Usenet server hostname, port, username, and password.
4) If you want imdb info+posters enable them
5) If you want any extra RSS feeds, open settings.py and add any extra RSS feeds to the dictionary (note these will be replaced when upgrading versions, so make a copy)
6) Browse an RSS or run a search and select a result. It will start downloading and as soon as the first RAR is finished, it should start playing.
7) If a missing or corrupt article is found, the stream should stop and ask you whether you want to continue the download (and hope it can be repaired with PAR files), or to cancel the download.
8) You can stop a streaming video and start it again (but currently you have to rebrowse/search for it).


Full Disclosure
==================
This script takes your Usenet username and password to connect to your server,
so you have to trust that I haven't made this to steal your login. :)
Please check the source code if you are worried about it by searching for:
xbmcplugin.getSetting("password")


Rationale
============
Why did I replace the SABnzbd+ backend?
- web API doesn't have detailed callback support to report when the download breaks or when the first RAR finishes
- it doesn't create the 0-byte RARs that XBMC requires to play video from a RAR set
- SABnzbd+ has to be installed, configured, and run separately from XBMC, which is flexible for power users but inconvenient for dummies ;)


Future Work
=============
- improve frontend:
    * make custom icons
    * add filters
    * clean up result names (replace dots with spaces)
    * support searching with Binsearch
    * maintain a queue of currently running streams (background downloading)
    * keep a list of most-recently-used NZBs and cache them

- improve backend:
    * add cross-platform par2 binaries
    * add cross-platform library to decode yEnc with less CPU usage


Credits
================
frontend created by switch
backend created by Matt Chambers

based on the script "XBMC-Addons Installer Plugin" by Nuka1195
small block of code from SABnzbd

feedparser - RSS feed parser written in python - feedparser.org
simplejson - simple json->dictionary decoder - http://code.google.com/p/simplejson/
pynzb - NZB parser - http://pypi.python.org/pypi/pynzb
SABnzbd-XBMC - a plugin to control SABnzbd+ from XBMC - http://forums.sabnzbd.org/index.php?topic=494.msg16453#msg16453
