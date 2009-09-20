"""
    Plugin for streaming Apple Movie Trailers
"""

# main imports
import sys
import os
import xbmc

# plugin constants
__plugin__ = "Apple Movie Trailers Lite"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Apple%20Movie%20Trailers%20Lite"
__useragent__ = "QuickTime/7.2 (qtver=7.2;os=Windows NT 5.1Service Pack 3)"
__credits__ = "Team XBMC"
__version__ = "1.7.4"
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "22965"


def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[PLUGIN] '%s: Version - %s-r%s' initialized!" % ( __plugin__, __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ] )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
    # spam revision info
    xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), xbmc.LOGNOTICE )
    # if not compatible, inform user
    if ( not ok ):
        import xbmcgui
        xbmcgui.Dialog().ok( "%s - %s: %s" % ( __plugin__, xbmc.getLocalizedString( 30700 ), __version__, ), xbmc.getLocalizedString( 30701 ) % ( __plugin__, ), xbmc.getLocalizedString( 30702 ) % ( __XBMC_Revision__, ), xbmc.getLocalizedString( 30703 ) )
    #return result
    return ok


if ( __name__ == "__main__" ):
    if ( not sys.argv[ 2 ] ):
        # only run if compatible
        if ( _check_compatible() ):
            import resources.lib.xbmcplugin_trailers as plugin
            plugin.Main()
    elif ( sys.argv[ 2 ].startswith( "?Fetch_Showtimes" ) ):
        import resources.lib.xbmcplugin_showtimes as showtimes
        s = showtimes.GUI( "plugin-AMTII-showtimes.xml", os.getcwd(), "default" )
        del s
    elif ( sys.argv[ 2 ].startswith( "?Download_Trailer" ) ):
        import resources.lib.xbmcplugin_download as download
        download.Main()
    elif ( sys.argv[ 2 ].startswith( "?OpenSettings" ) ):
        import xbmcplugin
        xbmcplugin.openSettings( sys.argv[ 0 ] )
        # sleep for a few milliseconds, to give dialog time to close.  had issues early, may not be necessary
        #TODO: verify this is necessary
        xbmc.sleep( 50 )
        # refresh listing in case settings changed
        xbmc.executebuiltin( "Container.Refresh" )

