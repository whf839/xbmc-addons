## Updates module for xbmc4xbox

import xbmcgui


class Updates:
    """
        Updates class:
        Only used for xbmc4xbox to check for updates.
    """

    def __init__( self, Addon ):
        # set our Addon class
        self.Addon = Addon
        # check for updates
        self._check_for_updates()

    def _check_for_updates( self ):
        try:
            # create dialog
            pDialog = xbmcgui.DialogProgress()
            # give feedback
            pDialog.create( self.Addon.getAddonInfo( "Name" ), self.Addon.getLocalizedString( 30760 ) )
            pDialog.update( 0 )
            # url to addon.xml file
            url = "%ssvn/addons/%s/addon.xml" % ( self.Addon.getSetting( "repo" ), self.Addon.getAddonInfo( "Id" ), )
            # import here for faster dialog
            import urllib
            import re
            # get addon.xml source
            xml = urllib.urlopen( url ).read()
            # parse version
            version = re.search( "<addon id=\"[^\"]+\".+?name=\"[^\"]+\".+?version=\"([^\"]+)\".+?provider-name=\"[^\"]+\".*?>", xml, re.DOTALL ).group( 1 )
            # set proper message
            msg1 = self.Addon.getLocalizedString( 30700 ) % ( self.Addon.getAddonInfo( "Version" ), )
            msg2 = [ self.Addon.getLocalizedString( 30701 ), self.Addon.getLocalizedString( 30702 ) % ( version, ) ][ version > self.Addon.getAddonInfo( "Version" ) ]
        except Exception, e:
            # set proper error messages
            msg1 = self.Addon.getLocalizedString( 30770 )
            msg2 = str( e )
        # done, close dialog
        pDialog.close()
        # notify user of result
        ok = xbmcgui.Dialog().ok( self.Addon.getAddonInfo( "Name" ), msg1, "", msg2 )
