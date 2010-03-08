import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

#
#
#
class Main :
    def __init__( self ) :
        #
        # Init
        #
        
        # Parse parameters...
        #
        params   = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))        
        searchBy = params[ "search_by" ]

        #
        # Playing movie...
        #
        if searchBy == "playing" :
            movieFullPath = xbmc.Player().getPlayingFile()
        #
        # Browse for movie file...
        #
        else :
            browse = xbmcgui.Dialog()
            movieFullPath = browse.browse(1, "xnapi", "video", ".avi|.mpg|.mpeg|.wmv|.asf|.divx|.mov|.m2p|.moov|.omf|.qt|.rm|.vob|.dat|.dv|.3ivx|.mkv|.ogm")
            
            # No file selected...
            if movieFullPath == "" :
                xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )
                return
        import xnapi_download 
        xnapi_download.Download(movieFullPath)
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
