"""
    Plugin for streaming MPlayer's sample videos
"""

# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcplugin

import re
import urllib


# plugin constants
__plugin__ = "MPlayer Samples"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/videos/MPlayer%20Samples"
__credits__ = "Team XBMC"
__version__ = "1.0"


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class _Parser:
    """
        Parses an html document for category links
    """
    def __init__( self, htmlSource ):
        # initialize our content list
        self.items = []
        # get the list
        self._get_items( htmlSource )

    def _get_items( self, htmlSource ):
        # parse source for items
        items = re.findall( '<tr><td class="n"><a href="([^"]*)">[^<]*</a>/?</td><td class="m">([^<]*)</td><td class="s">([^<]*)</td><td class="t">([^<]*)<', htmlSource )
        # enumerate thru items and set directories and videos
        for item in items:
            # fix date
            try:
                mm = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ].index( item[ 1 ][ 5 : 8 ] )
                date = "%02d-%02d-%04d" % (  int( item[ 1 ][ 9 : 11 ] ), mm + 1, int( item[ 1 ][ : 4 ] ), )
            except:
                date = ""
            # fix size
            try:
                m = ( 1024, 1048576, )[ item[ 2 ].endswith( "M" ) ]
                size = int( float( item[ 2 ][ : -1 ] ) * m )
            except:
                size = 0
            # add our item
            if ( ( item[ 3 ] == "Directory" and item[ 0 ] != "../" ) or ( os.path.splitext( item[ 0 ] )[ 1 ] and os.path.splitext( item[ 0 ] )[ 1 ] in xbmc.getSupportedMedia( "video" ) ) ):
                self.items += [ ( item[ 0 ], date, size, ( item[ 3 ] == "Directory" ), ) ]


class Main:
    # base urls
    BASE_URL = "http://samples.mplayerhq.hu/"

    def __init__( self ):
        # parse our argv
        self._parse_argv()
        # get the sites assets
        ok = self.get_items()
        # send notification we're finished, successfully or unsuccessfully
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

    def _parse_argv( self ):
        # call _Info() with our formatted argv to create the self.args object
        if ( sys.argv[ 2 ] ):
            exec "self.args = _Info(%s)" % ( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ).replace( "\\u0027", "'" ).replace( "\\u0022", '"' ).replace( "\\u0026", "&" ), )
        else:
            self.args = _Info( url=self.BASE_URL )

    def get_items( self ):
        ok = False
        # fetch the web page
        htmlSource = self._get_html_source( self.args.url )
        # if we were succesfule, parse for videos and directories
        if ( htmlSource is not None ):
            items = self.parse_html_source( htmlSource )
            # if items were found, add them
            if ( items ):
                ok = self._fill_media_list( items )
        return ok

    def _get_html_source( self, url ):
        try:
            # open url
            usock = urllib.urlopen( url )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            htmlSource = None
        return htmlSource

    def parse_html_source( self, htmlSource ):
        # Parse htmlSource for directories and videos
        parser = _Parser( htmlSource )
        return parser.items

    def _fill_media_list( self, items ):
        try:
            ok = True
            # enumerate through the list of directories and add the item to the media list
            for ( title, date, size, itype, ) in items:
                # handle folders and videos differently
                if ( itype ):
                    url = "%s?url=%s" % ( sys.argv[ 0 ], repr( self.args.url + title ) )
                else:
                    url = self.args.url + title
                # set the default icon
                icon = ( "defaultVideo.png", "DefaultFolder.png", )[ itype ]
                # only need to add label and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem=xbmcgui.ListItem( urllib.unquote( title ), iconImage=icon )
                # set extra info
                listitem.setInfo( type="Video", infoLabels={ "Title": title, "Date": date, "Size": size } )
                # add the item to the media list
                ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=listitem, isFolder=itype, totalItems=len( items ) )
                # if user cancels, call raise to exit loop
                if ( not ok ): raise
        except:
            # user cancelled dialog or an error occurred
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            ok = False
        if ( ok ):
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_SIZE )
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
        return ok


if ( __name__ == "__main__" ):
    Main()
