#!/usr/bin/python
# iTunes Plugin for XBMC
#
# LICENSE - See the LICENSE file that came with this module
#
# Copyright 2008 by Anoop Menon <d4rk@xbmc.org>
# Thanks to Nuka1195 and JMarshal for assistance in development.

# TODO:
# 1. Localization
# 2. Album art
# 3. Settings

__version__ = "0.01"
__license__ = "GPL"
__url__     = "http://xbmc.org/"
__author__  = "d4rk@xbmc.org"

import sys
import os
import os.path

RESOURCE_PATH = xbmc.translatePath(os.path.join(os.getcwd(), "resources"))
ICONS_PATH = os.path.join(RESOURCE_PATH, "icons")
BASE_URL="plugin://music/iTunes/"
platform = "OS X" # FIXME: add support for Windows
sys.path.append(os.path.join(RESOURCE_PATH, "platform_libraries", platform))

import xbmc
import xbmcgui as gui
import xbmcplugin as plugin
from itunes_parser import *

DB_PATH = xbmc.translatePath("u:\\plugins\\music\\iTunes\\xbmcitunesdb.db") #FIXME
db = ITunesDB(DB_PATH)

def import_library(filename):
    global db
    db.ResetDB()
    iparser = ITunesParser(db.AddTrackNew, db.AddPlaylistNew, db.SetConfig, progress_callback)
    try:
        iparser.Parse(filename)
        db.UpdateLastImport()
    except:
        print traceback.print_exc()
    db.Commit()

def progress_callback(current, max):
    item = gui.ListItem( ">>" )
    plugin.addDirectoryItem(handle = int(sys.argv[1]),
                            url="plugin://music/iTunes/",
                            listitem = item,
                            isFolder = False)

def get_itunes_library():
    filename = os.getenv("HOME")+"/Music/iTunes/iTunes Music Library.xml"
    return filename

def get_params(paramstring):
    params = {}
    paramstring = str(paramstring).strip()
    paramstring = paramstring.lstrip("?")
    if not paramstring:
        return params
    paramlist = paramstring.split("&")
    for param in paramlist:
        (k,v) = param.split("=")
        params[k] = v
    print params
    return params


def list_albums_by_artist(params):
    global db
    artistid = params['artistid']
    albums = db.GetAlbumsByArtistId(artistid)
    if len(albums) > 0:
        item = gui.ListItem( "<< All tracks by this Artist >>" )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url="plugin://music/iTunes/?action=tracks&artistid=%s" % artistid,
                                listitem = item,
                                isFolder = True)
        for (albumid, album, artistid) in albums:
            item = gui.ListItem( album )
            plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                    url="plugin://music/iTunes/?action=albums&albumid=%s" % albumid,
                                    listitem = item,
                                    isFolder = True)
    else:
        list_tracks(params)
    return
    
def render_tracks(tracks):
    for track in tracks:
        item = gui.ListItem( track['name'] )
        labels={
            "artist": track['artist'],
            "album": track['album'],
            "title": track['name'],
            "genre": track['genre']
            }
        if track['albumtracknumber']:
            labels['tracknumber'] = int(track['albumtracknumber'])
        if track['playtime']:
            labels['duration'] = int(track['playtime'])/1000.0
        item.setInfo( type="music", infoLabels=labels )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url=track['filename'],
                                listitem = item,
                                isFolder = False)

def list_tracks(params):
    global db
    artistid = params['artistid']
    tracks = db.GetTracksByArtist(artistid)
    render_tracks(tracks)
    return

def list_tracks_in_playlist(params):
    global db
    playlistid = params['playlistid']
    tracks = db.GetTracksInPlaylist(playlistid)
    render_tracks(tracks)

def list_tracks_by_album(params):
    global db
    albumid = params['albumid']
    tracks = db.GetTracksInAlbum(albumid)
    render_tracks(tracks)
    return

def list_tracks_in_genre(params):
    global db
    genreid = params['genreid']
    tracks = db.GetTracksInGenre(genreid)
    render_tracks(tracks)
    return

def list_tracks_with_rating(params):
    global db
    tracks = db.GetTracksWithRating(params['rating'])
    render_tracks(tracks)
    return

def list_artists(params):
    global db,ICONS_PATH
    artistid = 0
    try:
        artistid = params['artistid']
        return list_albums_by_artist(params)
    except Exception, e:
        print str(e)
        pass
    artists = db.GetArtists()
    icon = ICONS_PATH+"/artist.png"
    for (artistid,artist) in artists:
        item = gui.ListItem( artist, thumbnailImage=icon )
        #item.setInfo( type="Music", infoLabels={ "Artist": artist } )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url="plugin://music/iTunes/?action=artists&artistid=%s" % artistid,
                                listitem = item,
                                isFolder = True)
    return

