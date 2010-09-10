""" Lyrics module """

import os
import xbmc
from codecs import BOM_UTF8
import re
from resources.lib.scraper import Scraper
if ( os.environ.get( "OS", "n/a" ) == "xbox" ):
    import base64

# needs to be global as song and prefetched_song are two instances
lyrics_cache = dict()


class Lyrics:
    """
        Fetches, cleans and saves lyrics.
    """

    def __init__( self, Addon, prefetch ):
        # set our Addon class
        self.Addon = Addon
        # is this prefetch
        self.prefetch = prefetch
        # info regex
        self.clean_info_regex = re.compile( "\[[a-z]+?:.*\]\s" )
        # lrc regex
        self.clean_lrc_lyrics_regex = re.compile( "\[([0-9]+):([0-9]+(?:\.[0-9]+)?)\](.*)" )
        # Overall timestamp adjustment in milliseconds regex
        self.timestamp_lrc_lyrics_regex = re.compile( "\[offset:([+-]*[0-9]+)\]" )
        # Website downloaded from regex
        self.website_regex = re.compile( "\[we:(.+)\]" )
        # set our scraper object
        self.scraper = Scraper( self.Addon, prefetch=self.prefetch )

    def get_lyrics( self, song ):
        try:
            # needs to be global as song and prefetched_song are two instances
            global lyrics_cache
            # set key
            cachename = xbmc.getCacheThumbName( song.artist + song.title )
            # if cached lyrics are found set them
            if ( lyrics_cache.has_key( cachename ) ):
                # FIXME: deleting them loses the prefetched song when skipping backwards
                if ( not self.prefetch ):
                    # loop thru and set all attributes
                    for key, value in lyrics_cache[ cachename ].iteritems():
                        setattr( song, key, value )
                    # delete cached lyrics as they should be saved now.
                    del lyrics_cache[ cachename ]
                # cached lyrics are already cleaned
                return
            # if embedded lyrics are found set them
            elif ( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Lyrics" % ( self.prefetch, ) ) ):
                song.lyrics = unicode( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Lyrics" % ( self.prefetch, ) ), "utf-8", "replace" )
                song.message = self.Addon.getLocalizedString( 30861 )
            # if saved lyrics are found set them
            else:
                # use httpapi for xbox, with hack for change in xbmc so older revisions still work
                if ( song.lyrics_path.startswith( "smb://" ) and os.environ.get( "OS", "n/a" ) == "xbox" ):
                    song.lyrics = unicode( base64.standard_b64decode( xbmc.executehttpapi( "FileDownload(%s,bare)" % ( song.lyrics_path, ) ).split("\r\n\r\n")[ -1 ].strip( BOM_UTF8 ) ), "utf-8" )
                else:
                    song.lyrics = unicode( open( song.lyrics_path, "r" ).read().strip( BOM_UTF8 ), "utf-8" )
                # set saved message
                song.message = self.Addon.getLocalizedString( 30862 )
        except Exception, e:
            # no lyrics found, so fetch lyrics from internet
            self.scraper.fetch_lyrics( song )
            # if the search was successful save lyrics
            if ( song.status ):
                self.save_lyrics( song )
        # we need to clean lyrics in case they are lrc tagged
        self._clean_lyrics( song )
        # cache lyrics only if prefetch, we only cache for the fetched message.
        # TODO: consider removing this since the fetched message is only good once
        if ( self.prefetch and song.status ):
            lyrics_cache[ cachename ] = {
                "lyrics": song.lyrics,
                "lrc_lyrics": song.lrc_lyrics,
                "website": song.website,
                "message": song.message,
                "status": song.status,
                "lyric_tags": song.lyric_tags,
                "prefetched": True
            }

    def _clean_lyrics( self, song ):
        # nothing to clean?
        if ( song.lyrics is None ): return
        # default to lrc lyrics
        lrc_lyrics = True
        # get website
        if ( song.website is None ):
            try:
                song.website = self.website_regex.search( song.lyrics ).group( 1 )
            except:
                song.website = ""
        # eliminate info block
        song.lyrics = self.clean_info_regex.sub( "", song.lyrics )
        # separate lyrics and time stamps
        lyrics = self.clean_lrc_lyrics_regex.findall( song.lyrics )
        # autoscroll if lyrics not tagged and user preference
        if ( not lyrics and self.Addon.getSetting( "autoscroll_lyrics" ) == "true" ):
            # split lines
            lines = song.lyrics.strip().splitlines()
            # get total time
            total_time = int( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Duration" % ( self.prefetch, ) ).split( ":" )[ 0 ] ) * 60 + int( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Duration" % ( self.prefetch, ) ).split( ":" )[ 1 ] )
            # we set the same amount of time per lyric, what do you expect?
            lyric_time = float( total_time ) / len( lines )
            # enumerate thru and set each tagged lyric
            lyrics = [ [ str( int( ( ( count + 1 ) * lyric_time ) / 60 ) ), str( float( ( count + 1 ) * lyric_time ) % 60 ), lyric ] for count, lyric in enumerate( lines ) ]
            # these are non lrc lyrics
            lrc_lyrics = False
        # format lyrics
        if ( lyrics ):
            # set lyric type
            song.lrc_lyrics = lrc_lyrics
            # get any timestamp adjustment
            try:
                offset = float( self.timestamp_lrc_lyrics_regex.search( song.lyrics ).group( 1 ) ) / 1000
            except:
                offset = 0
            # reset lyrics
            song.lyrics = ""
            # loop thru and set our lyrics
            for lyric in lyrics:
                # valid lyric, add it
                song.lyric_tags.append( int( lyric[ 0 ] ) * 60 + float( lyric[ 1 ] ) + offset )
                song.lyrics += lyric[ 2 ].strip() + "\n"
        # strip lyrics 
        song.lyrics = song.lyrics.strip()

    def save_lyrics( self, song ):
        try:
            # format lyrics with song info header
            song.lyrics = "[ti:%s]\n[ar:%s]\n[al:%s]\n[re:%s]\n[ve:%s]\n[we:%s]\n[offset:0]\n\n%s" % (
                song.title,
                song.artist,
                song.album,
                self.Addon.getAddonInfo( "Name" ),
                self.Addon.getAddonInfo( "Version" ),
                song.website,
                song.lyrics,
            )
            # use httpapi for xbox, with hack for change in xbmc so older revisions still work
            if ( song.lyrics_path.startswith( "smb://" ) and os.environ.get( "OS", "n/a" ) == "xbox" ):
                # no way to create dirs on smb:// paths
                xbmc.executehttpapi( "FileUpload(%s,%s)" % ( song.lyrics_path, base64.standard_b64encode( BOM_UTF8 + song.lyrics.encode( "utf-8", "replace" ) ), ) )
            else:
                # if the path to the source file does not exist create it
                self._makedirs( os.path.dirname( song.lyrics_path ) )
                # save lyrics
                open( song.lyrics_path, "w" ).write( BOM_UTF8 + song.lyrics.encode( "utf-8", "replace" ) )
        except Exception, e:
            # log error
            xbmc.log( "Lyrics::save_lyrics (%s)" % ( e, ), xbmc.LOGERROR )
            # set error message
            song.message = self.Addon.getLocalizedString( 30852 ) % ( e, )
            song.status = False

    # FIXME: eliminate this if os.makedirs is wrapped properly
    def _makedirs( self, _path ):
        def _convert_smb_path( _path ):
            # if windows and smb:// convert to a proper format for shutil and os modules
            if ( _path.startswith( "smb://" ) and os.environ.get( "OS", "win32" ) == "win32" ):
                _path = _path.replace( "/", "\\" ).replace( "smb:", "" )
            # return result
            return _path
       # no need to create folders
        if ( os.path.isdir( _path ) ): return
        # temp path
        tmppath = _path
        # loop thru and create each folder
        while ( not os.path.isdir( tmppath ) ):
            try:
                os.mkdir( _convert_smb_path( tmppath ) )
            except:
                tmppath = os.path.dirname( tmppath )
        # call function until path exists
        self._makedirs( _path )
