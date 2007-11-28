"""
    Player module: plays the selected video
"""

# create the progress dialog (we do it here so there is minimal delay with nothing displayed)
import xbmcgui
pDialog = xbmcgui.DialogProgress()
pDialog.create( "Yahoo Music Videos Plugin", "Getting session ID..." )

# main imports
import sys
import os
import xbmc
import traceback

from YahooAPI.YahooClient import YahooClient


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class Main:
    # base paths
    BASE_CACHE_PATH = os.path.join( "P:\\", "Thumbnails", "Video" )

    def __init__( self ):
        self._parse_argv()
        # get our url
        url = self.construct_url()
        if ( self.args.download_path ):
            self.download_video( url )
        else:
            self.play_video( url )

    def _parse_argv( self ):
        # call _Info() with our formatted argv to create the self.args object
        exec "self.args = _Info(%s)" % ( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ).replace( "\\u0027", "'" ).replace( "\\u0022", '"' ).replace( "\\u0026", "&" ), )
        self.args.url = self.args.url.replace( "-*-*-", "&" )

    def download_video( self, url ):
        import urllib
        try:
            # construct an xbox compatible filepath
            ext = os.path.splitext( url )[ 1 ]
            if ( len( ext ) != 4 ):
                ext = ".avi"
            filepath = self.make_legal_filepath( self.args.title + ext )
            if ( not os.path.isfile( filepath ) ):
                # fetch the video
                urllib.urlretrieve( url, filepath, self._report_hook )
            # play the downloaded video
            self.play_video( filepath )
        except:
            pDialog.close()
            if ( os.path.isfile( filepath ) ):
                os.remove( filepath )

    def _report_hook( self, count, blocksize, totalsize ):
        percent = int( float( count * blocksize * 100) / totalsize )
        pDialog.update( percent, "Downloading video..." )
        if ( pDialog.iscanceled() ): raise

    def make_legal_filepath( self, title ):
        # construct the filename
        environment = os.environ.get( "OS", "xbox" )
        path = os.path.join( self.args.download_path, title ).replace( "\\", "/" )
        drive = os.path.splitdrive( path )[ 0 ]
        parts = os.path.splitdrive( path )[ 1 ].split( "/" )
        if ( not drive and parts[ 0 ].endswith( ":" ) and len( parts[ 0 ] ) == 2 ):
            drive = parts[ 0 ]
            parts[ 0 ] = ""
        if ( environment == "xbox" or environment == "win32" ):
            illegal_characters = """,*=|<>?;:"+"""
            for count, part in enumerate( parts ):
                tmp_name = ""
                for char in part:
                    # if char's ord() value is > 127 or an illegal character remove it
                    if ( char in illegal_characters or ord( char ) > 127 ): char = ""
                    tmp_name += char
                if ( environment == "xbox" ):
                    if ( len( tmp_name ) > 42 ):
                        if ( count == len( parts ) - 1 ):
                            ext = os.path.splitext( tmp_name )[ 1 ]
                            tmp_name = "%s%s" % ( os.path.splitext( tmp_name )[ 0 ][ : 42 - len( ext ) ].strip(), ext, )
                        else:
                            tmp_name = tmp_name[ : 42 ].strip()
                parts[ count ] = tmp_name
        filepath = xbmc.translatePath( drive + "/".join( parts ) )
        if ( environment == "win32" ):
            return filepath.encode( "utf-8" )
        else:
            return filepath

    def play_video( self, url=None ):
        # call _get_thumbnail() for the path to the cached thumbnail
        thumbnail = self._get_thumbnail( sys.argv[ 0 ] + sys.argv[ 2 ] )
        pDialog.close()
        if ( not pDialog.iscanceled() ):
            listitem = xbmcgui.ListItem( self.args.title, thumbnailImage=thumbnail )
            listitem.setInfo( "video", { "Title": self.args.title, "Genre": self.args.studio } )
            xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play( url, listitem )

    def construct_url( self ):
        # Yahoo client
        client = YahooClient()
        if ( "yahoo" in self.args.url ):
            url = client.construct_yahoo_video_url( self.args.url )
        elif ( "youtube" in self.args.url ):
            url = client.construct_youtube_video_url( self.args.url )
        else:
            url = self.args.url
        return url

    def _get_thumbnail( self, url ):
        # make the proper cache filename and path
        filename = xbmc.getCacheThumbName( url )
        filepath = xbmc.translatePath( os.path.join( self.BASE_CACHE_PATH, filename[ 0 ], filename ) )
        return filepath
