#
# Imports
#
import sys
import xbmcgui
import xbmcplugin
import urllib
from xml.dom          import minidom
from xbmcplugin_utils import HTTPCommunicator

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        #
        # Get comics / categories...
        #
        self.getComics( )
        
    #
    # Get comics / categories...
    #
    def getComics(self):
        #
        # Get list (XML)...
        #
        httpCommunicator = HTTPCommunicator()
        dom              = minidom.parseString( httpCommunicator.get( "http://comics.com/xml/homepage_scroller/" ) )

        for comic in dom.getElementsByTagName("Comic") :
            #
            # Init
            #
            comic_name  = ""
            comic_url   = ""
            comic_thumb = ""
            
            #
            # Parse entry details...
            #
            for childNode in comic.childNodes:
                if childNode.nodeName == "Name" :
                    comic_name  = childNode.firstChild.data
                elif childNode.nodeName == "URL" :
                    comic_url   = childNode.firstChild.data
                elif childNode.nodeName == "FilePath_Thumb" :
                    comic_thumb = childNode.firstChild.data

                # Comic strip view (list)...
                plugin_url = "%s?action=list&comic_name=%s&comic_url=%s" % ( sys.argv[0], urllib.quote_plus( comic_name ), urllib.quote_plus( comic_url ) )
            
            #
            #  Add list item...
            # 
            listitem = xbmcgui.ListItem (comic_name, iconImage = "DefaultPicture.png", thumbnailImage = comic_thumb)
            listitem.setInfo( "pictures", { "title" : "comic_name" } )
            ok = xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = plugin_url, listitem = listitem, isFolder = True)

        #
        # End of list...
        #

        # Sort by label...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        
