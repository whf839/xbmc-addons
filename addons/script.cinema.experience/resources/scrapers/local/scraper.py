"""
Local trailer scraper
"""
# TODO: add watched.xml to skip watched trailers

import os, sys, re
import xbmc
from random import shuffle
import xbmcaddon

_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
from folder import dirEntries


class Main:
    xbmc.log("[script.cinema.experience] - Local Folder Trailer Scraper Started", xbmc.LOGNOTICE )
    # base paths
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )

    def __init__( self, mpaa=None, genre=None, settings=None, movie=None ):
        self.mpaa = mpaa
        self.genre = genre.replace( "Sci-Fi", "Science Fiction" ).replace( "Action", "Action and ADV" ).replace( "Adventure", "ACT and Adventure" ).replace( "ACT",  "Action" ).replace( "ADV",  "Adventure" ).split( " / " )
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
            # add trailer to our final list
            trailer_info = self._set_trailer_info( trailer )
            trailer_genre = trailer_info[ 9 ].split(" / ")
            trailer_rating = trailer_info[ 6 ].replace("Rated ", "")
            if self.settings[ "trailer_limit_genre" ] and ( not list(set(trailer_genre) & set(self.genre) ) ):
                xbmc.log("[script.cinema.experience] - Genre Not Matched - Skipping Trailer", xbmc.LOGNOTICE )
                continue
            if self.settings[ "trailer_limit_mpaa" ] and ( not trailer_rating or not trailer_rating == self.mpaa ):
                xbmc.log("[script.cinema.experience] - MPAA Not Matched - Skipping Trailer", xbmc.LOGNOTICE )
                continue
            self.trailers += [ trailer_info ]
            # add id to watched file TODO: maybe don't add if not user preference
            self.watched += [ xbmc.getCacheThumbName( trailer ) ]
            # increment counter
            count += 1
            # if we have enough exit
            if ( count == self.settings[ "trailer_count" ] ):
                break
        if ( len(self.trailers) == 0 and self.settings[ "trailer_unwatched_only" ] and len( self.watched ) > 0 ):
            self._reset_watched()
            #attempt to load our playlist again
            self._shuffle_trailers()

    def _getnfo( self, path ):
        xbmc.log("[script.cinema.experience] - Retrieving Trailer NFO file", xbmc.LOGNOTICE )
        '''
            id=trailer[ 0 ]
            path=trailer[ 2 ],
            genre=trailer[ 9 ],
            title=trailer[ 1 ],
            thumbnail=trailer[ 3 ],
            plot=trailer[ 4 ],
            runtime=trailer[ 5 ],
            mpaa=trailer[ 6 ],
            release_date=trailer[ 7 ],
            studio=trailer[ 8 ],
            director=trailer[ 11 ]
        '''
        try:
            path = os.path.splitext( path )[0] + ".nfo"
            usock = open( path, "r" )
            # read source
            xmlSource =  usock.read()
            # close socket
            usock.close()
        except:
            xmlSource = ""
        xmlSource = xmlSource.replace("\n    ","")
        # if only
        xmlSource = xmlSource.replace('<movieinfo>','<movieinfo id="0">')
        # gather all trailer records <movieinfo>
        new_trailer = []
        trailer = re.findall( '<movieinfo id="(.*?)"><title>(.*?)</title><quality>(.*?)</quality><runtime>(.*?)</runtime><releasedate>(.*?)</releasedate><mpaa>(.*?)</mpaa><genre>(.*?)</genre><studio>(.*?)</studio><director>(.*?)</director><cast>(.*?)</cast><plot>(.*?)</plot><thumb>(.*?)</thumb>', xmlSource )
        if trailer:
            xbmc.log("[script.cinema.experience] - CE XML Match Found", xbmc.LOGNOTICE )
            for item in trailer:
                new_trailer += item
            return new_trailer[ 1 ], new_trailer[ 10 ], new_trailer[ 3 ], new_trailer[ 5 ], new_trailer[ 4 ], new_trailer[ 7 ], new_trailer[ 6 ], new_trailer[ 8 ]
        else:
            xbmc.log("[script.cinema.experience] - HD-Trailers.Net Downloader XML Match Found", xbmc.LOGNOTICE )
            title = "".join(re.compile("<title>(.*?)</title>", re.DOTALL).findall(xmlSource)) or ""
            plot = "".join(re.compile("<plot>(.*?)</plot>", re.DOTALL).findall(xmlSource)) or ""
            runtime = "".join(re.compile("<runtime>(.*?)</runtime>", re.DOTALL).findall(xmlSource)) or ""
            mpaa = "".join(re.compile("<mpaa>(.*?)</mpaa>", re.DOTALL).findall(xmlSource)) or ""
            release_date = "".join(re.compile("<premiered>(.*?)</premiered>", re.DOTALL).findall(xmlSource)) or ""
            studio = "".join(re.compile("<studio>(.*?)</studio>", re.DOTALL).findall(xmlSource)) or ""
            genre = "".join(re.compile("<genre>(.*?)</genre>", re.DOTALL).findall(xmlSource)) or ""
            director = "".join(re.compile("<director>(.*?)</director>", re.DOTALL).findall(xmlSource)) or ""
            return title, plot, runtime, mpaa, release_date, studio, genre, director


    def _set_trailer_info( self, trailer ):
        xbmc.log("[script.cinema.experience] - Setting Trailer Info", xbmc.LOGNOTICE )
        title = plot = runtime = mpaa = release_date = studio = genre = director = ""
        if os.path.isfile( os.path.splitext( trailer )[ 0 ] + ".nfo" ):
            xbmc.log("[script.cinema.experience] - Trailer .nfo file FOUND", xbmc.LOGNOTICE )
            title, plot, runtime, mpaa, release_date, studio, genre, director = self._getnfo( trailer )
        else:
            xbmc.log("[script.cinema.experience] - Trailer .nfo file NOT FOUND", xbmc.LOGNOTICE )
        result = ( xbmc.getCacheThumbName( trailer ), # id
                        title or os.path.basename( trailer ).split( "-trailer." )[ 0 ], # title
                        trailer, # trailer
                        self._get_thumbnail( trailer ), # thumb
                        plot, # plot
                        runtime, # runtime
                        mpaa, # mpaa
                        release_date, # release date
                        studio, # studio
                        genre, # genre
                        _L_( 32605 ), # writer
                        director, # director 32613
                        )
        return result

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
