## Category module: fetches a list of categories to use as folders

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class Main:
    # base urls
    BASE_URL = "http://www.cnn.com/.element/ssi/www/auto/2.0/video/xml/%s.xml"
    # base paths
    BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( os.getcwd(), "resources", "thumbnails" )
    # plugin handle
    _handle = int( sys.argv[ 1 ] )
    # Addon class
    Addon = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )

    def __init__( self ):
        self._parse_argv()
        self.get_categories()

    def _parse_argv( self ):
        if ( not sys.argv[ 2 ] ):
            self._log_addon_action( "started" )
            self.args = _Info( title="", category=None )
        else:
            # call _Info() with our formatted argv to create the self.args object
            exec "self.args = _Info(%s)" % ( urllib.unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ), )

    def _log_addon_action( self, action ):
        # log addon info
        xbmc.log( "=" * 80, xbmc.LOGNOTICE )
        xbmc.log( "[ADD-ON] - %s %s!" % ( self.Addon.getAddonInfo( "Name" ), action, ), xbmc.LOGNOTICE )
        xbmc.log( "           Id: %s - Type: %s - Version: %s" % ( self.Addon.getAddonInfo( "Id" ), self.Addon.getAddonInfo( "Type" ), self.Addon.getAddonInfo( "Version" ) ), xbmc.LOGNOTICE )
        xbmc.log( "=" * 80, xbmc.LOGNOTICE )

    def get_categories( self ):
        try:
            if ( not sys.argv[ 2 ] ):
                categories = (
                                        ( self.Addon.getLocalizedString( 30900 ), "categories", ),
                                        ( self.Addon.getLocalizedString( 30901 ), "ireports", ),
                                        #( self.Addon.getLocalizedString( 30902 ), "ontv", ),
                                        ( self.Addon.getLocalizedString( 30903 ), "espanol", ),
                                        #( self.Addon.getLocalizedString( 30904 ), "live", ),
                                    )
            elif ( self.args.category == "categories" ):
                categories = (
                                        ( self.Addon.getLocalizedString( 30950 ), "most_popular", ),
                                        ( self.Addon.getLocalizedString( 30951 ), "by_section_us", ),
                                        ( self.Addon.getLocalizedString( 30952 ), "by_section_world", ),
                                        ( self.Addon.getLocalizedString( 30953 ), "by_section_politics", ),
                                        ( self.Addon.getLocalizedString( 30954 ), "by_section_showbiz", ),
                                        ( self.Addon.getLocalizedString( 30955 ), "by_section_crime", ),
                                        ( self.Addon.getLocalizedString( 30956 ), "by_section_funny_news", ),
                                        ( self.Addon.getLocalizedString( 30957 ), "by_section_tech", ),
                                        ( self.Addon.getLocalizedString( 30958 ), "by_section_living", ),
                                        ( self.Addon.getLocalizedString( 30959 ), "by_section_health", ),
                                        ( self.Addon.getLocalizedString( 30960 ), "by_section_student", ),
                                        ( self.Addon.getLocalizedString( 30961 ), "by_section_business", ),
                                        ( self.Addon.getLocalizedString( 30962 ), "by_section_sports", ),
                                        ( self.Addon.getLocalizedString( 30963 ), "by_section_weather", ),
                                        ( self.Addon.getLocalizedString( 30964 ), "top_stories", ),
                                    )
            elif ( self.args.category == "ireports" ):
                categories = (
                                        ( self.Addon.getLocalizedString( 30965 ), "ireport_newsiest_now", ),
                                        ( self.Addon.getLocalizedString( 30966 ), "ireport_on_cnn", ),
                                        ( self.Addon.getLocalizedString( 30967 ), "ireport_sound_off", ),
                                        ( self.Addon.getLocalizedString( 30968 ), "ireport_off_beat", ),
                                        ( self.Addon.getLocalizedString( 30969 ), "cnni_programs_ireport", ),
                                    )
            elif ( self.args.category == "ontv" ):
                categories = (
                                        ( self.Addon.getLocalizedString( 30980 ), "cnn_programs_american_morning", ),
                                    )
            elif ( self.args.category == "espanol" ):
                categories = (
                                        ( self.Addon.getLocalizedString( 30970 ), "spanish_eleccions", ),
                                        ( self.Addon.getLocalizedString( 30971 ), "spanish_economia", ),
                                        ( self.Addon.getLocalizedString( 30972 ), "spanish_tu_dinero", ),
                                        ( self.Addon.getLocalizedString( 30973 ), "spanish_vida", ),
                                        ( self.Addon.getLocalizedString( 30974 ), "spanish_entretenimiento", ),
                                        ( self.Addon.getLocalizedString( 30975 ), "spanish_tecnologia", ),
                                        ( self.Addon.getLocalizedString( 30976 ), "spanish_estados_unidos", ),
                                        ( self.Addon.getLocalizedString( 30977 ), "spanish_america_latina", ),
                                        ( self.Addon.getLocalizedString( 30978 ), "spanish_spanish_mundo", ),
                                    )
            # fill media list
            ok = self._fill_media_list( categories )
        except Exception, e:
            # oops, notify user what error occurred
            LOG( str( e ), xbmc.LOGERROR )
            # set failed
            ok = False
        if ( ok ):
            xbmcplugin.addSortMethod( handle=self._handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            # set our plugin category
            xbmcplugin.setPluginCategory( handle=self._handle, category=self.args.title )
            # set fanart
            self._set_fanart()
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=self._handle, succeeded=ok )

    def _set_fanart( self ):
        # user fanart preference
        fanart = [ self.Addon.getSetting( "fanart_image" ), [ None, self.Addon.getSetting( "fanart_path" ) ][ self.Addon.getSetting( "fanart_path" ) != "" and self.Addon.getSetting( "fanart_type" ) == "0" ], [ self.Addon.getAddonInfo( "id" ), self.args.category ][ self.args.category is not None ] ]
        # if user passed fanart tuple (image, category path,)
        if ( fanart is not None ):
            # if skin has fanart image use it
            fanart_image = self.Addon.getAddonInfo( "Id" ) + "-fanart.png"
            # if no skin image check for a category image
            if ( not xbmc.skinHasImage( fanart_image ) ):
                if ( fanart[ 1 ] is not None ):
                    # set category image
                    fanart_image = fanart[ 1 ] + "%s.png" % fanart[ 2 ].split( ": " )[ 0 ]
                else:
                    # set user preference image
                    fanart_image = fanart[ 0 ]
            # set fanart
            xbmcplugin.setPluginFanart( handle=self._handle, image=fanart_image )

    def _fill_media_list( self, categories ):
        try:
            ok = True
            # enumerate through the list of categories and add the item to the media list
            for title, category in categories:
                if ( not sys.argv[ 2 ] ):
                    url = "%s?title=%s&category=%s" % ( sys.argv[ 0 ], urllib.quote_plus( repr( title ) ), urllib.quote_plus( repr( category ) ), )
                else:
                    url = "%s?title=%s&url=%s" % ( sys.argv[ 0 ], urllib.quote_plus( repr( "%s - %s" % ( self.args.title, title, ) ) ), urllib.quote_plus( repr( self.BASE_URL % ( category, ) ) ), )
                # check for a valid custom thumbnail for the current category
                thumbnail = self._get_thumbnail( category )
                # set the default icon
                icon = "DefaultFolder.png"
                # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem=xbmcgui.ListItem( title, iconImage=icon, thumbnailImage=thumbnail )
                # add the different infolabels we want to sort by
                listitem.setInfo( type="Video", infoLabels={ "Title": title } )
                # add the item to the media list
                ok = xbmcplugin.addDirectoryItem( handle=self._handle, url=url, listitem=listitem, isFolder=True, totalItems=len( categories ) )
                # if user cancels, call raise to exit loop
                if ( not ok ): raise
        except Exception, e:
            # oops, notify user what error occurred
            LOG( str( e ), xbmc.LOGERROR )
            # set failed
            ok = False
        # return result
        return ok

    def _get_thumbnail( self, title ):
        # create the full thumbnail path for skins directory
        thumbnail = os.path.join( os.path.basename( os.getcwd() ), title + ".png" )
        # use a plugin custom thumbnail if a custom skin thumbnail does not exists
        if ( not xbmc.skinHasImage( thumbnail ) ):
            # create the full thumbnail path for plugin directory
            thumbnail = os.path.join( self.BASE_PLUGIN_THUMBNAIL_PATH, title + ".png" )
            # use a default thumbnail if a custom thumbnail does not exists
            if ( not os.path.isfile( thumbnail ) ):
                thumbnail = ""
        # return thumbnail path
        return thumbnail