def list_playlists(params):
    global db, ICONS_PATH
    playlistid = 0
    try:
        playlistid = params['playlistid']
        return list_tracks_in_playlist(params)
    except Exception, e:
        print str(e)
        pass
    playlists = db.GetPlaylists()
    icon = ICONS_PATH+"/playlist.png"
    for (playlistid, playlist) in playlists:
        item = gui.ListItem( playlist, thumbnailImage=icon )
        # item.setInfo( type="Music" )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url="plugin://music/iTunes/?action=playlists&playlistid=%s" % playlistid,
                                listitem = item,
                                isFolder = True)
    return

def list_albums(params):
    global db, ICONS_PATH
    artistid = 0
    try:
        # if we have an album id, only list tracks in the album
        albumid = params['albumid']
        return list_tracks_by_album(params)
    except Exception, e:
        print str(e)
        pass
    albums = db.GetAlbums()
    if not albums:
        return
    icon = ICONS_PATH+"/albums.png"
    for (albumid, album, artistid) in albums:
        item = gui.ListItem( album, thumbnailImage=icon )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url="plugin://music/iTunes/?action=albums&albumid=%s" % (albumid),
                                listitem = item,
                                isFolder = True)
    return

def list_genres(params):
    global ICONS_PATH, db
    genreid = 0
    try:
        # if we have an genre id, only list tracks in that genre
        genreid = params['genreid']
        return list_tracks_in_genre(params)
    except Exception, e:
        print str(e)
        pass
    genres = db.GetGenres()
    if not genres:
        return
    icon = ICONS_PATH+"/genres.png"
    for (genreid, genre) in genres:
        item = gui.ListItem( genre, thumbnailImage=icon )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url="plugin://music/iTunes/?action=genres&genreid=%s" % (genreid),
                                listitem = item,
                                isFolder = True, totalItems=100)
    return


def list_ratings(params):
    global db,BASE_URL,ICONS_PATH
    albumid = 0
    try:
        # if we have an album id, only list tracks in the album
        rating = params['rating']
        return list_tracks_with_rating(params)
    except Exception, e:
        print str(e)
        pass
    for a in range(1,6):
        rating = "%d star "%a
        item = gui.ListItem( rating, thumbnailImage=ICONS_PATH+"/star%d.png"%a )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url=BASE_URL+"?action=ratings&rating=%d" % (a),
                                listitem = item,
                                isFolder = True)

def process_params(params):
    try:
        action = params['action']
    except:
        return root_directory()

    if action == "artists":
        return list_artists(params)
    elif action == "albums":
        return list_albums(params)
    elif action == "playlists":
        return list_playlists(params)
    elif action == "tracks":
        return list_tracks(params)
    elif action == "genres":
        return list_genres(params)
    elif action == "ratings":
        return list_ratings(params)
    elif action == "rescan":
        import_library(get_itunes_library())
        plugin.endOfDirectory( handle = int(sys.argv[1]), succeeded = False )
        sys.exit(0)

    root_directory()

def root_directory():
    global ICONS_PATH
    # add the artists entry
    item = gui.ListItem( "Artists", thumbnailImage=ICONS_PATH+"/artist.png" )
    item.setInfo( type="Music", infoLabels={ "Title": "Artists" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url="plugin://music/iTunes/?action=artists", listitem = item,
                            isFolder = True)

    item = gui.ListItem( "Albums", thumbnailImage=ICONS_PATH+"/albums.png" )
    item.setInfo( type="Music", infoLabels={ "Title": "Albums" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url="plugin://music/iTunes/?action=albums", listitem = item, 
                            isFolder = True)

    item = gui.ListItem( "Playlists", thumbnailImage=ICONS_PATH+"/playlist.png" )
    item.setInfo( type="Music", infoLabels={ "Title": "Playlists" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url="plugin://music/iTunes/?action=playlists", listitem = item, 
                            isFolder = True)

    item = gui.ListItem( "Genres", thumbnailImage=ICONS_PATH+"/genres.png" )
    item.setInfo( type="Music", infoLabels={ "Title": "Genres" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url="plugin://music/iTunes/?action=genres", listitem = item, 
                            isFolder = True)

    item = gui.ListItem( "Rating", thumbnailImage=ICONS_PATH+"/star.png" )
    item.setInfo( type="Music", infoLabels={ "Title": "Rating" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url="plugin://music/iTunes/?action=ratings", listitem = item, 
                            isFolder = True)

    item = gui.ListItem( "<< Import My iTunes Library >>", thumbnailImage=ICONS_PATH+"/import.png"  )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url="plugin://music/iTunes/?action=rescan", listitem = item, 
                            isFolder = True, totalItems=100)

def main():
    params = sys.argv[2]
    process_params(get_params(params))
    plugin.endOfDirectory( handle = int(sys.argv[1]), succeeded = True )

if __name__=="__main__":
    try:
        main()
    except Exception, e:
        print str(e)
        print traceback.print_exc()
