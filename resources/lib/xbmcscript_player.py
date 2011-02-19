__script__ = "Cinema Experience"
__scriptID__ = "script.cinema.experience"
###########################################################
"""
    Video Playlist Module:
    - Assembles Video Playlist based on user settings
    - When playlist complete, calls xbmcscript_trivia.py to perform trivia and start playlist
"""
############################################################
# main imports
import sys
import os
import xbmcgui
import xbmc
import xbmcaddon

_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting


# set proper message
try:
    message = ( 32530, 32540, )[ sys.argv[ 1 ] == "ClearWatchedTrailers" ]
except:
    message = 32520

pDialog = xbmcgui.DialogProgress()
pDialog.create( __script__, _L_( message )  )
pDialog.update( 0 )

from urllib import quote_plus
from random import shuffle, random

log_sep = "-"*70

class Main:
    # base paths
    BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data/" ), os.path.basename( _A_.getAddonInfo('path') ) )
    def __init__( self ):
        import traceback 
        self.number_of_features = int( _S_( "number_of_features") ) + 1
        self.playlistsize = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
        try:
            # create the playlist
            self.playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
            # Check to see if multiple features have been set in settings
            # if multiple features is greater than 1(not a single feature) 
            # add the intermission videos and audio files for the 2, third, etc movies
            if self.playlistsize > 1 and ( int( _S_( "intermission_video") ) > 0 or _S_( "intermission_audio") or _S_( "intermission_ratings") ): 
                for feature_count in range (1, self.playlistsize + 1):
                    xbmc.log( "[script.cinema.experience] - Feature #%-2d - %s" % ( feature_count, self.playlist[ feature_count - 1 ].getdescription() ), xbmc.LOGNOTICE )
                mpaa, audio, genre, movie = self._add_intermission_videos()
            # otherwise just build for a single video
            else:
                # get the queued video info
                xbmc.log( "[script.cinema.experience] - Feature - %s" % self.playlist[ 0 ].getdescription(), xbmc.LOGNOTICE )
                mpaa, audio, genre, movie = self._get_queued_video_info()
            self._create_playlist( mpaa, audio, genre, movie)
            # play the trivia slide show
            self._play_trivia( mpaa=mpaa, genre=genre )
        except:
            traceback.print_exc()

    def _add_intermission_videos( self ):
        xbmc.log( "[script.cinema.experience] - Adding intermission Video(s)", xbmc.LOGNOTICE )
        count = 0
        index_count = 1
        for feature in range( 1, self.playlistsize ):
            mpaa, audio, genre, movie = self._get_queued_video_info( index_count )
            #count = index_count
            # add intermission video
            if ( int( _S_( "intermission_video") ) > 0 ):
                xbmc.log( "[script.cinema.experience] - Inserting intermission Video(s): %s" % int( _S_( "intermission_video" ) ), xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] -     playlist Position: %d" % index_count, xbmc.LOGNOTICE )
                p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.log( "[script.cinema.experience] -     p_size: %d" % p_size, xbmc.LOGNOTICE )
                self._get_special_items(    playlist=self.playlist,
                                                    items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "intermission_video" ) ) ], 
                                                    path=( xbmc.translatePath( _S_( "intermission_video_file" ) ), xbmc.translatePath( _S_( "intermission_video_folder" ) ), )[ int( _S_( "intermission_video" ) ) > 1 ],
                                                    genre=_L_( 32612 ),
                                                    writer=_L_( 32612 ),
                                                    index=index_count
                                        )
                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size: 
                    index_count = index_count + int( _S_( "intermission_video" ) ) - 1
            # get rating video
            if ( _S_( "enable_ratings" ) ) == "true"  and (_S_( "intermission_ratings") ) == "true":
                xbmc.log( "[script.cinema.experience] - Inserting Intermission Rating Video",xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] -     playlist Position: %d" % index_count, xbmc.LOGNOTICE )
                p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.log( "[script.cinema.experience] -     p_size: %d" % p_size, xbmc.LOGNOTICE )
                self._get_special_items(    playlist=self.playlist,
                                                    items=1 * ( _S_( "rating_videos_folder" ) != "" ),
                                                    path=xbmc.translatePath( _S_( "rating_videos_folder" ) ) + mpaa + ".avi",
                                                    genre=_L_( 32603 ),
                                                    writer=_L_( 32603 ),
                                                    index = index_count
                                                    )
                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size:
                    index_count = index_count + 1
            # get Dolby/DTS videos
            if ( _S_( "enable_audio" ) ) == "true"  and (_S_( "intermission_audio") ) == "true":
                xbmc.log( "[script.cinema.experience] - Inserting Intermission Audio Format Video",xbmc.LOGNOTICE )
                xbmc.log( "[script.cinema.experience] -     playlist Position: %d" % index_count, xbmc.LOGNOTICE )
                p_size = xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size()
                xbmc.log( "[script.cinema.experience] -     p_size: %d" % p_size, xbmc.LOGNOTICE )
                self._get_special_items(    playlist=self.playlist,
                                                    items=1 * ( _S_( "audio_videos_folder" ) != "" ),
                                                    path=xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTS-MA" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ],
                                                    genre=_L_( 32606 ),
                                                    writer=_L_( 32606 ),
                                                    index = index_count
                                                    )
                # Move to the next feature + 1 - if we insert 2 videos, the next feature is 3 away from the first video, then prepare for the next intro(+1)
                # count = feature * 3 + 1
                if xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size() > p_size:
                    index_count = index_count + 1
            index_count = index_count + 1 
        # return info from first movie in playlist                                        
        mpaa, audio, genre, movie = self._get_queued_video_info( 0 )
        return mpaa, audio, genre, movie
        
    def _create_playlist( self, mpaa, audio, genre, movie ):
        # TODO: try to get a local thumb for special videos?
        xbmc.log( "[script.cinema.experience] - Building Cinema Experience Playlist",xbmc.LOGNOTICE )
        # get Dolby/DTS videos
        xbmc.log( "[script.cinema.experience] - Adding Audio Format Video",xbmc.LOGNOTICE )
        if ( _S_( "enable_audio" ) ) == "true" and ( _S_( "audio_videos_folder" ) ):
                self._get_special_items(    playlist=self.playlist,
                                                    items=1 * ( _S_( "audio_videos_folder" ) != "" ),
                                                    path=xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTS-MA" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ],
                                                    genre=_L_( 32606 ),
                                                    writer=_L_( 32606 ),
                                                    index=0
                                                )
        # Add Countdown video
        xbmc.log( "[script.cinema.experience] - Adding Count Down Videos: %s Videos" % _S_( "countdown_video" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "countdown_video" ) ) ], 
                                                path=( xbmc.translatePath( _S_( "countdown_video_file" ) ), xbmc.translatePath( _S_( "countdown_video_folder" ) ), )[ int( _S_( "countdown_video" ) ) > 1 ],
                                                genre=_L_( 32611 ),
                                                writer=_L_( 32611 ),
                                                index=0
                                            )
        # get rating video
        xbmc.log( "[script.cinema.experience] - Adding Ratings Video",xbmc.LOGNOTICE )
        if ( _S_( "enable_ratings" ) ) == "true" :
            self._get_special_items(    playlist=self.playlist,
                                                    items=1 * ( _S_( "rating_videos_folder" ) != "" ), 
                                                    path=xbmc.translatePath( _S_( "rating_videos_folder" ) ) + mpaa + ".avi",
                                                    genre=_L_( 32603 ),
                                                    writer=_L_( 32603 ),
                                                    index=0
                                                )
        # get feature presentation intro videos
        xbmc.log( "[script.cinema.experience] - Adding Feature Presentation Intro Videos: %s Videos" % _S_( "fpv_intro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "fpv_intro" ) ) ], 
                                                path=( xbmc.translatePath( _S_( "fpv_intro_file" ) ), xbmc.translatePath( _S_( "fpv_intro_folder" ) ), )[ int( _S_( "fpv_intro" ) ) > 1 ],
                                                genre=_L_( 32601 ),
                                                writer=_L_( 32601 ),
                                                index=0
                                            )
        # get trailers
        xbmc.log( "[script.cinema.experience] - Retriving Trailers: %s Trailers" % _S_( "trailer_count" ),xbmc.LOGNOTICE )
        trailers = self._get_trailers(  items=( 0, 1, 2, 3, 4, 5, 10, )[ int( _S_( "trailer_count" ) ) ],
                                                   mpaa=mpaa,
                                                   genre=genre,
                                                   movie=movie
                                                )
        # get coming attractions outro videos
        xbmc.log( "[script.cinema.experience] - Adding Coming Attraction Video: %s Videos" % _S_( "cav_outro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "cav_outro" ) ) ] * ( len( trailers ) > 0 ), 
                                                path=( xbmc.translatePath( _S_( "cav_outro_file" ) ), xbmc.translatePath( _S_( "cav_outro_folder" ) ), )[ int( _S_( "cav_outro" ) ) > 1 ],
                                                genre=_L_( 32608 ),
                                                writer=_L_( 32608 ),
                                                index=0
                                            )
        # enumerate through our list of trailers and add them to our playlist
        xbmc.log( "[script.cinema.experience] - Adding Trailers: %s Trailers" % len( trailers ),xbmc.LOGNOTICE )
        for trailer in trailers:
            # get trailers
            self._get_special_items(    playlist=self.playlist,
                                                    items=1,
                                                    path=trailer[ 2 ],
                                                    genre=trailer[ 9 ] or _L_( 32605 ),
                                                    title=trailer[ 1 ],
                                                    thumbnail=trailer[ 3 ],
                                                    plot=trailer[ 4 ],
                                                    runtime=trailer[ 5 ],
                                                    mpaa=trailer[ 6 ],
                                                    release_date=trailer[ 7 ],
                                                    studio=trailer[ 8 ] or _L_( 32604 ),
                                                    writer= _L_( 32605 ),
                                                    director=trailer[ 11 ],
                                                    index=0
                                                )
        # get coming attractions intro videos
        xbmc.log( "[script.cinema.experience] - Adding Coming Attraction Intro Videos: %s Videos" % _S_( "cav_intro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "cav_intro" ) ) ] * ( len( trailers ) > 0 ), 
                                                path=( xbmc.translatePath( _S_( "cav_intro_file" ) ), xbmc.translatePath( _S_( "cav_intro_folder" ) ), )[ int( _S_( "cav_intro" ) ) > 1 ],
                                                genre=_L_( 32600 ),
                                                writer=_L_( 32600 ),
                                                index=0
                                            )
        # get movie theater experience intro videos
        xbmc.log( "[script.cinema.experience] - Adding Movie Theatre Intro Videos: %s Videos" % _S_( "mte_intro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "mte_intro" ) ) ], 
                                                path=( xbmc.translatePath( _S_( "mte_intro_file" ) ), xbmc.translatePath( _S_( "mte_intro_folder" ) ), )[ int( _S_( "mte_intro" ) ) > 1 ],
                                                genre=_L_( 32607 ),
                                                writer=_L_( 32607 ),
                                                index=0
                                            )
        # get trivia outro video(s)
        xbmc.log( "[script.cinema.experience] - Adding Trivia Outro Videos: %s Videos" % _S_( "trivia_outro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                    items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_outro" ) ) ], 
                                                    path=( xbmc.translatePath( _S_( "trivia_outro_file" ) ), xbmc.translatePath( _S_( "trivia_outro_folder" ) ), )[ int( _S_( "trivia_outro" ) ) > 1 ],
                                                    genre=_L_( 32610 ),
                                                    writer=_L_( 32610 ),
                                                    index=0
                                                    #media_type="video/picture"
                                                )
        # get feature presentation outro videos
        xbmc.log( "[script.cinema.experience] - Adding Feature Presentation Outro Videos: %s Videos" % _S_( "fpv_outro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "fpv_outro" ) ) ], 
                                                path=( xbmc.translatePath( _S_( "fpv_outro_file" ) ), xbmc.translatePath( _S_( "fpv_outro_folder" ) ), )[ int( _S_( "fpv_outro" ) ) > 1 ],
                                                genre=_L_( 32602 ),
                                                writer=_L_( 32602 ),
                                                
                                            )
        # get movie theater experience outro videos
        xbmc.log( "[script.cinema.experience] - Adding Movie Theatre Outro Videos: %s Videos" % _S_( "mte_outro" ),xbmc.LOGNOTICE )
        self._get_special_items(    playlist=self.playlist,
                                                items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "mte_outro" ) ) ], 
                                                path=( xbmc.translatePath( _S_( "mte_outro_file" ) ), xbmc.translatePath( _S_( "mte_outro_folder" ) ), )[ int( _S_( "mte_outro" ) ) > 1 ],
                                                genre=_L_( 32607 ),
                                                writer=_L_( 32607 ),
                                                
                                            )
        xbmc.log( "[script.cinema.experience] - Playlist Size: %s" % xbmc.PlayList(xbmc.PLAYLIST_VIDEO).size(), xbmc.LOGNOTICE )
        return
        
    def _get_queued_video_info( self, feature=0 ):
        xbmc.log( "[script.cinema.experience] - _get_queued_video_info()", xbmc.LOGNOTICE )
        try:            
            # get movie name
            movie_title = self.playlist[ feature ].getdescription()
            # this is used to skip trailer for current movie selection
            movie = os.path.splitext( os.path.basename( self.playlist[ feature ].getfilename() ) )[ 0 ]
            # format our records start and end
            xbmc.executehttpapi( "SetResponseFormat()" )
            xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
            # TODO: verify the first is the best audio
            # setup the sql, we limit to 1 record as there can be multiple entries in streamdetails
            sql = "SELECT movie.c12, movie.c14, streamdetails.strAudioCodec FROM movie, streamdetails WHERE movie.idFile=streamdetails.idFile AND streamdetails.iStreamType=1 AND c00='%s' LIMIT 1" % ( movie_title.replace( "'", "''", ), )
            xbmc.log( "[script.cinema.experience]  - SQL: %s" % ( sql, ), xbmc.LOGNOTICE )
            # query database for info dummy is needed as there are two </field> formatters
            mpaa, genre, audio, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
            # TODO: add a check and new sql for videos queued from files mode, or try an nfo
            # calculate rating
            if mpaa == "":
                mpaa = "NR"
            elif mpaa.startswith("Rated"):
                mpaa = mpaa.split( " " )[ 1 - ( len( mpaa.split( " " ) ) == 1 ) ]
                mpaa = ( mpaa, "NR", )[ mpaa not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", ) ]
            else:
                mpaa = ( mpaa, "NR", )[ mpaa not in ( "12", "12A", "PG", "15", "18", "MA", "U", ) ]
        except:
            movie_title = mpaa = audio = genre = movie = ""
        # spew queued video info to log
        xbmc.log( "[script.cinema.experience] - Queued Movie Information", xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] " + log_sep, xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Title: %s" % ( movie_title, ), xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Path: %s" % ( movie, ), xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Genre: %s" % ( genre, ), xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - MPAA: %s" % ( mpaa, ), xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience] - Audio: %s" % ( audio, ), xbmc.LOGNOTICE )
        if ( _S_( "audio_videos_folder" ) ):
            xbmc.log( "[script.cinema.experience] - Folder: %s" % ( xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "dtsma": "DTS-MA", "ac3": "Dolby" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ], ), xbmc.LOGNOTICE )
        xbmc.log( "[script.cinema.experience]  %s" % log_sep, xbmc.LOGNOTICE )
        # return results
        return mpaa, audio, genre, movie

    def _get_special_items(   self, playlist, items, path, genre, title="", thumbnail=None, plot="",
                                                runtime="", mpaa="", release_date="0 0 0", studio="", writer="",
                                                director="", index=-1, media_type="video"
                                            ):
        import traceback
        # return if not user preference
        if ( not items ):
            return
        # if path is a file check if file exists
        if ( os.path.splitext( path )[ 1 ] and not path.startswith( "http://" ) and not ( xbmc.executehttpapi( "FileExists(%s)" % ( path, ) ) == "<li>True" ) ):
            return
        # set default paths list
        self.tmp_paths = [ path ]
        # if path is a folder fetch # videos/pictures
        if ( path.endswith( "/" ) or path.endswith( "\\" ) ):
            # initialize our lists
            self.tmp_paths = []
            self._get_items( [ path ], media_type )
            count = 0
            while count <6:
                shuffle( self.tmp_paths, random )
                count=count+1
        # enumerate thru and add our videos/pictures
        for count in range( items ):
            try:
                # set our path
                path = self.tmp_paths[ count ]
                # format a title (we don't want the ugly extension)
                title = title or os.path.splitext( os.path.basename( path ) )[ 0 ]
                # create the listitem and fill the infolabels
                listitem = self._get_listitem( title=title,
                                                    url=path,
                                                    thumbnail=thumbnail,
                                                    plot=plot,
                                                    runtime=runtime,
                                                    mpaa=mpaa,
                                                    release_date=release_date,
                                                    studio=studio or _L_( 32604 ),
                                                    genre=genre or _L_( 32605 ),
                                                    writer=writer,
                                                    director=director
                                                )
                # add our video/picture to the playlist or list
                if ( isinstance( playlist, list ) ):
                    playlist += [ ( path, listitem, ) ]
                else:
                    playlist.add( path, listitem, index=index )
            except:
                if items > count:
                    xbmc.log( "[script.cinema.experience] - Looking for %d files, but only found %d" % (items, count), level=xbmc.LOGNOTICE)
                    break
                else:
                    traceback.print_exc()
                
    def _get_items( self, paths, media_type ):
        # reset folders list
        folders = []
        # enumerate thru paths and fetch videos/pictures recursively
        for path in paths:
            # get the directory listing
            entries = xbmc.executehttpapi( "GetDirectory(%s)" % ( path, ) ).split( "\n" )
            # enumerate through our entries list and check for valid media type
            for entry in entries:
                # remove <li> from item
                entry = entry.replace( "<li>", "" )
                # if folder add to our folder list to recursively fetch videos/pictures
                if ( entry.endswith( "/" ) or entry.endswith( "\\" ) ):
                    folders += [ entry ]
                # is this a valid video/picture file
                elif ( entry and ( ( media_type.startswith( "video" ) and os.path.splitext( entry )[ 1 ] in xbmc.getSupportedMedia( "video" ) ) or
                    ( media_type.endswith( "picture" ) and os.path.splitext( entry )[ 1 ] in xbmc.getSupportedMedia( "picture" ) ) ) ):
                    # add our entry
                    self.tmp_paths += [ entry ]
        # if there are folders call again (we want recursive)
        if ( folders ):
            self._get_items( folders, media_type )

    def _get_trailers( self, items, mpaa, genre, movie ):
        # return if not user preference
        if ( not items ):
            return []
        # update dialog
        pDialog.update( -1, _L_( 32500 ) )
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

    def _get_listitem( self, title="", url="", thumbnail=None, plot="", runtime="", mpaa="", release_date="0 0 0", studio=_L_( 32604 ), genre="", writer="", director=""):
        # check for a valid thumbnail
        thumbnail = self._get_thumbnail( ( thumbnail, url, )[ thumbnail is None ] )
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
        xbmc.log( "[script.cinema.experience]  - Thumbnail Url: %s" % url, xbmc.LOGNOTICE )
        # if the cached thumbnail does not exist create the thumbnail based on filepath.tbn
        filename = xbmc.getCacheThumbName( url )
        thumbnail = os.path.join( self.BASE_CACHE_PATH, filename[ 0 ], filename )
        xbmc.log( "[script.cinema.experience]  - Thumbnail Filename: %s" % filename, xbmc.LOGNOTICE )
        # if cached thumb does not exist try auto generated
        if ( not os.path.isfile( thumbnail ) ):
            thumbnail = os.path.join( self.BASE_CACHE_PATH, filename[ 0 ], "auto-" + filename )
        # if cached thumb does not exist set default
        if ( not os.path.isfile( thumbnail ) ):
            thumbnail = "DefaultVideo.png"
        # return result
        return thumbnail

    def _play_trivia( self, mpaa, genre ):
        # if user cancelled dialog return
        if ( pDialog.iscanceled() ):
            pDialog.close()
            return
        # if trivia path and time to play the trivia slides
        if ( _S_( "trivia_folder" ) and int( float( _S_( "trivia_total_time" ) ) ) > 0 ):
            # update dialog with new message
            pDialog.update( -1, _L_( 32510 ) )
            # initialize intro/outro lists
            playlist_intro = []
            playlist_outro = []
            # get trivia intro videos
            self._get_special_items(    playlist=playlist_intro,
                                                    items=( 0, 1, 1, 2, 3, 4, 5, )[ int( _S_( "trivia_intro" ) ) ], 
                                                    path=( xbmc.translatePath( _S_( "trivia_intro_file" ) ), xbmc.translatePath( _S_( "trivia_intro_folder" ) ), )[ int( _S_( "trivia_intro" ) ) > 1 ],
                                                    genre=_L_( 32609 ),
                                                    #media_type="video/picture"
                                                )
            
            # trivia settings, grab them here so we don't need another _S_() object
            settings = {  "trivia_total_time": int( float( _S_( "trivia_total_time" ) ) ),
                                "trivia_folder":  xbmc.translatePath( _S_( "trivia_folder" ) ),
                                "trivia_slide_time": int( float( _S_( "trivia_slide_time" ) ) ),
                                "trivia_intro_playlist": playlist_intro,
                                "trivia_music": _S_( "trivia_music" ),
                                "trivia_adjust_volume": _S_( "trivia_adjust_volume" ),
                                "trivia_fade_volume": _S_( "trivia_fade_volume" ),
                                "trivia_fade_time": int( float( _S_( "trivia_fade_time" ) ) ),
                                "trivia_music_file":  xbmc.translatePath( _S_( "trivia_music_file" ) ),
                                "trivia_music_folder":  xbmc.translatePath( _S_( "trivia_music_folder" ) ),
                                "trivia_music_volume": int( float( _S_( "trivia_music_volume" ) ) ),
                                "trivia_unwatched_only": _S_( "trivia_unwatched_only" ) == "true"                                
                            }
            # set the proper mpaa rating user preference
            mpaa = (  _S_( "trivia_rating" ), mpaa, )[ _S_( "trivia_limit_query" ) == "true" ]
            xbmc.log( "[script.cinema.experience] - MPAA Rating: %s" % mpaa, xbmc.LOGNOTICE )
            # import trivia module and execute the gui
            from resources.lib.xbmcscript_trivia import Trivia as Trivia
            xbmc.log( "[script.cinema.experience] - Starting Trivia script", xbmc.LOGNOTICE )
            ui = Trivia( "script-CExperience-trivia.xml", _A_.getAddonInfo('path'), "default", "720p", settings=settings, playlist=self.playlist, dialog=pDialog, mpaa=mpaa, genre=genre )
            #ui.doModal()
            del ui
            # we need to activate the video window
            xbmc.executebuiltin( "XBMC.ActivateWindow(2005)" )
        else:
            # no trivia slide show so play the video
            pDialog.close()
            # play the video playlist
            xbmc.Player().play( self.playlist )
        
            
    
