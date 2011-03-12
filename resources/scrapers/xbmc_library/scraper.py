"""
XBMC Movie Library Trailer Scraper
"""

import sys
import os
import xbmcaddon
import xbmc

from random import shuffle
from urllib import quote_plus
import datetime, traceback

_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString

sys.path.append( os.path.join( _A_.getAddonInfo('path'), "resources" ) )

__useragent__ = "QuickTime/7.2 (qtver=7.2;os=Windows NT 5.1Service Pack 3)"


class Main:
    print "XBMC Movie Library Trailer Scraper"
    
    def __init__( self, mpaa=None, genre=None, settings=None, movie=None ):
        self.mpaa = mpaa
        self.genre = genre.split( " / " )
        self.settings = settings
        #  initialize our trailer list
        self.trailers = []

    def fetch_trailers( self ):        
        # get watched list
        self._get_watched()
        count = 0
        sqlquery = """SELECT movieview.c00, movieview.c19, movieview.c12, movieview.c14 from movieview WHERE NOT c19="" ORDER BY RANDOM()"""
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(CloseRecord;</record>;OpenField,)" )
        xbmc.log( "[script.cinema.experience]  - SQL: %s" % ( sqlquery, ), xbmc.LOGNOTICE )
        try:
            sqlresult = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sqlquery ), )
            #xbmc.log( "[script.cinema.experience] - sqlresult: %s" % sqlresult, xbmc.LOGNOTICE )
            sqlrecords = sqlresult.split("</record>")
            trailer_list = sqlrecords[ 0:len( sqlrecords ) -1 ]
            for trailer in trailer_list:
                title, trailer_path, trailer_ratingsql, trailer_genresql, dummy = trailer.split("</field>")
                # shorten MPAA/BBFC ratings
                if trailer_ratingsql == "":
                    trailer_ratingsql = "NR"
                elif trailer_ratingsql.startswith("Rated"):
                    trailer_ratingsql = trailer_ratingsql.split( " " )[ 1 - ( len( trailer_ratingsql.split( " " ) ) == 1 ) ]
                    trailer_ratingsql = ( trailer_ratingsql, "NR", )[ trailer_ratingsql not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", ) ]
                elif trailer_ratingsql.startswith("UK"):
                    trailer_ratingsql = trailer_ratingsql.split( ":" )[ 1 - ( len( trailer_ratingsql.split( ":" ) ) == 1 ) ]
                    trailer_ratingsql = ( trailer_ratingsql, "NR", )[ trailer_ratingsql not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
                else:
                    trailer_ratingsql = ( trailer_ratingsql, "NR", )[ trailer_ratingsql not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
                # add trailer to our final list
                if ( self.settings[ "trailer_unwatched_only" ] and xbmc.getCacheThumbName( trailer_path ) in self.watched ):
                    continue
                trailer_genre = trailer_genresql.split(" / ")
                if self.settings[ "trailer_limit_genre" ] and ( not list(set(trailer_genre) & set(self.genre) ) ):
                    xbmc.log("[script.cinema.experience] - Genre Not Matched - Skipping Trailer", xbmc.LOGNOTICE )
                    continue
                if self.settings[ "trailer_limit_mpaa" ] and ( not trailer_ratingsql or not trailer_ratingsql == self.mpaa ):
                    xbmc.log("[script.cinema.experience] - MPAA Not Matched - Skipping Trailer", xbmc.LOGNOTICE )
                    continue
                trailer_info = ( xbmc.getCacheThumbName( trailer_path ), # id
                                 title, # title
                                 trailer_path, # trailer
                                 self._get_thumbnail( trailer_path ), # thumb
                                 '', # plot
                                 '', # runtime
                                 trailer_ratingsql, # mpaa
                                 '', # release date
                                 '', # studio
                                 trailer_genresql, # genre
                                 _L_( 32605 ), # writer
                                 '', # director 32613
                                )
                self.trailers += [ trailer_info ]
                # add id to watched file TODO: maybe don't add if not user preference
                self.watched += [ xbmc.getCacheThumbName( trailer_path ) ]
                # increment counter
                count += 1
                # if we have enough exit
                if ( count == self.settings[ "trailer_count" ] ):
                   break
            return self.trailers
        except:
            xbmc.log( "[script.cinema.experience] - Error searching database", xbmc.LOGNOTICE )
            traceback.print_exc()

    def _get_thumbnail( self, path ):
        xbmc.log("[script.cinema.experience] - Getting Thumbnail", xbmc.LOGNOTICE )
        # check for a thumb based on trailername.tbn
        thumbnail = os.path.splitext( path )[ 0 ] + ".tbn"
        # if thumb does not exist try stripping -trailer
        if ( not os.path.isfile( thumbnail ) ):
            thumbnail = "%s.tbn" % ( os.path.splitext( path )[ 0 ].replace( "-trailer", "" ), )
            # if thumb does not exist return empty
            if ( not os.path.isfile( thumbnail ) ):
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

