"""
Local trailer scraper
"""
# TODO: add watched.xml to skip watched trailers

import os, sys
import xbmc
from random import shuffle
import xbmcaddon

_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
from folder import dirEntries


class Main:
    xbmc.log("Local trailer scraper", xbmc.LOGNOTICE )
    # base paths
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )

    def __init__( self, mpaa=None, genre=None, settings=None, movie=None ):
        self.mpaa = mpaa
        self.genre = genre
        self.settings = settings
        self.movie = movie
        self.trailers = []
        self.tmp_trailers = []

    def fetch_trailers( self ):
        xbmc.log("[script.cinema.experience] - Fetching Trailers", xbmc.LOGNOTICE )
        # get watched list
        self._get_watched()
        # fetch all trailers recursively
        self.tmp_trailers = dirEntries( self.settings[ "trailer_folder" ], "video", "TRUE", "-trailer" )
        # get a random number of trailers
        self._shuffle_trailers()
        # save watched list
        self._save_watched()
        # return results
        return self.trailers

    def _shuffle_trailers( self ):
        # randomize the groups and create our play list
        xbmc.log("[script.cinema.experience] - Shuffling Trailers", xbmc.LOGNOTICE )
        shuffle( self.tmp_trailers )
        # reset counter
        count = 0
        # now create our final playlist
        for trailer in self.tmp_trailers:
            # user preference to skip watch trailers
            if ( self.settings[ "trailer_unwatched_only" ] and xbmc.getCacheThumbName( trailer ) in self.watched ):
                continue
            # add id to watched file TODO: maybe don't add if not user preference
            self.watched += [ xbmc.getCacheThumbName( trailer ) ]
            # add trailer to our final list
            self.trailers += [ self._set_trailer_info( trailer ) ]
            # increment counter
            count += 1
            # if we have enough exit
            if ( count == self.settings[ "trailer_count" ] ):
                break
        if ( len(self.trailers) == 0 and self.settings[ "trailer_unwatched_only" ] and len( self.watched ) > 0 ):
             self._reset_watched()
             #attempt to load our playlist again
             self._shuffle_trailers()

    def _set_trailer_info( self, trailer ):
        xbmc.log("[script.cinema.experience] - Setting Trailer Info", xbmc.LOGNOTICE )
        result = ( xbmc.getCacheThumbName( trailer ), # id
                        os.path.basename( trailer ).split( "-trailer." )[ 0 ], # title
                        trailer, # trailer
                        self._get_thumbnail( trailer ), # thumb
                        "", # plot
                        "", # runtime
                        "", # mpaa
                        "", # release date
                        "", # studio
                        "", # genre
                        _L_( 32605 ), # writer
                        _L_( 32605 ), # director 32613
                        )
        return result

    def _get_thumbnail( self, path ):
        xbmc.log("[script.cinema.experience] - Getting Thumbnail", xbmc.LOGNOTICE )
        # check for a thumb based on trailername.tbn
        thumbnail = os.path.splitext( path )[ 0 ] + ".tbn" 
        # if thumb does not exist try stripping -trailer
        if ( not xbmc.executehttpapi( "FileExists(%s)" % ( thumbnail, ) ) == "<li>True" ):
            thumbnail = "%s.tbn" % ( os.path.splitext( path )[ 0 ].replace( "-trailer", "" ), )
            # if thumb does not exist return empty
            if ( not xbmc.executehttpapi( "FileExists(%s)" % ( thumbnail, ) ) == "<li>True" ):
                # set empty string
                thumbnail = None
        # return result
        return thumbnail

    def _get_watched( self ):
        xbmc.log("[script.cinema.experience] - Getting Watched List", xbmc.LOGNOTICE )
        try:
            # base path to watched file
            base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] + "_watched.txt" )
            # open path
            usock = open( base_path, "r" )
            # read source
            self.watched = eval( usock.read() )
            # close socket
            usock.close()
        except:
            self.watched = []
            
    def _reset_watched( self ):
        xbmc.log("[script.cinema.experience] - Resetting Watched List", xbmc.LOGNOTICE )
        base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] + "_watched.txt" )
        if ( os.path.isfile( base_path ) ):
            os.remove( base_path )
            self.watched = []

    def _save_watched( self ):
        xbmc.log("[script.cinema.experience] - Saving Watched List", xbmc.LOGNOTICE )
        try:
            # base path to watched file
            base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] +"_watched.txt" )
            # if the path to the source file does not exist create it
            if ( not os.path.isdir( os.path.dirname( base_path ) ) ):
                os.makedirs( os.path.dirname( base_path ) )
            # open source path for writing
            file_object = open( base_path, "w" )
            # write xmlSource
            file_object.write( repr( self.watched ) )
            # close file object
            file_object.close()
        except:
            pass
