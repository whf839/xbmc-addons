"""
    Plugin for streaming content from CNN
"""

# main imports
import sys
import xbmc

# plugin constants
__plugin__ = "CNN Video"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/CNN%20Video"
__credits__ = "Team XBMC"
__version__ = "1.2.1"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        from cnnAPI import xbmcplugin_categories as plugin
    else:
        from cnnAPI import xbmcplugin_videos as plugin
    plugin.Main()
