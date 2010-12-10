## XBMC Lyrics

import sys
import xbmcaddon

# Addon class
Addon = xbmcaddon.Addon( id="script.xbmc.lyrics" )


if ( __name__ == "__main__" ):
    # player
    if ( len( sys.argv ) == 1 or sys.argv[ 1 ].isdigit() ):
        import resources.lib.player as player
        player.XBMCPlayer( xbmc.PLAYER_CORE_PAPLAYER, Addon=Addon, gui=len( sys.argv) == 1 )
    # text viewer
    elif ( sys.argv[ 1 ].startswith( "viewer=" ) ):
        import resources.lib.viewer as viewer
        viewer.Viewer( Addon=Addon, kind=sys.argv[ 1 ].split( "=" )[ 1 ] )
    # xbox check for updates
    elif ( sys.argv[ 1 ].startswith( "updates" ) ):
        import resources.lib.updates as updates
        updates.Updates( Addon=Addon )
    # utilities
    elif ( sys.argv[ 1 ].startswith( "util=" ) ):
        import resources.lib.utils as utils
        utils.Utilities( Addon=Addon, function=sys.argv[ 1 ].split( "=" )[ 1 ] )
