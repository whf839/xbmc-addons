# main imports
import sys
import os

try:
    import xbmc
    DEBUG = False
except:
    DEBUG = True

import xbmcgui
import urllib2
from urllib import urlencode
import md5
import re
import time
from xbmcaddon import Addon

__Settings__ = Addon(id="weather.weatherplus")

def _fetch_data( base_url ):
	try:
            request = urllib2.Request( base_url )
            # add a faked header
            request.add_header( "User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)" )
            # open requested url
            usock = urllib2.urlopen( request )
            # read source
            data = usock.read()
            # close socket
            usock.close()
            return data
        except urllib2.HTTPError, e:
            # if error 503 and this is the first try, recall function after sleeping, otherwise return ""
            if ( e.code == 503 and retry ):
                # TODO: this is so rare, but try and determine if 3 seconds is enogh
                print "Trying url %s one more time." % base_url
                time.sleep( 3 )
                # try one more time
                return self._fetch_data( base_url, refreshtime, filename, animated, subfolder, False )
            else:
                # we've already retried, return ""
                print "Second error 503 for %s, increase sleep time." % base_url
                return ""
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            # some unknown error, return ""
            return ""

class Main:
	def __init__(self, loc=1):
		location = ""
		location_name = []
		kb = xbmc.Keyboard("","Type a name of your location", False)
		kb.doModal()
		if (kb.isConfirmed()):
			userInput = kb.getText()
			if (userInput is not None):
				location = self._fetch_location(userInput)	
		dialog = xbmcgui.Dialog()
		for count, loca in enumerate(location):
			location_name += [ location[count][0]+ ", "+ location[count][1] ]
		select = dialog.select("Choose your location", location_name)
		print select
		if ( select != -1 ):
			self.location = location[ select ]
			print __Settings__.getSetting("alt_location1")
			__Settings__.setSetting( ("alt_location1", "alt_location2", "alt_location3", )[ loc-1 ], location_name[ select ] )
			__Settings__.setSetting( ("alt_code1", "alt_code2", "alt_code3", )[ loc-1 ], self.location[2] )
		__Settings__.openSettings()
		# url = "http://www.accuweather.com/quick-look.aspx?loc=" + self.location[2]
		# print url
		# htmlSource = _fetch_data ( url )
		# print htmlSource
	
	def _fetch_location(self, userInput):
		pattern_location = "<location city=\"([^\"]+)\" state=\"([^\"]+)\" location=\"([^\"]+)\"/>"
		htmlSource = _fetch_data ( "http://www.accuweather.com/includes/ajax-functions/cityLookup.asp?location="+ userInput )
		location = re.findall( pattern_location, htmlSource )
		return location

Main( loc=int( sys.argv[ 1 ].split( "=" )[ 1 ] ) )
