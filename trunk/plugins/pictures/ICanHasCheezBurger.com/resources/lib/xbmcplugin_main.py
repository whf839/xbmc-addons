# ICanHasCheezBurger Random Lol XBMC Plugin
# Based on Dan Dare's Comics.com plugin
# 
# Modified from the original Comics.com plugin
#  by Brian Millham <brian@millham.net>
#
# Imports
#
import sys
import xbmcgui
import xbmcplugin
import urllib

#
# Main class
#
class Main:
    #
    # Init
    #
    def __init__(self):
        #
        # Get Lols
        #
        self.getLols( )
        
    #
    # Get Lols
    #
    def getLols(self):
        url_base = "http://api.cheezburger.com/xml/category/%s/lol/random/"
        lol_list = sorted(['Cats', 'Dogs', 'Objects',
                           'Other Animals', 'News', 'Celebs',
                           'Fail', 'Engrish', 'Comix'] )

        for lol in lol_list:
            lol_name = "Random Lol %s" % lol
            lol_url = url_base % lol
            plugin_url = "%s?action=list&lol_name=%s&lol_url=%s" % (
             sys.argv[0],
             urllib.quote_plus( lol_name ),
             urllib.quote_plus( lol_url ) )
            #
            #  Add list item...
            # 
            listitem = xbmcgui.ListItem (lol_name,
             iconImage = "DefaultPicture.png",
             thumbnailImage = "DefaultPicture.png")
            listitem.setInfo( "pictures", { "title" : "lol_name" } )
            ok = xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]),
             url = plugin_url,
             listitem = listitem,
             isFolder = True)

        #
        # End of list...
        #

        # Sort by label...
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
            
        # End of list...
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )        
