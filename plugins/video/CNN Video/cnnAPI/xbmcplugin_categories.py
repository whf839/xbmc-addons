"""
    Category module: fetches a list of categories to use as folders
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

import urllib


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class Main:
    # base urls
    BASE_URL = "http://www.cnn.com/.element/ssi/www/auto/2.0/video/xml/%s.xml"

    # base paths
    BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( os.getcwd(), "thumbnails" )

    def __init__( self ):
        self._parse_argv()
        self.get_categories()

    def _parse_argv( self ):
        if ( not sys.argv[ 2 ] ):
            self.args = _Info( title="" )
        else:
            # call _Info() with our formatted argv to create the self.args object
            exec "self.args = _Info(%s)" % ( urllib.unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ), )

    def get_categories( self ):
        try:
            if ( not sys.argv[ 2 ] ):
                categories = (
                                        ( xbmc.getLocalizedString( 30900 ), "categories", ),
                                        ( xbmc.getLocalizedString( 30901 ), "ireports", ),
                                        #( xbmc.getLocalizedString( 30902 ), "ontv", ),
                                        ( xbmc.getLocalizedString( 30903 ), "espanol", ),
                                        #( xbmc.getLocalizedString( 30904 ), "live", ),
                                    )
            elif ( self.args.category == "categories" ):
                categories = (
                                        ( xbmc.getLocalizedString( 30950 ), "most_popular", ),
                                        ( xbmc.getLocalizedString( 30951 ), "by_section_us", ),
                                        ( xbmc.getLocalizedString( 30952 ), "by_section_world", ),
                                        ( xbmc.getLocalizedString( 30953 ), "by_section_politics", ),
                                        ( xbmc.getLocalizedString( 30954 ), "by_section_showbiz", ),
                                        ( xbmc.getLocalizedString( 30955 ), "by_section_crime", ),
                                        ( xbmc.getLocalizedString( 30956 ), "by_section_funny_news", ),
                                        ( xbmc.getLocalizedString( 30957 ), "by_section_tech", ),
                                        ( xbmc.getLocalizedString( 30958 ), "by_section_living", ),
                                        ( xbmc.getLocalizedString( 30959 ), "by_section_health", ),
                                        ( xbmc.getLocalizedString( 30960 ), "by_section_student", ),
                                        ( xbmc.getLocalizedString( 30961 ), "by_section_business", ),
                                        ( xbmc.getLocalizedString( 30962 ), "by_section_sports", ),
                                        ( xbmc.getLocalizedString( 30963 ), "by_section_weather", ),
                                        ( xbmc.getLocalizedString( 30964 ), "top_stories", ),
                                    )
            elif ( self.args.category == "ireports" ):
                categories = (
                                        ( xbmc.getLocalizedString( 30965 ), "ireport_newsiest_now", ),
                                        ( xbmc.getLocalizedString( 30966 ), "ireport_on_cnn", ),
                                        ( xbmc.getLocalizedString( 30967 ), "ireport_sound_off", ),
                                        ( xbmc.getLocalizedString( 30968 ), "ireport_off_beat", ),
                                        ( xbmc.getLocalizedString( 30969 ), "cnni_programs_ireport", ),
                                    )
            elif ( self.args.category == "ontv" ):
                categories = (
                                        ( xbmc.getLocalizedString( 30980 ), "cnn_programs_american_morning", ),
                                    )
            elif ( self.args.category == "espanol" ):
                categories = (
                                        ( xbmc.getLocalizedString( 30970 ), "spanish_eleccions", ),
                                        ( xbmc.getLocalizedString( 30971 ), "spanish_economia", ),
                                        ( xbmc.getLocalizedString( 30972 ), "spanish_tu_dinero", ),
                                        ( xbmc.getLocalizedString( 30973 ), "spanish_vida", ),
                                        ( xbmc.getLocalizedString( 30974 ), "spanish_entretenimiento", ),
                                        ( xbmc.getLocalizedString( 30975 ), "spanish_tecnologia", ),
                                        ( xbmc.getLocalizedString( 30976 ), "spanish_estados_unidos", ),
                                        ( xbmc.getLocalizedString( 30977 ), "spanish_america_latina", ),
                                        ( xbmc.getLocalizedString( 30978 ), "spanish_spanish_mundo", ),
                                    )
            # fill media list
            ok = self._fill_media_list( categories )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        if ( ok ):
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            # set our plugin category
            xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

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
                icon = "defaultfolder.png"
                # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem=xbmcgui.ListItem( title, iconImage=icon, thumbnailImage=thumbnail )
                # add the different infolabels we want to sort by
                listitem.setInfo( type="Video", infoLabels={ "Title": title } )
                # add the item to the media list
                ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=True, totalItems=len( categories ) )
                # if user cancels, call raise to exit loop
                if ( not ok ): raise
        except:
            # user cancelled dialog or an error occurred
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        return ok

    def _get_thumbnail( self, title ):
        # create the full thumbnail path for skins directory
        thumbnail = os.path.join( sys.modules[ "__main__" ].__plugin__, title + ".png" )
        # use a plugin custom thumbnail if a custom skin thumbnail does not exists
        if ( not xbmc.skinHasImage( thumbnail ) ):
            # create the full thumbnail path for plugin directory
            thumbnail = os.path.join( self.BASE_PLUGIN_THUMBNAIL_PATH, title + ".png" )
            # use a default thumbnail if a custom thumbnail does not exists
            if ( not os.path.isfile( thumbnail ) ):
                thumbnail = ""
        return thumbnail
