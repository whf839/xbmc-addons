import xbmc, xbmcgui
import sys, os, re
import urllib, urllib2

__plugin__ = 'VideoMonkey'
__author__ = 'sfaxman'
__svn_url__ = 'http://xbmc-addons.googlecode.com/svn/addons/plugin.video.VideoMonkey/'
__credits__ = 'bootsy'
__version__ = '1.4.1'

rootDir = os.getcwd()
if rootDir[-1] == ';':rootDir = rootDir[0:-1]

class Main:
    def __init__(self):
        self.pDialog = None
        self.curr_file = ''
        self.run()

    def run(self):
            import videomonkey
            videomonkey.Main()
            #sys.modules.clear()

win = Main()
