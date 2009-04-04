"""
    Plugin for downloading scripts/plugins/skins from SVN repositories
"""

# main imports
import sys
import xbmc

# plugin constants
__plugin__ = "SVN Repo Installer"
__author__ = "nuka1195/BigBellyBilly"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/programs/SVN%20Repo%20Installer"
__credits__ = "Team XBMC"
__version__ = "1.5.2"

xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )


if ( __name__ == "__main__" ):
    if ( "download_url=" in sys.argv[ 2 ] ):
        from installerAPI import xbmcplugin_downloader as plugin
    elif ( sys.argv[ 2 ] == "?category='updates'" ):
        from installerAPI import xbmcplugin_update as plugin
    else:
        from installerAPI import xbmcplugin_list as plugin
    plugin.Main()
