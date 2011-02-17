# constants
__script__ = "Cinema Experience"
__author__ = "nuka1195-giftie-ackbarr"
__url__ = "http://code.google.com/p/xbmc-addons/"
__version__ = "1.0.16"
__XBMC_Revision__ = "34000"
__scriptID__ = "script.cinema.experience"

import xbmcgui, xbmc, xbmcaddon, os, re
import traceback 
import time         

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

def auto_refresh( before, mode ):
    xbmc.log( "[script.cinema.experience] - auto_refresh( %s, %s )" % ( before, mode ), xbmc.LOGNOTICE )
    # turn off autorefresh
    if _S_( "autorefresh" ) == "true" and before == "True" and mode=="disable":
        xbmc.executehttpapi( "SetGUISetting(1; videoplayer.adjustrefreshrate; False)" )
    # turn on autorefresh
    elif _S_( "autorefresh" ) == "true" and before == "True" and mode=="enable":
        xbmc.executehttpapi( "SetGUISetting(1; videoplayer.adjustrefreshrate; True)" )
    status = xbmc.executehttpapi( "GetGuiSetting(1; videoplayer.adjustrefreshrate)" ).strip("<li>")
    xbmc.log( "[script.cinema.experience] - Autorefresh Status: %s" % status, xbmc.LOGNOTICE )
    
def start_script( library_view = "movietitles" ):
    # turn off autorefresh
    autorefresh_movie = "False"
    auto_refresh( autorefresh, "disable" )
    xbmc.executebuiltin( "ActivateWindow(videolibrary,%s,return)" % library_view )
    # wait until Video Library shows
    while not xbmc.getCondVisibility( "Container.Content(movies)" ):
        pass
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, "Press 'Q' or '0' to Queue Movie(s)", 300000, image) )
    # wait until playlist is full to the required number of features
    xbmc.log( "[script.cinema.experience] - Waiting for queue to be filled with %s Feature films" % number_of_features, xbmc.LOGNOTICE )
    count = 0
    while xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() < ( number_of_features ):                
        if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > count:
            xbmc.log( "[script.cinema.experience] - User queued %s of %s Feature films" % (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), number_of_features), xbmc.LOGNOTICE )
            header1 = header + " - Feature " + "%d" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
            message = "Queued - " + xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() -1].getdescription()
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header1, message, time_delay, image) )
            count = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
            xbmc.sleep(time_delay*2)
        if not xbmc.getCondVisibility( "Container.Content(movies)" ):
            break
    xbmc.log( "[script.cinema.experience] - User queued %s Feature films" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), xbmc.LOGNOTICE )
    # If for some reason the limit does not get reached and the window changed, cancel script
    if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() < ( number_of_features ):
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, "Script Canceled", time_delay, image) )
        _clear_playlists()
    else:
        from resources.lib import xbmcscript_player as script
        script.Main()
        _clear_playlists( "music" )
        count = -1
        # prelim programming for adding - Activate script and other additions
        while xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() < ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1 ):
            if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition() > count:
                xbmc.sleep( 2000 )
                video_label = xbmc.executehttpapi( "GetVideoLabel(280)").strip("<li>")
                video_label2 = xbmc.executehttpapi( "GetVideoLabel(251)").strip("<li>")
                xbmc.log( "[script.cinema.experience] - video_label(280): %s" % video_label, xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] - video_label(251): %s" % video_label2, xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] - Playlist Position: %s  Playlist Size: %s " % ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition(), (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1) ), xbmc.LOGNOTICE )               
                if ( video_label == _L_( 32606 ) ):
                    if _S_( "autorefresh" ) == "true" and _S_( "autorefresh_movie" ) == "true":
                        auto_refresh( autorefresh, "enable" )
                        autorefresh_movie = "True"
                else:
                    if autorefresh_movie == "True":
                        auto_refresh( autorefresh, "disable" )
                        autorefresh_movie = "False"
                #xbmc.sleep( 5000 )
                xbmc.log( "[script.cinema.experience] - autorefresh_movie: %s" % autorefresh_movie, xbmc.LOGNOTICE )
                count = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition()                    
            #xbmc.sleep( 2000 )
        video_label = xbmc.executehttpapi( "GetVideoLabel(280)").strip("<li>")
        video_label2 = xbmc.executehttpapi( "GetVideoLabel(251)").strip("<li>")
        xbmc.log( "[script.cinema.experience] - Playlist Position: %s  Playlist Size: %s " % ( xbmc.PlayList(xbmc.PLAYLIST_VIDEO).getposition(), (xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() - 1) ), xbmc.LOGNOTICE )
        if (video_label not in headings):
            xbmc.log( "[script.cinema.experience] - video_label(280): %s" % video_label, xbmc.LOGNOTICE )
            xbmc.log( "[script.cinema.experience] - video_label(251): %s" % video_label2, xbmc.LOGNOTICE )
            #xbmc.Player().pause()
            if _S_( "autorefresh" ) == "true":
                auto_refresh( autorefresh, "enable" )
                autorefresh_movie == "True"
                xbmc.sleep( 300 )
                #xbmc.Player().play()
        else:
            xbmc.log( "[script.cinema.experience] - video_label(280): %s" % video_label, xbmc.LOGNOTICE )
            if autorefresh_movie == "True":
                auto_refresh( autorefresh, "disable" )
                autorefresh_movie == "False"   

if ( __name__ == "__main__" ):
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
                else:
                    _clear_playlists()
                    start_script( sys.argv[ 1 ].lower() )
            except:
                traceback.print_exc()       
    except:
        _clear_playlists()
        autorefresh_movie = "False"
        # only run if compatible
        if ( _check_compatible() ):
            start_script( "movietitles" )
    # turn on autorefresh if script turned it off
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % (header, "Script Exiting", time_delay, image) )
    _clear_playlists()
    if _S_( "autorefresh" ) == "true":
        auto_refresh( autorefresh, "enable" )
    #sys.modules.clear()