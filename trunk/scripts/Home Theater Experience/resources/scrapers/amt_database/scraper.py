"""
Apple Movie Trailers script database scraper
"""

import sys
import os

import xbmc

from random import randrange
from urllib import quote_plus
import datetime

# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( os.getcwd(), "resources", "platform_libraries", env ) )
from pysqlite2 import dbapi2 as sqlite


class Main:
    BASE_DATA_PATH = os.path.join( xbmc.translatePath( "special://masterprofile/" ), "script_data", "Apple Movie Trailers" )

    def __init__( self, mpaa=None, genre=None, settings=None ):
        self.mpaa = mpaa
        self.genre = genre
        self.settings = settings

    def clear_watched( self ):
        # make db connection
        records = Records( amt_db_path=self.settings[ "amt_db_path" ] )
        # clear watched sql
        sql ="UPDATE movies SET times_watched=0, last_watched=''"
        # update the record with our new values
        ok = records.update( sql )
        # close the database
        records.close()

    def fetch_trailers( self ):
        try:
            #  initialize our trailer list
            trailers = []
            # make db connection
            records = Records( amt_db_path=self.settings[ "amt_db_path" ] )
            # select only trailers with valid trailer urls sql
            sql = """
                        SELECT movies.*, studios.studio, genres.genre  
                        FROM movies, genres, genre_link_movie, studios, studio_link_movie 
                        WHERE movies.trailer_urls IS NOT NULL 
                        AND movies.trailer_urls!='[]' 
                        %s
                        %s
                        %s
                        %s
                        AND genre_link_movie.idMovie=movies.idMovie 
                        AND genre_link_movie.idGenre=genres.idGenre 
                        AND studio_link_movie.idMovie=movies.idMovie 
                        AND studio_link_movie.idStudio=studios.idStudio 
                        ORDER BY RANDOM() 
                        LIMIT %d;
                    """
            # mpaa ratings
            mpaa_ratings = { "G": 0, "PG": 1, "PG-13": 2, "R": 3, "NC-17": 4 }
            # set the proper mpaa rating user preference
            self.mpaa = ( self.settings[ "trailer_rating" ], self.mpaa, )[ self.settings[ "limit_query" ] ]
            # rating query
            rating_sql = ( "", "AND (%s)" % " ".join( [ "rating='%s' OR" % rating for rating, index in mpaa_ratings.items() if index <= mpaa_ratings.get( self.mpaa, -1 ) ] )[ : -3 ], )[ mpaa_ratings.has_key( self.mpaa ) ]
            # HD only query, only for amt db source
            hd_sql = ( "", "AND (movies.trailer_urls LIKE '%720p.mov%' OR movies.trailer_urls LIKE '%1080p.mov%')", )[ self.settings[ "amt_hd_only" ] and ( self.settings[ "trailer_quality" ] > 3 ) ]
            # Only unwatched query, only for amt db source
            watched_sql = ( "", "AND movies.times_watched=0", )[ self.settings[ "unwatched_only" ] ]
            # genre query, only for amt db source
            genre_sql = ( "", "AND genres.genre='Newest'", )[ self.settings[ "amt_newest_only" ] and not self.settings[ "limit_query" ] ]
            genres = self.genre.replace( "Sci-Fi", "Science Fiction" ).replace( "Action", "Action and ADV" ).replace( "Adventure", "ACT and Adventure" ).replace( "ACT",  "Action" ).replace( "ADV",  "Adventure" ).split( " / " )
            genre_sql = ( genre_sql, "AND (%s)" % " ".join( [ "genres.genre='%s' OR" % genre for genre in genres ] )[ : -3 ], )[ self.settings[ "limit_query" ] ]
            # fetch our trailers
            result = records.fetch( sql % ( hd_sql, rating_sql, genre_sql, watched_sql, self.settings[ "number_trailers" ], ) )
            # close db connection
            records.close()
            # enumerate thru and set the needed info (TODO: maybe search for all genres)
            for trailer in result:
                # append trailer
                trailers += [ ( trailer[ 0 ], # id
                                    trailer[ 1 ], # title
                                    self._get_trailer_url( trailer[ 3 ] ), # trailer
                                    os.path.join( self.BASE_DATA_PATH, ".cache", trailer[ 4 ][ 0 ], trailer[ 4 ] ), # thumb
                                    trailer[ 5 ], # plot
                                    trailer[ 6 ], # runtime
                                    trailer[ 7 ], # mpaa
                                    trailer[ 9 ], # release date
                                    trailer[ 15 ], # studio
                                    trailer[ 16 ], # genre
                                    "", # writer
                                    "", # director
                                    ) ]
                # mark trailer watched
                self._mark_watched( trailer[ 0 ] )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        # return result
        return trailers

    def _get_trailer_url( self, trailer_urls ):
        # pick a random url (only applies to multiple urls)
        r = randrange( len( trailer_urls ) )
        # get intial choice
        choice = ( self.settings[ "trailer_quality" ], len( trailer_urls[ r ] ) - 1, )[ self.settings[ "trailer_quality" ] >= len( trailer_urls[ r ] ) ]
        # if quality is non progressive
        if ( self.settings[ "trailer_quality" ] <= 2 ):
            # select the correct non progressive trailer
            while ( trailer_urls[ r ][ choice ].endswith( "p.mov" ) and choice != -1 ): choice -= 1
        # quality is progressive
        else:
            # select the proper progressive quality
            quality = ( "480p", "720p", "1080p", )[ self.settings[ "trailer_quality" ] - 3 ]
            # select the correct progressive trailer
            while ( quality not in trailer_urls[ r ][ choice ] and trailer_urls[ r ][ choice ].endswith( "p.mov" ) and choice != -1 ): choice -= 1
        # if there was a valid trailer set it
        url = ""
        if ( choice >= 0 ):
            url = trailer_urls[ r ][ choice ]
        # return choice
        return url

    def _mark_watched( self, idMovie ):
        try:
            # our database object
            records = Records( amt_db_path=self.settings[ "amt_db_path" ] )
            # needed sql commands
            fetch_sql = "SELECT times_watched FROM movies WHERE idMovie=?;"
            update_sql = "UPDATE movies SET times_watched=?, last_watched=? WHERE idMovie=?;"
            # we fetch the times watched so we can increment by one
            result = records.fetch( fetch_sql, ( idMovie, ) )
            if ( result ):
                # increment the times watched
                times_watched = result[ 0 ][ 0 ] + 1
                # get todays date
                last_watched = datetime.date.today()
                # update the record with our new values
                ok = records.update( update_sql, ( times_watched, last_watched, idMovie, ) )
            # close the database
            records.close()
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )


class Records:
    def __init__( self, *args, **kwargs ):
        self.connect( kwargs[ "amt_db_path" ] )

    def connect( self, db ):
        self.db = sqlite.connect( db )
        self.cursor = self.db.cursor()

    def commit( self ):
        try:
            self.db.commit()
            return True
        except: return False

    def close( self ):
        self.db.close()
    
    def fetch( self, sql, params=None ):
        try:
            if ( params is not None ): self.cursor.execute( sql, params )
            else: self.cursor.execute( sql )
            retval = self.cursor.fetchall()
        except:
            retval = None
        return retval

    def update( self, sql, params=None ):
        try:
            if ( params is None ):
                self.cursor.execute( sql )
            else:
                self.cursor.execute( sql, params )
            ok = self.commit()
            return True
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return False
