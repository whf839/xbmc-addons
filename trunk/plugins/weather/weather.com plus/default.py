"""
    Weather plugin for www.weather.com
"""

#main imports
import sys
import xbmc

# Script constants
__pluginname__ = "weather.com+"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/weather/Weather.com"
__version__ = "1.0"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __pluginname__, __version__, ), xbmc.LOGNOTICE )

# Start the main plugin
if ( __name__ == "__main__" ):
    from resources.lib.xbmcplugin_weather import Main
    Main()
    sys.modules.clear()
