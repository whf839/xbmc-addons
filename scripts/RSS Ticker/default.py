import sys
import os
import xbmc

# Script constants
__scriptname__ = "RSS Ticker Manager"
__author__ = "rwparris2"
__url__ = "http://code.google.com/p/xbmc-addons/"
__credits__ = "Team XBMC"
__version__ = "1.1.2"

xbmc.log( "[SCRIPT] '%s: version %s' initialized!" % ( __scriptname__, __version__, ), xbmc.LOGNOTICE )

if ( __name__ == "__main__" ):
    import resources.lib.gui as gui
    ui = gui.GUI( "rssTicker.xml", os.getcwd(), "default" )
    ui.doModal()
    del ui
    sys.modules.clear()
