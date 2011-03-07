__script__ = "Cinema Experience"
__scriptID__ = "script.cinema.experience"
import sys
import os
import xbmcgui
import xbmc
import xbmcaddon
import traceback, threading

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting


# set proper message
message = 32520

#pDialog = xbmcgui.DialogProgress()
#pDialog.create( __script__, _L_( message )  )
#pDialog.update( 0 )

from urllib import quote_plus
from random import shuffle, random

BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
from download import download

downloaded_trailers = []

def _get_trailers( items, mpaa, genre, movie ):
    # return if not user preference
    if ( not items ):
        return []
    # trailer settings, grab them here so we don't need another _S_() object
    settings = { "trailer_amt_db_file":  xbmc.translatePath( _S_( "trailer_amt_db_file" ) ),
                      "trailer_folder":  xbmc.translatePath( _S_( "trailer_folder" ) ),
                      "trailer_rating": _S_( "trailer_rating" ),
                 "trailer_limit_query": _S_( "trailer_limit_query" ) == "true",
                   "trailer_play_mode": int( _S_( "trailer_play_mode" ) ),
                     "trailer_hd_only": _S_( "trailer_hd_only" ) == "true",
                     "trailer_quality": int( _S_( "trailer_quality" ) ),
              "trailer_unwatched_only": _S_( "trailer_unwatched_only" ) == "true",
                 "trailer_newest_only": _S_( "trailer_newest_only" ) == "true",
                       "trailer_count": ( 0, 1, 2, 3, 4, 5, 10, )[ int( _S_( "trailer_count" ) ) ],
                     "trailer_scraper": ( "amt_database", "amt_current", "local", )[ int( _S_( "trailer_scraper" ) ) ]
               }
    # get the correct scraper
    exec "from resources.scrapers.%s import scraper as scraper" % ( settings[ "trailer_scraper" ], )
    Scraper = scraper.Main( mpaa, genre, settings, movie )
    # fetch trailers
    trailers = Scraper.fetch_trailers()
    # return results
    return trailers
    
def downloader( mpaa, genre ):
    movie = ""
    xbmc.log( "[script.cinema.experience] - Starting Trailer Downloader", xbmc.LOGNOTICE )
    save_download_list( _download_trailers( mpaa, genre, movie ) )
    return
    
def save_download_list( download_trailers ):
    xbmc.log( "[script.cinema.experience] - Saving List of Downloaded Trailers", xbmc.LOGNOTICE )
    try:
        # base path to watched file
        base_path = os.path.join( BASE_CURRENT_SOURCE_PATH, "downloaded_trailers.txt" )
        # if the path to the source file does not exist create it
        if ( not os.path.isdir( os.path.dirname( base_path ) ) ):
            os.makedirs( os.path.dirname( base_path ) )
        # open source path for writing
        file_object = open( base_path, "w" )
        if download_trailers:
            for trailer in download_trailers:
                # write list
                file_object.write( repr( trailer[ 2 ] ) )
            # close file object
        else:
            file_object.write( "" )
        file_object.close()
    except:
        traceback.print_exc()

        
def _download_trailers( mpaa, genre, movie ):
    updated_trailers = []
    xbmc.log( "[script.cinema.experience] - Downloading Trailers: %s Trailers" % ( 0, 1, 2, 3, 4, 5, 10, )[ int( _S_( "trailer_count" ) ) ], xbmc.LOGNOTICE )
    trailers = _get_trailers(  items=( 0, 1, 2, 3, 4, 5, 10, )[ int( _S_( "trailer_count" ) ) ],
                                mpaa=mpaa,
                               genre=genre,
                               movie=movie
                            )
    for trailer in trailers:
        updated_trailer={}
        xbmc.log( "[script.cinema.experience] - Attempting To Download Trailer: %s" % trailer[ 1 ], xbmc.LOGNOTICE )
        filename, ext = os.path.splitext( os.path.basename( (trailer[ 2 ].split("|")[0] ).replace( "?","" ) ) )
        filename = filename + "-trailer" + ext
        file_path = os.path.join( _S_( "trailer_download_folder" ), filename ).replace( "\\\\", "\\" )
        # check to see if trailer is already downloaded
        if os.path.isfile( file_path ): 
            success = True
            destination = file_path
        else:
            success, destination = download( trailer[ 2 ], _S_( "trailer_download_folder" ), file_tag="-trailer" )
        if success:
            xbmc.log( "[script.cinema.experience] - Downloaded Trailer: %s" % trailer[ 1 ], xbmc.LOGNOTICE )
            updated_trailer[ 0 ] = trailer[ 0 ]
            updated_trailer[ 1 ] = trailer[ 1 ]
            updated_trailer[ 2 ] = destination
            updated_trailer[ 3 ] = trailer[ 3 ]
            updated_trailer[ 4 ] = trailer[ 4 ]
            updated_trailer[ 5 ] = trailer[ 5 ]
            updated_trailer[ 6 ] = trailer[ 6 ]
            updated_trailer[ 7 ] = trailer[ 7 ]
            updated_trailer[ 8 ] = trailer[ 8 ]
            updated_trailer[ 9 ] = trailer[ 9 ]
            updated_trailer[ 10 ] = trailer[ 10 ]
            updated_trailer[ 11 ] = trailer[ 11 ]
            _create_nfo_file( updated_trailer, destination )
        else:
            xbmc.log( "[script.cinema.experience] - Failed to Download Trailer: %s" % trailer[ 1 ], xbmc.LOGNOTICE )
            updated_trailer=[]
        updated_trailers += [ updated_trailer ]
    return updated_trailers
    
def _create_nfo_file( trailer, trailer_nfopath ):
    '''
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
    xbmc.log( "[script.cinema.experience] - Creating Trailer NFO file", xbmc.LOGNOTICE )
    # set quality, we do this since not all resolutions have trailers
    quality = ( "Standard", "480p", "720p", "1080p" )[ int( _S_( "trailer_quality" ) ) ]
    # set movie info
    nfoSource = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<movieinfo id="%s">
    <title>%s</title>
    <quality>%s</quality>
    <runtime>%s</runtime>
    <releasedate>%s</releasedate>
    <mpaa>%s</mpaa>
    <genre>%s</genre>
    <studio>%s</studio>
    <director>%s</director>
    <cast>%s</cast>
    <plot>%s</plot>
    <thumb>%s</thumb>
</movieinfo>
""" % ( trailer[ 0 ], trailer[ 1 ], quality, trailer[ 5 ], trailer[ 7 ], trailer[ 6 ], trailer[ 9 ], trailer[ 8 ], trailer[ 11 ], "", trailer[ 4 ], trailer[ 3 ] )
    # save nfo file
    return _save_nfo_file( nfoSource, trailer_nfopath )

def _save_nfo_file( nfoSource, trailer_nfopath ):
    xbmc.log( "[script.cinema.experience] - Saving Trailer NFO file", xbmc.LOGNOTICE )
    destination = os.path.splitext( trailer_nfopath )[0] + ".nfo"
    try:
        # open source path for writing
        file_object = open( destination.encode( "utf-8" ), "w" )
        # write xmlSource
        file_object.write( nfoSource.encode( "utf-8" ) )
        # close file object
        file_object.close()
        # return successful
        return True
    except Exception, e:
        # oops, notify user what error occurred
        xbmc.log( "[script.cinema.experience] - %s" % str( e ), xbmc.LOGERROR )
        # return failed
        return False