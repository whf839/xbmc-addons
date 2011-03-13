__script__ = "Cinema Experience"
__scriptID__ = "script.cinema.experience"

import traceback, os, re, sys
import xbmc, xbmcaddon, xbmcgui
from urllib import quote_plus
from random import shuffle, random


_A_ = xbmcaddon.Addon( __scriptID__ )
# language method
_L_ = _A_.getLocalizedString
# settings method
_S_ = _A_.getSetting

#tmp_paths = []
BASE_CACHE_PATH = os.path.join( xbmc.translatePath( "special://profile" ), "Thumbnails", "Video" )
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( _A_.getAddonInfo('path'), 'resources' ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

from music import parse_playlist
from folder import dirEntries

log_sep = "-"*70

def _get_trailers( items, mpaa, genre, movie ):
    # return if not user preference
    if ( not items ):
        return []
    # trailer settings, grab them here so we don't need another _S_() object
    settings = { "trailer_amt_db_file":  xbmc.translatePath( _S_( "trailer_amt_db_file" ) ),
                      "trailer_folder":  xbmc.translatePath( _S_( "trailer_folder" ) ),
                      "trailer_rating": _S_( "trailer_rating" ),
                  "trailer_limit_mpaa": _S_( "trailer_limit_mpaa" ) == "true",
                 "trailer_limit_genre": _S_( "trailer_limit_genre" ) == "true",
                   "trailer_play_mode": int( _S_( "trailer_play_mode" ) ),
                     "trailer_hd_only": _S_( "trailer_hd_only" ) == "true",
                     "trailer_quality": int( _S_( "trailer_quality" ) ),
              "trailer_unwatched_only": _S_( "trailer_unwatched_only" ) == "true",
                 "trailer_newest_only": _S_( "trailer_newest_only" ) == "true",
                       "trailer_count": ( 0, 1, 2, 3, 4, 5, 10, )[ int( _S_( "trailer_count" ) ) ],
                     "trailer_scraper": ( "amt_database", "amt_current", "local", "xbmc_library", )[ int( _S_( "trailer_scraper" ) ) ]
               }
    # get the correct scraper
    exec "from resources.scrapers.%s import scraper as scraper" % ( settings[ "trailer_scraper" ], )
    Scraper = scraper.Main( mpaa, genre, settings, movie )
    # fetch trailers
    trailers = Scraper.fetch_trailers()
    # return results
    return trailers

def _get_special_items( playlist, items, path, genre, title="", thumbnail=None, plot="",
                        runtime="", mpaa="", release_date="0 0 0", studio="", writer="",
                        director="", index=-1, media_type="video"
                      ):
    xbmc.log( "[script.cinema.experience] - _get_special_items() Started", level=xbmc.LOGNOTICE)
    # return if not user preference
    if ( not items ):
        return
    # if path is a file check if file exists
    if ( os.path.splitext( path )[ 1 ] and not path.startswith( "http://" ) and not ( xbmc.executehttpapi( "FileExists(%s)" % ( path, ) ) == "<li>True" ) ):
        return
    # set default paths list
    tmp_paths = [ path ]
    # if path is a folder fetch # videos/pictures
    if ( path.endswith( "/" ) or path.endswith( "\\" ) ):
        # initialize our lists
        tmp_paths = _get_items( [ path ], media_type, tmp_paths )
        count = 0
        while count <6:
            shuffle( tmp_paths, random )
            count += 1
    # enumerate thru and add our videos/pictures
    for count in range( items ):
        try:
            # set our path
            path = tmp_paths[ count ]
            # format a title (we don't want the ugly extension)
            title = title or os.path.splitext( os.path.basename( path ) )[ 0 ]
            # create the listitem and fill the infolabels
            listitem = _get_listitem( title=title,
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
            traceback.print_exc()
            if items > count:
                xbmc.log( "[script.cinema.experience] - Looking for %d files, but only found %d" % (items, count), level=xbmc.LOGNOTICE)
                break
            else:
                traceback.print_exc()

def _get_items( paths, media_type, tmp_paths ):
    xbmc.log( "[script.cinema.experience] - _get_items() Started", level=xbmc.LOGNOTICE)
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
                tmp_paths += [ entry ]
    # if there are folders call again (we want recursive)
    if ( folders ):
        _get_items( folders, media_type )
    return tmp_paths

def _get_listitem( title="", url="", thumbnail=None, plot="", runtime="", mpaa="", release_date="0 0 0", studio=_L_( 32604 ), genre="", writer="", director=""):
    # check for a valid thumbnail
    thumbnail = _get_thumbnail( ( thumbnail, url, )[ thumbnail is None ] )
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

def _get_thumbnail( url ):
    xbmc.log( "[script.cinema.experience] - _get_thumbnail() Started", level=xbmc.LOGNOTICE)
    xbmc.log( "[script.cinema.experience] - Thumbnail Url: %s" % url, xbmc.LOGNOTICE )
    # if the cached thumbnail does not exist create the thumbnail based on filepath.tbn
    filename = xbmc.getCacheThumbName( url )
    thumbnail = os.path.join( BASE_CACHE_PATH, filename[ 0 ], filename )
    xbmc.log( "[script.cinema.experience] - Thumbnail Filename: %s" % filename, xbmc.LOGNOTICE )
    # if cached thumb does not exist try auto generated
    if ( not os.path.isfile( thumbnail ) ):
        thumbnail = os.path.join( BASE_CACHE_PATH, filename[ 0 ], "auto-" + filename )
    # if cached thumb does not exist set default
    if ( not os.path.isfile( thumbnail ) ):
        thumbnail = "DefaultVideo.png"
    # return result
    return thumbnail

def _get_queued_video_info( feature = 0 ):
    xbmc.log( "[script.cinema.experience] - _get_queued_video_info() Started", xbmc.LOGNOTICE )
    try:
        # get movie name
        movie_title = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[ feature ].getdescription()
        # this is used to skip trailer for current movie selection
        movie = os.path.splitext( os.path.basename( xbmc.PlayList( xbmc.PLAYLIST_VIDEO )[ feature ].getfilename() ) )[ 0 ]
        # format our records start and end
        xbmc.executehttpapi( "SetResponseFormat()" )
        xbmc.executehttpapi( "SetResponseFormat(OpenField,)" )
        # TODO: verify the first is the best audio
        # setup the sql, we limit to 1 record as there can be multiple entries in streamdetails
        sql = "SELECT movie.c12, movie.c14, streamdetails.strAudioCodec FROM movie, streamdetails WHERE movie.idFile=streamdetails.idFile AND streamdetails.iStreamType=1 AND c00='%s' LIMIT 1" % ( movie_title.replace( "'", "''", ), )
        xbmc.log( "[script.cinema.experience] - SQL: %s" % ( sql, ), xbmc.LOGNOTICE )
        # query database for info dummy is needed as there are two </field> formatters
        mpaa, genre, audio, dummy = xbmc.executehttpapi( "QueryVideoDatabase(%s)" % quote_plus( sql ), ).split( "</field>" )
        # TODO: add a check and new sql for videos queued from files mode, or try an nfo
        # calculate rating
        if mpaa == "":
            mpaa = "NR"
        elif mpaa.startswith("Rated"):
            mpaa = mpaa.split( " " )[ 1 - ( len( mpaa.split( " " ) ) == 1 ) ]
            mpaa = ( mpaa, "NR", )[ mpaa not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", ) ]
        elif mpaa.startswith("UK"):
            mpaa = mpaa.split( ":" )[ 1 - ( len( mpaa.split( ":" ) ) == 1 ) ]
            mpaa = ( mpaa, "NR", )[ mpaa not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
        else:
            mpaa = ( mpaa, "NR", )[ mpaa not in ( "12", "12A", "PG", "15", "18", "R18", "MA", "U", ) ]
        if mpaa not in ( "G", "PG", "PG-13", "R", "NC-17", "Unrated", "NR" ):
            if mpaa in ("12", "12A",):
                equivalent_mpaa = "PG-13"
            elif mpaa == "15":
                equivalent_mpaa = "R"
            elif mpaa == "U":
                equivalent_mpaa = "G"
            elif mpaa in ("18", "R18", "MA",):
                equivalent_mpaa = "NC-17"
            else:
                equivalent_mpaa = mpaa
    except:
        traceback.print_exc()
        movie_title = mpaa = audio = genre = movie = equivalent_mpaa = ""
    # spew queued video info to log
    xbmc.log( "[script.cinema.experience] - Queued Movie Information", xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] " + log_sep, xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Title: %s" % ( movie_title, ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Path: %s" % ( movie, ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Genre: %s" % ( genre, ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - MPAA: %s" % ( mpaa, ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience] - Audio: %s" % ( audio, ), xbmc.LOGNOTICE )
    if ( _S_( "audio_videos_folder" ) ):
        xbmc.log( "[script.cinema.experience] - Folder: %s" % ( xbmc.translatePath( _S_( "audio_videos_folder" ) ) + { "dca": "DTS", "ac3": "Dolby", "dtsma": "DTSHD-MA", "dtshd_ma": "DTSHD-MA", "a_truehd": "Dolby TrueHD", "truehd": "Dolby TrueHD" }.get( audio, "Other" ) + xbmc.translatePath( _S_( "audio_videos_folder" ) )[ -1 ], ), xbmc.LOGNOTICE )
    xbmc.log( "[script.cinema.experience]  %s" % log_sep, xbmc.LOGNOTICE )
    # return results
    return mpaa, audio, genre, movie, equivalent_mpaa

def _wait_until_end(): # wait until the end of the playlist(for Trivia Intro)
    xbmc.log( "[script.cinema.experience] - Waiting Until End Of Trivia Intro Playlist", xbmc.LOGNOTICE)
    psize = xbmc.PlayList( xbmc.PLAYLIST_VIDEO ).size() - 1
    xbmc.log( "[script.cinema.experience] - Playlist Size: %s" % ( psize + 1), xbmc.LOGNOTICE)
    while xbmc.PlayList( xbmc.PLAYLIST_VIDEO ).getposition() < psize:
        pass
    xbmc.log( "[script.cinema.experience] - Video TotalTime: %s" % xbmc.Player().getTotalTime(), xbmc.LOGNOTICE)
    while xbmc.Player().getTime() < ( xbmc.Player().getTotalTime() - 0.5 ):
        pass
    xbmc.log( "[script.cinema.experience] - Video getTime: %s" % xbmc.Player().getTime(), xbmc.LOGNOTICE)
    xbmc.sleep(500)

def build_music_playlist():
    xbmc.log( "[script.cinema.experience] - Building Music Playlist", xbmc.LOGNOTICE)
    xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioPlaylist.Clear", "id": 1}')
    track_location =[]
    music_playlist = xbmc.PlayList( xbmc.PLAYLIST_MUSIC )
    # check to see if playlist or music file is selected
    if ( int( _S_( "trivia_music" ) ) == 1 ):
        if ( _S_( "trivia_music_file" ).endswith(".m3u")):
            playlist_file = open( _S_( "trivia_music_file" ), 'rb')
            saved_playlist = playlist_file.readlines()
            track_info, track_location = parse_playlist( saved_playlist, xbmc.getSupportedMedia('music') )
        elif ( os.path.splitext( _S_( "trivia_music_file" ) )[1] in xbmc.getSupportedMedia('music') ):
            count = 0
            for count in range(100):
                track_location.append( _S_( "trivia_music_file" ) )
    # otherwise
    else:
        if ( _S_( "trivia_music_folder" ) ):
            # search given folder and subfolders for files
            track_location = dirEntries( _S_( "trivia_music_folder" ), "music", "TRUE" )
    # shuffle playlist
    count = 0
    while count <6:
        shuffle( track_location, random )
        count=count+1
    for track in track_location:
        music_playlist.add( track,  )
