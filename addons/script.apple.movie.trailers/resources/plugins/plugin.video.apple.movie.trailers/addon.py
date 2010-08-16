"""
    Plugin for streaming content from Apple.com
"""

# main imports
import sys
import os
import xbmc

# plugin constants
__plugin__ = "Apple Movie Trailers"
__script__ = "Apple Movie Trailers"
__author__ = "Nuka1195"
__url__ = "http://code.google.com/p/xbmc-scripting/"
__svn_url__ = "http://xbmc-scripting.googlecode.com/svn/trunk/Apple%20Movie%20Trailers"
__credits__ = "XBMC TEAM, freenode/#xbmc-scripting"
__version__ = "1.5.0"


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        from resources.lib import categories as plugin
    elif ( "idMovie=" in sys.argv[ 2 ] ):
        from resources.lib import player as plugin
    else:
        from resources.lib import videos as plugin
    plugin.Main()
