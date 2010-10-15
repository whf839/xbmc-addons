""" Song module """

import os
import xbmc
from resources.lib.lyrics import Lyrics


class Song:
    """
        Parses song info and holds all song attributes.
    """

    def __init__( self, Addon, prefetch=False ):
        # set our Addon class
        self.Addon = Addon
        # our we prefetching
        self.prefetch = prefetch
        # initialize our Lyrics class
        self.Lyrics = Lyrics( self.Addon, prefetch=self.prefetch )

    def _clear_song_attributes( self ):
        # initialize our song attributes
        self.artist = None
        self.album = None
        self.title = None
        self.message = None
        self.website = None
        self.status = True
        self.lyrics = None
        self.lyric_tags = list()
        self.lrc_lyrics = False
        self.lyrics_path = None
        self.prefetched = False

    def get_song_info( self ):
        # clear song info
        self._clear_song_attributes()
        # fetch next song info
        if ( self.prefetch and not xbmc.getCondVisibility( "MusicPlayer.HasNext" ) ): return
        # get song info from infolabels
        self.artist = unicode( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Artist" % ( self.prefetch, ) ), "utf-8" )
        self.album = unicode( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Album" % ( self.prefetch, ) ), "utf-8" )
        self.title = unicode( xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Title" % ( self.prefetch, ) ), "utf-8" )
        file = xbmc.getInfoLabel( "MusicPlayer.Offset(%d).Filename" % ( self.prefetch, ) )
        # if no proper tags, parse from filename
        if ( not self.artist or not self.title ):
            self._get_song_info_from_filename( file )
        # no song info found so skip
        if ( self.artist is None ):
            # set no song info error message and status
            self.message = self.Addon.getLocalizedString( 30850 )
            self.status = False
        else:
            # set fatx filesystem? this is ignored for XBMC so no need to check if xbox
            fatx = not file.startswith( "smb://" )
            # we use "Unknown" for non existent albums. it's only used for tagging lyrics
            if ( self.album is None or self.album == "" ):
                self.album = u"Unknown"
            # set shared path if user preference
            if ( self.Addon.getSetting( "lyrics_save_mode" ) == "0" ):
                # set user subfolder preference
                if ( self.Addon.getSetting( "lyrics_subfolder_template" ) == r"%A/" ):
                    subfolder = xbmc.makeLegalFilename( self.artist, fatx )
                else:
                    subfolder = os.path.join( xbmc.makeLegalFilename( self.artist, fatx ), xbmc.makeLegalFilename( self.album,fatx ) )
                # create full path
                self.lyrics_path = xbmc.validatePath( os.path.join( xbmc.translatePath( self.Addon.getSetting( "lyrics_save_path" ) ), subfolder, xbmc.makeLegalFilename( os.path.splitext( os.path.basename( file ) )[ 0 ] + self.Addon.getSetting( "lyrics_save_extension" ), fatx ) ) )
            # set song path if user preference
            elif ( self.Addon.getSetting( "lyrics_save_mode" ) == "1" ):
                # split file from folder
                folder, file = os.path.split( file )
                # change extension
                file = os.path.splitext( file )[ 0 ] + self.Addon.getSetting( "lyrics_save_extension" )
                # create path
                self.lyrics_path = xbmc.makeLegalFilename( os.path.join( folder, self.Addon.getSetting( "lyrics_subfolder" ), file ), fatx )
            # get lyrics
            self.Lyrics.get_lyrics( self )

    def _get_song_info_from_filename( self, file ):
        try:
            # log message
            xbmc.log( "Song::_get_song_info_from_filename (format=%s, file=%s)" % ( self.Addon.getSetting( "song_filename_template" ), file, ), xbmc.LOGDEBUG )
            # parse artist/title from filename
            if ( self.Addon.getSetting( "song_filename_template" ) == r"[%N - ]%A - %T" ):
                artist, title = os.path.splitext( os.path.basename( file ) )[ 0 ].split( "-" )[ -2 : ]
                album = "Unknown"
            # parse artist and album from folder names, title from filename
            elif ( self.Addon.getSetting( "song_filename_template" ) == r"%A/%B/[%N - ][%A - ]%T" ):
                artist = os.path.basename( os.path.dirname( os.path.dirname( file ) ) )
                album = os.path.basename( os.path.dirname( file ) )
                title = os.path.splitext( os.path.basename( file ) )[ 0 ].split( "-" )[ -1 ]
            # clean and make a unicode object
            self.artist = unicode( artist.strip(), "utf-8" )
            self.album = unicode( album.strip(), "utf-8" )
            self.title = unicode( title.strip(), "utf-8" )
        except Exception, e:
            # log error
            xbmc.log( "Invalid file format setting (%s)" % ( e, ), xbmc.LOGERROR )
            # clear song info if a parsing error occurred
            self._clear_song_attributes()
