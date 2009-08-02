"""
    Plugin for viewing content from Youtube.com
"""

# main imports
import sys
import xbmc

# plugin constants
__plugin__ = "YouTube"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/YouTube"
__version__ = "1.6.8a"
__XBMC_Revision__ = "19457"


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
        ok = True
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
            from YoutubeAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_videos'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_users'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_categories as plugin
    elif ( "category='presets_categories'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_categories as plugin
    elif ( "category='delete_preset'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_categories as plugin
    elif ( "category='play_video_by_id'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_player_by_id as plugin
    elif ( "category='play_video'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_player as plugin
    elif ( "category='download_video'" in sys.argv[ 2 ] ):
        from YoutubeAPI import xbmcplugin_download as plugin
    else:
        from YoutubeAPI import xbmcplugin_videos as plugin
    try:
        plugin.Main()
    except:
        pass
