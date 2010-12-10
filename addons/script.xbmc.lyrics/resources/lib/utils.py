## Utilities module

import os
import xbmc
import xbmcgui


class Utilities:
    """
        Shared functions
    """

    def __init__( self, Addon, function=None ):
        # set our Addon class
        self.Addon = Addon
        # do work
        if ( function is not None ):
            exec "self.%s()" % ( function, )

    def clear_artist_aliases( self ):
        # ask if user is sure
        if ( xbmcgui.Dialog().yesno( self.Addon.getAddonInfo( "Name" ), self.Addon.getLocalizedString( 30845 ) ) ):
            # create path to alias file
            _path = os.path.join( xbmc.translatePath( self.Addon.getAddonInfo( "Profile" ) ), "artist_aliases.txt" )
            # if file exists remove it
            if ( os.path.isfile( _path ) ):
                os.remove( _path )
            # notify user
            ok = xbmcgui.Dialog().ok( self.Addon.getAddonInfo( "Name" ), self.Addon.getLocalizedString( 30830 ) )
