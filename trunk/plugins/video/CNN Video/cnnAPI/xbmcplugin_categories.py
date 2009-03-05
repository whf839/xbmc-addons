"""
    Category module: fetches a list of categories to use as folders
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

from sgmllib import SGMLParser
import urllib


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class _Parser( SGMLParser ):
    """
        Parses an html document for categories
    """
    # base urls
    BASE_URL = "http://www.cnn.com/"

    def reset( self ):
        SGMLParser.reset( self )
        # list of _Info() objects
        self.categories = []
        self._init_vars()

    def _init_vars( self ):
        # reset content variables
        self.title = []
        self.category = ""

    def start_a( self, attrs ):
        # links are in href keys
        for key, value in attrs:
            # if it is a valid category set it
            if ( key == "href" and value.startswith( "javascript:load" ) and "," in value ):
                self.category = value.split( "," )[ 1 ].strip().replace( "'", "" ).replace( ";", "" ).replace( ")", "" )[ 1 : ]

    def end_a( self ):
        # if we found a valid category add it to our list and reset content variables
        if ( self.category ):
            self.make_object( " ".join( self.title ), self.category )
            self._init_vars()

    def handle_data( self, text ):
        # if we found a valid category grab the category title
        if ( self.category ):
            self.title += [ text.title().replace( "Cnn", "CNN" ).replace( "Tv", "TV" ) ]

    def make_object( self, title, category ):
        # add item to our _Info() object list
        self.categories += [ _Info( title=title, url=self.BASE_URL + category ) ]


class Main:
    # base urls
    BASE_CATEGORY_URL = "http://www.cnn.com/video"

    # base paths
    BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( os.getcwd(), "thumbnails" )

    def __init__( self ):
        self.get_categories()

    def get_categories( self ):
        try:
            # open url
            usock = urllib.urlopen( self.BASE_CATEGORY_URL )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
            # Parse htmlSource for categories
            parser = _Parser()
            parser.feed( htmlSource )
            parser.close()
            # fill media list
            ok = self._fill_media_list( parser.categories )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

    def _fill_media_list( self, categories ):
        try:
            ok = True
            # enumerate through the list of categories and add the item to the media list
            for category in categories:
                url = "%s?title=%s&url=%s" % ( sys.argv[ 0 ], category.title, category.url, )
                # check for a valid custom thumbnail for the current category
                thumbnail = self._get_thumbnail( category.title )
                # set the default icon
                icon = "defaultfolder.png"
                # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem=xbmcgui.ListItem( category.title, iconImage=icon, thumbnailImage=thumbnail )
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
