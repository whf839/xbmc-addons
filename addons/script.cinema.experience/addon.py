# constants
__script__ = "Cinema Experience"
__author__ = "nuka1195-giftie-ackbarr"
__url__ = "http://code.google.com/p/xbmc-addons/"
__version__ = "1.0.32"
__scriptID__ = "script.cinema.experience"

import xbmcgui, xbmc, xbmcaddon, os, re
import traceback 
import time
from urllib import quote_plus       

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting


number_of_features = int( _S_( "number_of_features" ) ) + 1
playback = ""
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
headings = ( _L_(32600), _L_(32601), _L_(32602), _L_(32603), _L_(32604), _L_(32605), _L_(32606), _L_(32607), _L_(32608), _L_(32609), _L_(32610), _L_(32611), _L_(32612) )
header = "Cinema Experience"
time_delay = 200
image = xbmc.translatePath( os.path.join( _A_.getAddonInfo("path"), "icon.png") )
autorefresh = xbmc.executehttpapi( "GetGuiSetting(1; videoplayer.adjustrefreshrate)" ).strip("<li>")


def footprints():
    xbmc.log( "[script.cinema.experience] - Script Name: %s" % __script__, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Script ID: %s" % __scriptID__, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Script Version: %s" % __version__, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Autorefresh - Before Script: %s" % autorefresh, xbmc.LOGNOTICE )

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
        #video_tag = xbmc.InfoTagVideo()
        from resources.lib import xbmcscript_player as script
        script.Main()
        _clear_playlists( "music" )
        count = -1
        # prelim programming for adding - Activate script and other additions
        while xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() < ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1 ):
            if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() > count:
                xbmc.sleep( 2000 )
                #movie_title = video_tag.getTitle()
                #movie_writer = video_tag.getWritingCredits()
                #movie_genre = video_tag.getGenre()
                #xbmc.log( "[script.cinema.experience] - movie_title: %s" % movie_title, xbmc.LOGNOTICE )
                #xbmc.log( "[script.cinema.experience] - movie_writer: %s" % movie_writer, xbmc.LOGNOTICE )
                #xbmc.log( "[script.cinema.experience] - movie_genre: %s" % movie_genre, xbmc.LOGNOTICE )
                #xbmc.log( "[script.cinema.experience] - movie_next: %s" % movie_next, xbmc.LOGNOTICE )
                if movie_next:
                    try:
                        movie_title = xbmc.executehttpapi( "GetVideoLabel(250)").strip("<li>")
                        xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie_title, xbmc.LOGNOTICE )
                    except:
                        movie_title = repr( xbmc.executehttpapi( "GetVideoLabel(250)").strip("<li>") )
                        xbmc.log( "[script.cinema.experience] - Movie Title: %s" % movie_title, xbmc.LOGNOTICE )
                    movie_next= False
                try:
                    video_label = ( xbmc.executehttpapi( "GetVideoLabel(280)").strip("<li>") )
                    video_label2 = ( xbmc.executehttpapi( "GetVideoLabel(251)").strip("<li>") ) 
                except:
                    video_label = ( repr( xbmc.executehttpapi( "GetVideoLabel(280)").strip("<li>") ) ).strip("'")
                    video_label2 = (repr( xbmc.executehttpapi( "GetVideoLabel(251)").strip("<li>") ) ).strip("'")
                xbmc.log( "[script.cinema.experience] - video_label(280): %s" % video_label, xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] - video_label(251): %s" % video_label2, xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] - Playlist Position: %s  Playlist Size: %s " % ( ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() + 1 ), (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() ) ), xbmc.LOGNOTICE )               
                if ( video_label == _L_( 32606 ) ):
                    movie_next = True
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
            video_label = xbmc.executehttpapi( "GetVideoLabel(280)").strip("<li>")
            video_label2 = xbmc.executehttpapi( "GetVideoLabel(251)").strip("<li>")
            xbmc.log( "[script.cinema.experience] - Playlist Position: %s  Playlist Size: %s " % ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition(), (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1) ), xbmc.LOGNOTICE )
            if (video_label not in headings):
                xbmc.log( "[script.cinema.experience] - video_label(280): %s" % video_label, xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] - video_label(251): %s" % video_label2, xbmc.LOGNOTICE )
                #xbmc.Player().pause()
                if _S_( "autorefresh" ) == "true":
                    auto_refresh( autorefresh, "enable" )
                    autorefresh_movie == True
                    xbmc.sleep( 300 )
                    #xbmc.Player().play()
            else:
                xbmc.log( "[script.cinema.experience] - video_label(280): %s" % video_label, xbmc.LOGNOTICE )
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