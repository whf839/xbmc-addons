#
# Imports
#
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

#
# Main class
#
class Main:
    def __init__( self ):        
        #
        # Search by movie file...
        #
        listitem = xbmcgui.ListItem( "Search by movie file...", iconImage="DefaultFolder.png" )
        xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=search&search_by=hash' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)
        

        #
        # Search for playing movie...
        #
        if xbmc.Player().isPlayingVideo() :
            listitem = xbmcgui.ListItem( "Search for playing movie...", iconImage="DefaultFolder.png" )
            xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = '%s?action=search&search_by=playing' % ( sys.argv[ 0 ] ), listitem=listitem, isFolder=True)        
        
        #
        # Disable sorting...
        #
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
        
        #
        # End of list...
        #
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
