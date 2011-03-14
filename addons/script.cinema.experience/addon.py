# constants
__script__ = "Cinema Experience"
__author__ = "nuka1195-giftie-ackbarr"
__url__ = "http://code.google.com/p/xbmc-addons/"
__version__ = "1.0.38"
__scriptID__ = "script.cinema.experience"

import xbmcgui, xbmc, xbmcaddon, os, re, sys
import traceback
import time
from urllib import quote_plus
from threading import Thread

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting


number_of_features = int( _S_( "number_of_features" ) ) + 1
playback = ""
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
headings = ( _L_(32600), _L_(32601), _L_(32602), _L_(32603), _L_(32604), _L_(32605), _L_(32606), _L_(32607), _L_(32608), _L_(32609), _L_(32610), _L_(32611), _L_(32612) )
header = "Cinema Experience"
time_delay = 200
image = xbmc.translatePath( os.path.join( _A_.getAddonInfo("path"), "icon.png") )
autorefresh = xbmc.executehttpapi( "GetGuiSetting(1; videoplayer.adjustrefreshrate)" ).strip("<li>")
playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )

from ce_playlist import _get_special_items, _wait_until_end, _get_queued_video_info, build_music_playlist
from slides import _fetch_slides
from trailer_downloader import downloader

def footprints():
    xbmc.log( "[script.cinema.experience] - Script Name: %s" % __script__, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Script ID: %s" % __scriptID__, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Script Version: %s" % __version__, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Autorefresh - Before Script: %s" % autorefresh, xbmc.LOGNOTICE )

def _load_trigger_list():
    xbmc.log( "[script.cinema.experience] - Loading Trigger List", xbmc.LOGNOTICE)
    try:
        # set base watched file path
        base_path = os.path.join( BASE_CURRENT_SOURCE_PATH, "trigger_list.txt" )
        # open path
        usock = open( base_path, "r" )
        # read source
        trigger_list = eval( usock.read() )
        # close socket
        usock.close()
    except:
        xbmc.log( "[script.cinema.experience] - Loading Trigger List", xbmc.LOGNOTICE)
        traceback.print_exc()
        trigger_list = []
    return trigger_list
            
def _clear_watched_items( clear_type ):
    xbmc.log( "[script.cinema.experience] - _clear_watched_items( %s )" % ( clear_type ), xbmc.LOGNOTICE )
    # initialize base_path
    base_paths = []
    # clear trivia or trailers
    if ( clear_type == "ClearWatchedTrailers" ):
        # trailer settings, grab them here so we don't need another _S_() object
        settings = { "trailer_amt_db_file":  xbmc.translatePath( _S_( "trailer_amt_db_file" ) ) }
        # handle AMT db special
        from resources.scrapers.amt_database import scraper as scraper
        Scraper = scraper.Main( settings=settings )
        # update trailers
        Scraper.clear_watched()
        # set base watched file path
        base_paths += [ os.path.join( BASE_CURRENT_SOURCE_PATH, "amt_current_watched.txt" ) ]
        base_paths += [ os.path.join( BASE_CURRENT_SOURCE_PATH, "local_watched.txt" ) ]
    else:
        # set base watched file path
        base_paths = [ os.path.join( BASE_CURRENT_SOURCE_PATH, "trivia_watched.txt" ) ]
    try:
        # set proper message
        message = ( 32531, 32541, )[ sys.argv[ 1 ] == "ClearWatchedTrailers" ]
        # remove watched status file(s)
        for base_path in base_paths:
            # remove file if it exists
            if ( os.path.isfile( base_path ) ):
                os.remove( base_path )
    except:
        # set proper message
        message = ( 32532, 32542, )[ sys.argv[ 1 ] == "ClearWatchedTrailers" ]
    # inform user of result
    ok = xbmcgui.Dialog().ok( _L_( 32000 ), _L_( message ) )

def _view_changelog( ):
    xbmc.log( "[script.cinema.experience] - _view_changelog()", xbmc.LOGNOTICE )

def _view_readme( ):
    xbmc.log( "[script.cinema.experience] - _view_readme()", xbmc.LOGNOTICE )

def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[script.cinema.experience] - Version - %s-r%s' initialized!" % ( __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ][ : 5 ] )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
    # spam revision info
    xbmc.log( "[script.cinema.experience] -     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] -     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), xbmc.LOGNOTICE )
    return ok

def _clear_playlists( mode="both" ):
    # clear playlists
    if mode=="video" or mode=="both":
        vplaylist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        vplaylist.clear()
        xbmc.log( "[script.cinema.experience] - Video Playlist Cleared", xbmc.LOGNOTICE )
    if mode=="music" or mode=="both":
        mplaylist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        mplaylist.clear()
        xbmc.log( "[script.cinema.experience] - Music Playlist Cleared", xbmc.LOGNOTICE )

def log_settings():
    xbmc.log( "[script.cinema.experience] - ", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Trivia Settings", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_total_time: %s" % _S_( "trivia_total_time" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_folder: %s" % _S_( "trivia_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_slide_time: %s" % _S_( "trivia_slide_time" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_limit_query: %s" % _S_( "trivia_limit_query" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_rating: %s" % _S_( "trivia_rating" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_intro: %s" % _S_( "trivia_intro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_intro_file: %s" % _S_( "trivia_intro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_intro_folder: %s" % _S_( "trivia_intro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_outro: %s" % _S_( "trivia_outro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_outro_file: %s" % _S_( "trivia_outro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_outro_folder: %s" % _S_( "trivia_outro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_music: %s" % _S_( "trivia_music" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_music_file: %s" % _S_( "trivia_music_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_music_folder: %s" % _S_( "trivia_music_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_adjust_volume: %s" % _S_( "trivia_adjust_volume" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_music_volume: %s" % _S_( "trivia_music_volume" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_fade_volume: %s" % _S_( "trivia_fade_volume" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_fade_time: %s" % _S_( "trivia_fade_time" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trivia_unwatched_only: %s" % _S_( "trivia_unwatched_only" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - ", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Special Video Settings", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - mte_intro: %s" % _S_( "mte_intro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - mte_intro_file: %s" % _S_( "mte_intro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - mte_intro_folder: %s" % _S_( "mte_intro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - mte_outro: %s" % _S_( "mte_outro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - mte_outro_file: %s" % _S_( "mte_outro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - mte_outro_folder: %s" % _S_( "mte_outro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - fpv_intro: %s" % _S_( "fpv_intro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - fpv_intro_file: %s" % _S_( "fpv_intro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - fpv_intro_folder: %s" % _S_( "fpv_intro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - fpv_outro: %s" % _S_( "fpv_outro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - fpv_outro_file: %s" % _S_( "fpv_outro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - fpv_outro_folder: %s" % _S_( "fpv_outro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - enable_ratings: %s" % _S_( "enable_ratings" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - rating_videos_folder: %s" % _S_( "rating_videos_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - enable_audio: %s" % _S_( "enable_audio" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - audio_videos_folder: %s" % _S_( "audio_videos_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - countdown_video: %s" % _S_( "countdown_video" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - countdown_video_file: %s" % _S_( "countdown_video_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - countdown_video_folder: %s" % _S_( "countdown_video_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - ", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Trailer Settings", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_count: %s" % _S_( "trailer_count" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - cav_intro: %s" % _S_( "cav_intro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - cav_intro_file: %s" % _S_( "cav_intro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - cav_intro_folder: %s" % _S_( "cav_intro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - cav_outro: %s" % _S_( "cav_outro" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - cav_outro_file: %s" % _S_( "cav_outro_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - cav_outro_folder: %s" % _S_( "cav_outro_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_play_mode: %s" % _S_( "trailer_play_mode" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_scraper: %s" % _S_( "trailer_scraper" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_folder: %s" % _S_( "trailer_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_amt_db_file: %s" % _S_( "trailer_amt_db_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_newest_only: %s" % _S_( "trailer_newest_only" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_quality: %s" % _S_( "trailer_quality" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_hd_only: %s" % _S_( "trailer_hd_only" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_limit_query: %s" % _S_( "trailer_limit_query" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_rating: %s" % _S_( "trailer_rating" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - trailer_unwatched_only: %s" % _S_( "trailer_unwatched_only" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - ", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Feature Presentation Settings", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - number_of_features: %s" % _S_( "number_of_features" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - intermission_video: %s" % _S_( "intermission_video" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - intermission_video_file: %s" % _S_( "intermission_video_file" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - intermission_video_folder: %s" % _S_( "intermission_video_folder" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - intermission_audio: %s" % _S_( "intermission_audio" ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - ", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Misc Settings", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - autorefresh: %s" % _S_( "autorefresh" ), xbmc.LOGNOTICE )

def _build_playlist( movie_titles ):
    for movie in movie_titles:
        xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie, xbmc.LOGNOTICE )
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
        # select Movie path from movieview Limit 1
        sql = "SELECT movieview.c16, movieview.strPath, movieview.strFileName FROM movieview WHERE c00 LIKE '%s' LIMIT 1" % ( movie.replace( "'", "''", ), )
        xbmc.log( "[script.cinema.experience]  - SQL: %s" % ( sql, ), xbmc.LOGNOTICE )
        # query database for info dummy is needed as there are two </field> formatters
        try:
            movie_title, movie_path, movie_filename, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
        except:
            movie_title, movie_path, movie_filename, dummy = ""
        movie_full_path = os.path.join(movie_path, movie_filename).replace("\\\\" , "\\")
        xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie_title, xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Movie Path: %s" % movie_path, xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Movie Filename: %s" % movie_filename, xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Full Movie Path: %s" % movie_full_path, xbmc.LOGNOTICE )
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        listitem = xbmcgui.ListItem(movie_title, )
        listitem.setInfo('video', {'Title': movie_title,})
        playlist.add(url=movie_full_path, listitem=listitem, )
        xbmc.sleep( 150 )

def _store_playlist():
    p_list = []
    voxcommando()
    try:
        xbmc.log( "[script.cinema.experience] - Storing Playlist", xbmc.LOGNOTICE )
        true = True
        false = False
        null = None
        json_query = '{"jsonrpc": "2.0", "method": "VideoPlaylist.GetItems", "id": 1}'
        json_response = xbmc.executeJSONRPC(json_query)
        response = json_response
        if ( response.startswith( "{" ) ):
            response = eval( response )
        result = response['result']
        p_list = result['items']
    except:
        xbmc.log( "[script.cinema.experience] - Error - Playlist Empty", xbmc.LOGNOTICE )
    return p_list

def voxcommando():
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlistsize = playlist.size()
    if playlistsize > 1:
        movie_titles = ""
        for feature_count in range (1, playlistsize + 1):
            movie_title = playlist[ feature_count - 1 ].getdescription()
            xbmc.log( "[script.cinema.experience] - Feature #%-2d - %s" % ( feature_count, movie_title ), xbmc.LOGNOTICE )
            movie_titles = movie_titles + movie_title + "<li>"
        movie_titles = movie_titles.rstrip("<li>")
        if _S_( "voxcommando" ) == "true":
            xbmc.executehttpapi( "Broadcast(<b>CElaunch." + str(playlistsize ) + "<li>" + movie_titles + "</b>;33000)" )
    else:
        # get the queued video info
        movie_title = playlist[ 0 ].getdescription()
        xbmc.log( "[script.cinema.experience] - Feature - %s" % movie_title, xbmc.LOGNOTICE )
        if _S_( "voxcommando" ) == "true":
            xbmc.executehttpapi( "Broadcast(<b>CElaunch<li>" + movie_title + "</b>;33000)" )

def _sqlquery( sqlquery ):
    movie_list = []
    movies = []
    xbmc.executehttpapi( "SetResponseFormat()" )
    xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
    #sqlquery = "SELECT movieview.c00 FROM movieview JOIN genrelinkmovie ON genrelinkmovie.idMovie=movieview.idMovie JOIN genre ON genrelinkmovie.idGenre=genre.idGenre WHERE strGenre='Action' ORDER BY RANDOM() LIMIT 4"
    xbmc.log( "[script.cinema.experience]  - SQL: %s" % ( sqlquery, ), xbmc.LOGNOTICE )
    try:
        sqlresult = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sqlquery ), )
        xbmc.log( "[script.cinema.experience] - sqlresult: %s" % sqlresult, xbmc.LOGNOTICE )
        movies = sqlresult.split("</field>")
        movie_list = movies[ 0:len( movies ) -1 ]
    except:
        xbmc.log( "[script.cinema.experience] - Error searching database", xbmc.LOGNOTICE )
    return movie_list

def auto_refresh( before, mode ):
    xbmc.log( "[script.cinema.experience] - auto_refresh( %s, %s )" % ( before, mode ), xbmc.LOGNOTICE )
    # turn off autorefresh
    if _S_( "autorefresh" ) == "true" and before and mode=="disable":
        xbmc.executehttpapi( "SetGUISetting(1; videoplayer.adjustrefreshrate; False)" )
    # turn on autorefresh
    elif _S_( "autorefresh" ) == "true" and before and mode=="enable":
        xbmc.executehttpapi( "SetGUISetting(1; videoplayer.adjustrefreshrate; True)" )
    status = xbmc.executehttpapi( "GetGuiSetting(1; videoplayer.adjustrefreshrate)" ).strip("<li>")
    xbmc.log( "[script.cinema.experience] - Autorefresh Status: %s" % status, xbmc.LOGNOTICE )

def _play_trivia( mpaa, genre, plist ):
    # if trivia path and time to play the trivia slides
    pDialog = xbmcgui.DialogProgress()
    pDialog.create( __script__, _L_( 32520 )  )
    pDialog.update( 0 )
    if ( int( _S_( "trailer_play_mode" ) ) == 1 ):
        xbmc.log( "[script.cinema.experience] - Starting Downloader Tread", xbmc.LOGNOTICE )
        #downloaded_trailers = downloader( mpaa, genre )
        thread = Thread( target=downloader, args=( mpaa, genre ) )
        thread.start()
    if ( _S_( "trivia_folder" ) and int( float( _S_( "trivia_total_time" ) ) ) > 0 ):
        ## update dialog with new message
        #pDialog.update( -1, _L_( 32510 ) )
        # initialize intro/outro lists
        playlist_intro = []
        play_list = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        play_list.clear()
        # get trivia intro videos
        _get_special_items( playlist=play_list,
                               items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_intro" ) ) ],
                                path=( xbmc.translatePath( _S_( "trivia_intro_file" ) ), xbmc.translatePath( _S_( "trivia_intro_folder" ) ), )[ int( _S_( "trivia_intro" ) ) > 1 ],
                               genre=_L_( 32609 ),
                               index=0
                          )

        # trivia settings, grab them here so we don't need another _S_() object
        settings = {  "trivia_total_time": int( float( _S_( "trivia_total_time" ) ) ),
                          "trivia_folder": xbmc.translatePath( _S_( "trivia_folder" ) ),
                      "trivia_slide_time": int( float( _S_( "trivia_slide_time" ) ) ),
                           "trivia_intro": _S_( "trivia_intro" ),
                  "trivia_intro_playlist": playlist_intro,
                           "trivia_music": _S_( "trivia_music" ),
                   "trivia_adjust_volume": _S_( "trivia_adjust_volume" ),
                     "trivia_fade_volume": _S_( "trivia_fade_volume" ),
                       "trivia_fade_time": int( float( _S_( "trivia_fade_time" ) ) ),
                      "trivia_music_file": xbmc.translatePath( _S_( "trivia_music_file" ) ),
                    "trivia_music_folder": xbmc.translatePath( _S_( "trivia_music_folder" ) ),
                    "trivia_music_volume": int( float( _S_( "trivia_music_volume" ) ) ),
                  "trivia_unwatched_only": _S_( "trivia_unwatched_only" ) == "true"
                            }

        if ( int(_S_( "trivia_music" ) ) > 0):
            pDialog.update( -1, _L_( 32511 )  )
            build_music_playlist()
        xbmc.log( "[script.cinema.experience] - ## Intro ##", xbmc.LOGNOTICE)
        # set the proper mpaa rating user preference
        mpaa = (  _S_( "trivia_rating" ), mpaa, )[ _S_( "trivia_limit_query" ) == "true" ]
        xbmc.log( "[script.cinema.experience] - Slide MPAA Rating: %s" % mpaa, xbmc.LOGNOTICE )
        # import trivia module and execute the gui
        pDialog.update( 50 )
        slide_playlist = _fetch_slides( mpaa )
        pDialog.close()
        if not int( _S_( "trivia_intro" ) ) == 0:
            xbmc.Player().play( play_list )
            _wait_until_end()
        from xbmcscript_trivia import Trivia
        xbmc.log( "[script.cinema.experience] - Starting Trivia script", xbmc.LOGNOTICE )
        ui = Trivia( "script-CExperience-trivia.xml", _A_.getAddonInfo('path'), "default", "720p", settings=settings, mpaa=mpaa, genre=genre, plist=plist, slide_playlist=slide_playlist )
        #ui.doModal()
        del ui
        # we need to activate the video window
        xbmc.executebuiltin( "XBMC.ActivateWindow(2005)" )
    else:
        # no trivia slide show so play the video
        pDialog.close()
        # play the video playlist
        import xbmcscript_player as script
        script.Main()
        xbmc.Player().play( xbmc.PlayList(xbmc.PLAYLIST_VIDEO) )
    
def start_script( library_view = "oldway" ):
    messy_exit = False
    xbmc.log( "[script.cinema.experience] - Library_view: %s" % library_view, xbmc.LOGNOTICE )
    # turn off autorefresh
    early_exit = False
    autorefresh_movie = False
    movie_next = False
    auto_refresh( autorefresh, "disable" )
    if library_view != "oldway":
        xbmc.executebuiltin( "ActivateWindow(videolibrary,%s,return)" % library_view )
        # wait until Video Library shows
        while not xbmc.getCondVisibility( "Container.Content(movies)" ):
            pass
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32546 ), 300000, image) )
        # wait until playlist is full to the required number of features
        xbmc.log( "[script.cinema.experience] - Waiting for queue to be filled with %s Feature films" % number_of_features, xbmc.LOGNOTICE )
        count = 0
        while xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() < ( number_of_features ):
            if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > count:
                xbmc.log( "[script.cinema.experience] - User queued %s of %s Feature films" % (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), number_of_features), xbmc.LOGNOTICE )
                header1 = header + " - Feature " + "%d" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                message = _L_( 32543 ) + xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() -1].getdescription()
                xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header1, message, time_delay, image) )
                count = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.sleep(time_delay*2)
            if not xbmc.getCondVisibility( "Container.Content(movies)" ):
                early_exit = True
                break
        xbmc.log( "[script.cinema.experience] - User queued %s Feature films" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), xbmc.LOGNOTICE )
        if not early_exit:
            header1 = header + " - Feature " + "%d" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
            message = _L_( 32543 ) + xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() -1].getdescription()
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header1, message, time_delay, image) )
            early_exit = False
        # If for some reason the limit does not get reached and the window changed, cancel script
    if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() < ( number_of_features ) and library_view != "oldway":
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32544 ), time_delay, image) )
        _clear_playlists()
    else:
        mpaa, audio, genre, movie, equivalent_mpaa = _get_queued_video_info( 0 )
        plist = _store_playlist() # need to store movie playlist
        _play_trivia( equivalent_mpaa, genre, plist )
        _clear_playlists( "music" )
        trigger_list = _load_trigger_list()
        count = -1
        # prelim programming for adding - Activate script and other additions
        while xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() < ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1 ):
            if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() > count:
                try:
                    xbmc.log( "[script.cinema.experience] - Item From Trigger List: %s" % trigger_list[ xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() ], xbmc.LOGNOTICE )
                except:
                    xbmc.log( "[script.cinema.experience] - Problem With Trigger List", xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] - Playlist Position: %s  Playlist Size: %s " % ( ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() + 1 ), (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() ) ), xbmc.LOGNOTICE )
                if trigger_list[ xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() + 1] == "Movie":
                    if _S_( "autorefresh" ) == "true" and _S_( "autorefresh_movie" ) == "true":
                        auto_refresh( autorefresh, "enable" )
                        autorefresh_movie = True
                else:
                    if autorefresh_movie:
                        auto_refresh( autorefresh, "disable" )
                        autorefresh_movie = False
                #xbmc.sleep( 5000 )
                xbmc.log( "[script.cinema.experience] - autorefresh_movie: %s" % autorefresh_movie, xbmc.LOGNOTICE )
                count = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition()
            #xbmc.sleep( 2000 )
        if not xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() < 1: # To catch an already running script when a new instance started
            try:
                xbmc.log( "[script.cinema.experience] - Item From Trigger List: %s" % trigger_list[ xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() ], xbmc.LOGNOTICE )
            except:
                xbmc.log( "[script.cinema.experience] - Problem With Trigger List", xbmc.LOGNOTICE )
            xbmc.log( "[script.cinema.experience] - Playlist Position: %s  Playlist Size: %s " % ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition(), (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1) ), xbmc.LOGNOTICE )
            if ( trigger_list[ xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() ] not in headings):
                xbmc.log( "[script.cinema.experience] - Item From Trigger List: %s" % trigger_list[ xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() ], xbmc.LOGNOTICE )
                #xbmc.Player().pause()
                if _S_( "autorefresh" ) == "true":
                    auto_refresh( autorefresh, "enable" )
                    autorefresh_movie == True
                    xbmc.sleep( 300 )
                    #xbmc.Player().play()
            else:
                xbmc.log( "[script.cinema.experience] - Item From Trigger List: %s" % trigger_list[ xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() ], xbmc.LOGNOTICE )
                if autorefresh_movie:
                    auto_refresh( autorefresh, "disable" )
                    autorefresh_movie == False
            messy_exit = False
        else:
            xbmc.log( "[script.cinema.experience] - Playlist Size: %s   User must have restarted script after pressing stop" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), xbmc.LOGNOTICE )
            xbmc.log( "[script.cinema.experience] - Stopping Script", xbmc.LOGNOTICE )
            messy_exit = True
    return messy_exit

if ( __name__ == "__main__" ):
    footprints()
    # check to see if an argv has been passed to script
    if ( int(xbmc.executehttpapi( "GetLogLevel" ).replace( "<li>", "" ) ) > 1 ):
        log_settings()
    # check to see if an argv has been passed to script
    try:
        if ( sys.argv[ 1 ] ):
            xbmc.log( "[script.cinema.experience] - Script Started With: %s" % sys.argv[ 1 ], xbmc.LOGNOTICE )
            try:
                if ( sys.argv[ 1 ] == "ClearWatchedTrivia" or sys.argv[ 1 ] == "ClearWatchedTrailers" ):
                    _clear_watched_items( sys.argv[ 1 ] )
                elif ( sys.argv[ 1 ] == "ViewChangelog" ):
                    _view_changelog()
                elif ( sys.argv[ 1 ] == "ViewReadme" ):
                    _view_readme()
                elif ( sys.argv[ 1 ] == "oldway" ):
                    _A_.setSetting( id='number_of_features', value='0' ) # set number of features to 1
                    _clear_playlists()
                    xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
                    xbmc.log( "[script.cinema.experience] - Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), xbmc.LOGNOTICE )
                    # we need to sleep so the video gets queued properly
                    xbmc.sleep( 500 )
                    autorefresh_movie = False
                    exit = start_script( "oldway" )
                elif ( sys.argv[ 1 ].startswith( "command" ) ):   # Command Arguments
                    sys_argv = sys.argv[ 1 ].replace("<li>",";")
                    command = re.split(";", sys_argv, maxsplit=1)[1]
                    xbmc.log( "[script.cinema.experience] - Command Call: %s" % command, xbmc.LOGNOTICE )
                    if command.startswith( "movie_title" ):   # Movie Title
                        _clear_playlists()
                        if command.startswith( "movie_title;" ):
                            titles = re.split(";", command, maxsplit=1)[1]
                        elif command.startswith( "movie_title=" ):
                            titles = re.split("=", command, maxsplit=1)[1]
                        movie_titles = titles.split( ";" )
                        if not movie_titles == "":
                            _build_playlist( movie_titles )
                            autorefresh_movie = False
                            exit = start_script( "oldway" )
                        else:
                            exit = False
                    elif command.startswith( "sqlquery" ):    # SQL Query
                        _clear_playlists()
                        sqlquery = re.split(";", command, maxsplit=1)[1]
                        movie_titles = _sqlquery( sqlquery )
                        if not movie_titles == "":
                            _build_playlist( movie_titles )
                            autorefresh_movie = False
                            exit = start_script( "oldway" )
                        else:
                            exit = False
                    elif command.startswith( "open_settings" ):    # Open Settings
                        _A_.openSettings()
                        exit = False
                else:
                    _clear_playlists()
                    exit = start_script( sys.argv[ 1 ].lower() )
            except:
                traceback.print_exc()
    except:
        #start script in 'Old Way' if the script is called with out argv... queue the movie the old way
        _A_.setSetting( id='number_of_features', value='0' ) # set number of features to 1
        _clear_playlists()
        xbmc.executebuiltin( "Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ) )
        xbmc.log( "[script.cinema.experience] - Action(Queue,%d)" % ( xbmcgui.getCurrentWindowId() - 10000, ), xbmc.LOGNOTICE )
        # we need to sleep so the video gets queued properly
        xbmc.sleep( 500 )
        autorefresh_movie = False
        start_script( "oldway" )
    # turn on autorefresh if script turned it off
    #xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, _L_( 32545 ), time_delay, image) )
    xbmc.log( "[script.cinema.experience] - messy_exit: %s" % exit, xbmc.LOGNOTICE )
    if exit:
        pass
    else:
        _clear_playlists()
        if _S_( "autorefresh" ) == "true":
            auto_refresh( autorefresh, "enable" )
    _A_.setSetting( id='number_of_features', value='%d' % (number_of_features - 1) )
    #sys.modules.clear()
