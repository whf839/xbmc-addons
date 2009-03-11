"""
    This script displays radars and forecasts from www.weather.com
"""

#main imports
import sys
import os
import xbmc

# Script constants
__scriptname__ = "TWC Supplemental"
__author__ = "Nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/TWC%20Supplemental"
__credits__ = "Team XBMC"
__version__ = "1.5.2"
__svn_revision__ = 0

xbmc.log( "[SCRIPT] '%s: version %s' initialized!" % ( __scriptname__, __version__, ), xbmc.LOGNOTICE )


# Start the main gui
if ( __name__ == "__main__" ):
    # check if user passed an arg to set script as window
    try:
        # passed 1, so we want a window
        window = sys.argv[ 1 ] == "1"
    except:
        # nothing passed so default to dialog
        window = False
    import resources.lib.gui as gui
    ui = gui.GUI( "script-twc-main.xml", os.getcwd(), "Default" )
    ui.doModal()
    del ui
    sys.modules.clear()
