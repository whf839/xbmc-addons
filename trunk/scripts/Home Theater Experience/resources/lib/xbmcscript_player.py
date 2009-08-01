"""
    Main Player Module:
    - plays optional trivia slide show w/music
    - plays optional coming attractions intro video/playlist
    - plays # of optional random trailers
    - plays optional feature presentation intro video/playlist
    - plays user queued video
    - plays optional end of feature presentation video/playlist
"""
# main imports
import sys
import os
import xbmcgui
import xbmc

_ = xbmc.Language( scriptPath=os.getcwd() ).getLocalizedString

# set proper message
try:
    sys.argv[ 1 ] == "clearWatched"
    message = 32530
except:
    message = 32520

pDialog = xbmcgui.DialogProgress()
pDialog.create( sys.modules[ "__main__" ].__script__, _( message )  )

from urllib import quote_plus
from random import shuffle


class Main:
    # base paths
    BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/" ), "script_data", os.path.basename( os.getcwd() ) )

    def __init__( self ):
        # get all the settings
        self._get_settings()
        #   if an arg was passed check it for clearWatched
        try:
            if ( sys.argv[ 1 ] == "clearWatched" ):
                self._clear_watched_items()
        except:
            # create the playlist
            self._create_playlist()
            # play the trivia slide show
            self._play_trivia()

    def _clear_watched_items( self ):
        try:
            # handle AMT db special
            if ( self.settings[ "trailer_scraper" ] == "amt_database" ):
                # get the correct scraper
                exec "from resources.scrapers.%s import scraper as scraper" % ( self.settings[ "trailer_scraper" ], )
                Scraper = scraper.Main( settings=self.settings )
                # update trailers
                ok = Scraper.clear_watched()
            else:
                # set base watxhed file path
                base_path = os.path.join( self.BASE_CURRENT_SOURCE_PATH, self.settings[ "trailer_scraper" ] + "_watched.txt" )
                # remove file
                os.remove( base_path )
        except:
            pass

    def _get_settings( self ):
        # get settings object
        __settings__ = xbmc.Settings( path=os.getcwd() )
        # initialize settings dictionary
        self.settings = {}
        # special settings
        self.settings[ "rating_videos_path" ] = xbmc.translatePath( __settings__.getSetting( "rating_videos_path" ) )
        self.settings[ "fpv_number" ] = ( 0, -1, 1, 2, 3, )[ int( __settings__.getSetting( "fpv_number" ) ) ]
        self.settings[ "feature_presentation_video" ] = __settings__.getSetting( "feature_presentation_video" )
        self.settings[ "feature_presentation_videos" ] = __settings__.getSetting( "feature_presentation_videos" )
        self.settings[ "epv_number" ] = ( 0, -1, 1, 2, 3, )[ int( __settings__.getSetting( "epv_number" ) ) ]
        self.settings[ "end_presentation_video" ] = __settings__.getSetting( "end_presentation_video" )
        self.settings[ "end_presentation_videos" ] = __settings__.getSetting( "end_presentation_videos" )
        # trailer settings
        self.settings[ "number_trailers" ] = ( 0, 1, 2, 3, 4, 5, 10, )[ int( __settings__.getSetting( "number_trailers" ) ) ]
        self.settings[ "cav_number" ] = ( 0, -1, 1, 2, 3, )[ int( __settings__.getSetting( "cav_number" ) ) ]
        self.settings[ "coming_attraction_video" ] = __settings__.getSetting( "coming_attraction_video" )
        self.settings[ "coming_attraction_videos" ] = __settings__.getSetting( "coming_attraction_videos" )
        self.settings[ "trailer_scraper" ] = ( "amt_database", "amt_current", "local", )[ int( __settings__.getSetting( "trailer_scraper" ) ) ]
        self.settings[ "amt_db_path" ] = xbmc.translatePath( __settings__.getSetting( "amt_db_path" ) )
        self.settings[ "trailer_path" ] = xbmc.translatePath( __settings__.getSetting( "trailer_path" ) )
        self.settings[ "unwatched_only" ] = __settings__.getSetting( "unwatched_only" ) == "true"
        self.settings[ "limit_query" ] = __settings__.getSetting( "limit_query" ) == "true"
        self.settings[ "trailer_rating" ] = __settings__.getSetting( "trailer_rating" )
        self.settings[ "amt_newest_only" ] = __settings__.getSetting( "amt_newest_only" ) == "true"
        self.settings[ "trailer_quality" ] = int( __settings__.getSetting( "trailer_quality" ) )
        self.settings[ "amt_hd_only" ] = __settings__.getSetting( "amt_hd_only" ) == "true"
        # trivia settings
        self.settings[ "trivia_total_time" ] = ( 0, 10, 15, 20, 30, 45, 60 )[ int( __settings__.getSetting( "trivia_total_time" ) ) ]
        self.settings[ "trivia_path" ] = xbmc.translatePath( __settings__.getSetting( "trivia_path" ) )
        self.settings[ "trivia_slide_time" ] = ( 10, 15, 20, 25, 30, 45, 60 )[ int( __settings__.getSetting( "trivia_slide_time" ) ) ]
        self.settings[ "trivia_music" ] = __settings__.getSetting( "trivia_music" )
        self.settings[ "trivia_music_volume" ] = int( __settings__.getSetting( "trivia_music_volume" ).replace( "%", "" ) )
        self.settings[ "trivia_end_image" ] = __settings__.getSetting( "trivia_end_image" )
        self.settings[ "trivia_end_music" ] = __settings__.getSetting( "trivia_end_music" )

    def _create_playlist( self ):
        # create a video playlist
        self.playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
        # get the queued video info
        mpaa, genre, movie = self._get_queued_video_info()
        # get rating video
        self._get_special_videos(   items=1, 
                                                path=self.settings[ "rating_videos_path" ],
                                                genre=_( 32603 ),
                                                index=0
                                            )
        # get feature presentation videos
        self._get_special_videos(   items=self.settings[ "fpv_number" ], 
                                                path=( self.settings[ "feature_presentation_video" ], self.settings[ "feature_presentation_videos" ], )[ self.settings[ "fpv_number" ] > 0 ],
                                                genre=_( 32601 ),
                                                index=0
                                            )
        # get trailers
        ok = self._get_trailers(  items=self.settings[ "number_trailers" ],
                                            mpaa=mpaa,
                                            genre=genre,
                                            movie=movie
                                        )
        # get coming attractions videos
        self._get_special_videos(   items=self.settings[ "cav_number" ] * ok, 
                                                path=( self.settings[ "coming_attraction_video" ], self.settings[ "coming_attraction_videos" ], )[ self.settings[ "cav_number" ] > 0 ],
                                                genre=_( 32600 ),
                                                index=0
                                            )
        # get end of feature presentation videos
        self._get_special_videos(   items=self.settings[ "epv_number" ], 
                                                path=( self.settings[ "end_presentation_video" ], self.settings[ "end_presentation_videos" ], )[ self.settings[ "epv_number" ] > 0 ],
                                                genre=_( 32602 )
                                            )

    def _get_queued_video_info( self ):
        try:
            # get movie name
            movie_title = self.playlist[ 0 ].getdescription()
            movie = os.path.splitext( os.path.basename( self.playlist[ 0 ].getfilename() ) )[ 0 ]
            # format our records start and end
            xbmc.executehttpapi( "SetResponseFormat()" )
            xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
            sql = "SELECT c12, c14 FROM movie WHERE c00='%s' LIMIT 1" % ( movie_title, )
            # query database for info dummy is needed as there are two </field> formatters
            mpaa, genre, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
            rating = mpaa.split( " " )
            part = 1 - ( len( rating ) == 1 )
            mpaa = rating[ part ]
        except:
            mpaa = ""
            genre = ""
            movie = ""
        # return results
        return mpaa, genre, movie

    def _get_special_videos( self, items, path, genre, index=-1 ):
        # return if not user preference
        if ( not items ):
            return
        # if path is a file check if file exists
        if ( not path.endswith( "/" ) and not path.endswith( "\\" ) and not ( xbmc.executehttpapi( "FileExists(%s)" % ( path, ) ) == "<li>True" ) ):
            return
        # set default paths list
        paths = [ path ]
        # if path is a folder fetch # videos
        if ( path.endswith( "/" ) or path.endswith( "\\" ) ):
            # initialize our lists (we want paths to be the same list as self.tmp_paths)
            paths = self.tmp_paths = []
            self._get_videos( [ path ] )
            shuffle( paths )
        # enumerate thru and add our videos
        for count in range( abs( items ) ):
            # set our path
            path = paths[ count ]
            # format a title (we don't want the ugly extension)
            title = os.path.splitext( os.path.basename( path ) )[ 0 ]
            # create the listitem and fill the infolabels
            listitem = self._get_listitem( title=title, url=path, genre=genre )
            # add our item to the playlist
            self.playlist.add( path, listitem, index=index )

    def _get_videos( self, paths ):
        # reset folders list
        folders = []
        # enumerate thru paths and fetch slides recursively
        for path in paths:
            # get the directory listing
            entries = xbmc.executehttpapi( "GetDirectory(%s)" % ( path, ) ).split( "\n" )
            # enumerate through our entries list and separate question, clue, answer
            for entry in entries:
                # remove <li> from item
                entry = entry.replace( "<li>", "" )
                # if folder add to our folder list to recursively fetch slides
                if ( entry.endswith( "/" ) ):
                    folders += [ entry ]
                # does this entry match our pattern "-trailer." and is a video file
                elif ( entry and os.path.splitext( entry )[ 1 ] in xbmc.getSupportedMedia( "video" ) ):
                    # add our entry
                    self.tmp_paths += [ entry ]
        # if there are folders call again (we want recursive)
        if ( folders ):
            self._fetch_trailers( folders )

    def _get_trailers( self, items, mpaa, genre, movie ):
        # return if not user preference
        if ( not items ):
            return items
        # update dialog
        pDialog.update( -1, _( 32500 ) )
        # get the correct scraper
        exec "from resources.scrapers.%s import scraper as scraper" % ( self.settings[ "trailer_scraper" ], )
        Scraper = scraper.Main( mpaa, genre, self.settings, movie )
        # fetch trailers
        trailers = Scraper.fetch_trailers()
        # initalize our check (false in case no trailers were returned)
        ok = False
        # enumerate through our list of trailers and add them to our playlist
        for trailer in trailers:
            # create the listitem and fill the infolabels
            listitem = self._get_listitem( title=trailer[ 1 ],
                                                        url=trailer[ 2 ],
                                                        thumbnail=trailer[ 3 ],
                                                        plot=trailer[ 4 ],
                                                        runtime=trailer[ 5 ],
                                                        mpaa=trailer[ 6 ],
                                                        release_date=trailer[ 7 ],
                                                        studio=trailer[ 8 ] or _( 32604 ),
                                                        genre=trailer[ 9 ] or _( 32605 ),
                                                        writer=trailer[ 10 ],
                                                        director=trailer[ 11 ] )
            # add our item to the playlist
            if ( trailer[ 2 ] ):
                # we have trailers
                ok = True
                self.playlist.add( trailer[ 2 ], listitem, index=0 )
        # return success
        return ok

    def _get_listitem( self, title="", url="", thumbnail=None, plot="", runtime="", mpaa="", release_date="0 0 0", studio=_( 32604 ), genre="", writer="", director=""):
        # check for a valid thumbnail
        if ( thumbnail is None ):
            thumbnail = self._get_thumbnail( url )
        # set the default icon
        icon = "DefaultVideo.png"
        # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
        listitem = xbmcgui.ListItem( title, iconImage=icon, thumbnailImage=thumbnail )
        # release date and year
        try:
            parts = release_date.split( " " )
            year = int( parts[ 2 ] )
        except:
            year = 0
        # add the different infolabels we want to sort by
        listitem.setInfo( type="Video", infoLabels={ "Title": title, "Plot": plot, "PlotOutline": plot, "RunTime": runtime, "MPAA": mpaa, "Year": year, "Studio": studio, "Genre": genre, "Writer": writer, "Director": director } )
        # return result
        return listitem

    def _get_thumbnail( self, url ):
        # if the cached thumbnail does not exist create the thumbnail based on filepath.tbn
        filename = xbmc.getCacheThumbName( url )
        thumbnail = os.path.join( self.BASE_CACHE_PATH, filename[ 0 ], filename )
        # if cached thumb does not exist return empty
        if ( not os.path.isfile( thumbnail ) ):
            # set empty string
            thumbnail = ""
        # return result
        return thumbnail

    def _play_trivia( self ):
        # if user cancelled dialog return
        if ( pDialog.iscanceled() ):
            pDialog.close()
            return
        # if trivia path and time to play the trivia slides
        if (self.settings[ "trivia_path" ] and self.settings[ "trivia_total_time" ] ):
            # update dialog with new message
            pDialog.update( -1, _( 32510 ) )
            # import trivia module and execute the gui
            from resources.lib.xbmcscript_trivia import Trivia as Trivia
            ui = Trivia( "script-HTExperience-trivia.xml", os.getcwd(), "default", False, settings=self.settings, playlist=self.playlist, dialog=pDialog )
            ui.doModal()
            del ui
            # we need to activate the video window
            xbmc.executebuiltin( "XBMC.ActivateWindow(2005)" )
        else:
            # no trivia slide show so play the video
            pDialog.close()
            # play the video playlist
            xbmc.Player().play( self.playlist )
