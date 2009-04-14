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
__version__ = "1.5.4"
__XBMC_Revision__ = "19001"


def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[PLUGIN] '%s: version %s' initialized!" % ( __plugin__, __version__, ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
        xbmc_rev = 0
        xbmc_rev = int( xbmc_version.split( " " )[ 1 ].replace( "r", "" ) )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so make incompatible
        ok = False
    # spam revision info
    xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", )[ ok ], ), xbmc.LOGNOTICE )
    # if not compatible, inform user
    if ( not ok ):
        import xbmcgui
        xbmcgui.Dialog().ok( "%s - %s: %s" % ( __plugin__, xbmc.getLocalizedString( 30700 ), __version__, ), xbmc.getLocalizedString( 30701 ) % ( __plugin__, ), xbmc.getLocalizedString( 30702 ) % ( __XBMC_Revision__, ), xbmc.getLocalizedString( 30703 ) )
    #return result
    return ok
    

if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        # check for compatibility, only need to check this once
        ok = _check_compatible()
        # only run if ok
        if ( ok ):
            from installerAPI import xbmcplugin_list as plugin
    elif ( "download_url=" in sys.argv[ 2 ] ):
        from installerAPI import xbmcplugin_downloader as plugin
    elif ( sys.argv[ 2 ] == "?category='updates'" ):
        from installerAPI import xbmcplugin_update as plugin
    try:
        plugin.Main()
    except:
        pass
