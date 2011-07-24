"""
    Weather plugin
"""

#main imports
import sys
import urllib, os.path, xbmc, re, htmlentitydefs, time

# Script constants
__plugin__ = "Weather Plus"
__pluginname__ = "Weather Plus"
__author__ = "brightsr (original sources by nuka1195)"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/addons/weather.weatherplus"
__version__ = "2.2.8"
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "21010"

def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[PLUGIN] '%s: Version - %s-r%s' initialized!" % ( __plugin__, __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ][ : 5 ] )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
    # spam revision info
    # xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), xbmc.LOGNOTICE )
    #return result
    return ok

# Start the main plugin
if ( __name__ == "__main__" ):
    if ( _check_compatible() ):
        from xbmcplugin_weather import Main
        Main()
    else:
        raise

