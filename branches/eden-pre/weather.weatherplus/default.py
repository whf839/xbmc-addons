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
__version__ = "2.5.1"
#__svn_revision__ = "$Revision$"
#__XBMC_Revision__ = "21010"
#__XBMC_Build__ = "10"

'''
def _check_compatible():
    # get xbmc build version
    xbmc_build = xbmc.getInfoLabel( "System.BuildVersion" )
    try:
        # spam plugin statistics to log
        xbmc.log( "[PLUGIN] '%s: Version - %s-r%s' initialized!" % ( __plugin__, __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )     
        # compatible?
        ok = int( xbmc_build.split( " " )[ 0 ] ) >= int( __XBMC_Build__ )
    except:
        # error, is it PRE-11.0? before 20111116 = old pre-eden, after = new pre-eden
	ok = (0, 1)[ xbmc_build.startswith("PRE-11") ] * ( ( int( " ".join( re.findall("Git[:]([0-9]+)", xbmc_build) ) ) >= 20111116 ) + 1 )
	
    # spam revision info
    # xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "     ** Found XBMC Build Version: %s [%s] **" % ( xbmc.getInfoLabel( "System.BuildVersion" ), ( "Not Compatible", "Compatible(Dharma or old pre-eden)", "Compatible(new pre-Eden)", )[ ok ], ), xbmc.LOGNOTICE )
    #return result
    return ok
'''

# Start the main plugin

xbmc.log( "[PLUGIN] '%s: Version - %s' initialized!" % ( __plugin__, __version__ ), xbmc.LOGNOTICE )     

if ( __name__ == "__main__" ):
    #__ver__ = _check_compatible()
    if ( 1 ):
        from xbmcplugin_weather import Main
	argv = len(sys.argv[1])
        Main( argv == 1 ) # argv > 1 : guisettings has areacode ( so sys.argv[1] has areacode )
    else:
        raise

