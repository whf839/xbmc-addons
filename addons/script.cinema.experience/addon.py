# constants
__script__ = "Cinema Experience"
__author__ = "nuka1195-giftie-ackbarr"
__url__ = "http://code.google.com/p/xbmc-addons/"
__version__ = "1.0.9"
__XBMC_Revision__ = "34000"
__scriptID__ = "script.cinema.experience"

import xbmcgui, xbmc, xbmcaddon, os
import traceback          

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting  

BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )

def _clear_watched_items( clear_type ):
    xbmc.log( "[script.cinemaexperience] - _clear_watched_items( %s )" % ( clear_type ), xbmc.LOGNOTICE )
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
    xbmc.log( "[script.cinemaexperience] - _view_changelog()", xbmc.LOGNOTICE )

def _view_readme( ):
    xbmc.log( "[script.cinemaexperience] - _view_readme()", xbmc.LOGNOTICE )

def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[script.cinemaexperience]: Version - %s-r%s' initialized!" % ( __version__, __svn_revision__.replace( "$", "" ).replace( "Revision", "" ).replace( ":", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_rev = int( xbmc.getInfoLabel( "System.BuildVersion" ).split( " r" )[ -1 ][ : 5 ] )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so unknown, allow to run
        xbmc_rev = 0
        ok = 2
    # spam revision info
    xbmc.log( "[script.cinemaexperience] -     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinemaexperience] -     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", "Unknown", )[ ok ], ), xbmc.LOGNOTICE )
    # TODO: maybe remove this notification
    # if not compatible, inform user
    if ( not ok ):
        import xbmcgui
        import os
        # get localized strings
        _ = xbmc.getLocalizedString
        # inform user
        #xbmcgui.Dialog().ok( "%s - %s: %s" % ( __script__, _L_( 32700 ), __version__, ), _L_( 32701 ) % ( __script__, ), _L_( 32702 ) % ( __XBMC_Revision__, ), _L_( 32703 ) )
    #return result
    return ok


if ( __name__ == "__main__" ):
    # only run if compatible
    try:
        if ( sys.argv[ 1 ] ):
            try:
                if ( sys.argv[ 1 ] == "ClearWatchedTrivia" or sys.argv[ 1 ] == "ClearWatchedTrailers" ):
                    _clear_watched_items( sys.argv[ 1 ] )
                elif ( sys.argv[ 1 ] == "ViewChangelog" ):
                    _view_changelog()
                elif ( sys.argv[ 1 ] == "ViewReadme" ):
                    _view_readme()
            except:
                traceback.print_exc()
       
    except:
        if ( _check_compatible() ):
            from resources.lib import xbmcscript_player as script
            script.Main()


