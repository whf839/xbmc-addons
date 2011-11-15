"""
    Weather plugin
"""

#main imports
import sys
import urllib, os.path, xbmc, re, htmlentitydefs, time

REMOTE_DBG = False 

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)

# Script constants
__plugin__ = "Weather Plus"
__pluginname__ = "Weather Plus"
__author__ = "brightsr (original sources by nuka1195)"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/addons/weather.weatherplus"
__version__ = "2.4.0"
__svn_revision__ = "$Revision$"
#__XBMC_Revision__ = "21010"
__XBMC_Build__ = "10"

def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[PLUGIN] '%s: Version - %s-r%s' initialized!" % ( __plugin__, __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_build = xbmc.getInfoLabel( "System.BuildVersion" ).split( " " )[ 0 ]
        # compatible?
        ok = xbmc_build >= int( __XBMC_Build__ )
    except:
        # error, is it PRE-11.0?
	ok = (1, 0)[ xbmc_build.startwith("PRE-11") ] * 2
	
    # spam revision info
    # xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "     ** Found XBMC Build Version: %s [%s] **" % ( xbmc.getInfoLabel( "System.BuildVersion" ), ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), xbmc.LOGNOTICE )
    #return result
    return ok

# Start the main plugin
if ( __name__ == "__main__" ):
    if ( _check_compatible() ):
        from xbmcplugin_weather import Main
        Main()
    else:
        raise

