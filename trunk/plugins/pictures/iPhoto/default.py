#!/usr/bin/python

# iPhoto Plugin for XBMC
#
# LICENSE - See the LICENSE file that came with this module
#
# Copyright 2008 by Anoop Menon <d4rk@xbmc.org>
# Thanks to Nuka1195 and JMarshal for assistance in development.

__version__ = "0.01"
__url__     = "http://xbmc.org/"
__license__ = "GPL"
__author__  = "d4rk@xbmc.org"

import sys
import os
import os.path

RESOURCE_PATH = xbmc.translatePath(os.path.join(os.getcwd(), "resources"))
ICONS_PATH = os.path.join(RESOURCE_PATH, "icons")
BASE_URL="plugin://pictures/iPhoto/"
platform = "OS X" # FIXME: add support for Windows
sys.path.append(os.path.join(RESOURCE_PATH, "platform_libraries", platform))

import xbmc
import xbmcgui as gui
import xbmcplugin as plugin
from iphoto_parser import *

DB_PATH = xbmc.translatePath("u:\\plugins\\pictures\\iPhoto\\xbmciphotodb.db") #FIXME
db = IPhotoDB(DB_PATH)

def import_library(filename):
    global db
    db.ResetDB()
    iparser = IPhotoParser(db.AddAlbumNew, db.AddRollNew, db.AddKeywordNew, db.AddMediaNew, 
                           progress_callback)
    try:
        iparser.Parse(filename)
        db.UpdateLastImport()
    except:
        print traceback.print_exc()

def progress_callback(current, max):
    global BASE_URL
    item = gui.ListItem( ">>" )
    plugin.addDirectoryItem(handle = int(sys.argv[1]),
                            url=BASE_URL,
                            listitem = item,
                            isFolder = False)

def get_iphoto_library():
    filename = os.getenv("HOME")+"/Pictures/iPhoto Library/AlbumData.xml"
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

def list_photos_in_event(params):
    global DB,BASE_URL
    rollid = params['rollid']
    media = db.GetMediaInRoll(rollid)
    for (caption, mediapath, thumbpath, originalpath, rating) in media:
        if not mediapath:
            mediapath = originalpath
        if not thumbpath:
            thumbpath = originalpath
        if not caption:
            caption = originalpath
        item = gui.ListItem( caption, thumbnailImage=thumbpath )
        #item.setInfo( type="pictures", infoLabels={ "title":caption } )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url=mediapath,
                                listitem = item,
                                isFolder = False)

def list_events(params):
    global db,BASE_URL
    rollid = 0
    try:
        # if we have an album id, only list tracks in the album
        rollid = params['rollid']
        return list_photos_in_event(params)
    except Exception, e:
        print str(e)
        pass
    rolls = db.GetRolls()
    if not rolls:
        return
    for (rollid, name, thumb, rolldate, count) in rolls:
        item = gui.ListItem( name, thumbnailImage=thumb )
        item.setInfo( type="pictures", infoLabels={ "count": count } )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url=BASE_URL+"?action=events&rollid=%s" % (rollid),
                                listitem = item,
                                isFolder = True)
    return

def list_photos_in_album(params):
    global DB,BASE_URL
    albumid = params['albumid']
    media = db.GetMediaInAlbum(albumid)
    render_media(media)

def list_photos_with_rating(params):
    global DB,BASE_URL
    rating = params['rating']
    media = db.GetMediaWithRating(rating)
    render_media(media)

def list_albums(params):
    global db,BASE_URL
    albumid = 0
    try:
        # if we have an album id, only list tracks in the album
        albumid = params['albumid']
        return list_photos_in_album(params)
    except Exception, e:
        print str(e)
        pass
    albums = db.GetAlbums()
    if not albums:
        return
    for (albumid, name) in albums:
        if name == "Photos":
            continue
        item = gui.ListItem( name )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url=BASE_URL+"?action=albums&albumid=%s" % (albumid),
                                listitem = item,
                                isFolder = True)
    return

def list_ratings(params):
    global db,BASE_URL,ICONS_PATH
    albumid = 0
    try:
        # if we have an album id, only list tracks in the album
        rating = params['rating']
        return list_photos_with_rating(params)
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
    
def render_media(media):
    for (caption, mediapath, thumbpath, originalpath, rating) in media:
        if not mediapath:
            mediapath = originalpath
        if not thumbpath:
            thumbpath = originalpath
        if not caption:
            caption = originalpath
        item = gui.ListItem( caption, thumbnailImage=thumbpath )
        #item.setInfo( type="pictures", infoLabels={ "title":caption } )
        plugin.addDirectoryItem(handle = int(sys.argv[1]),
                                url=mediapath,
                                listitem = item,
                                isFolder = False)

def process_params(params):
    try:
        action = params['action']
    except:
        return root_directory()

    if action == "events":
        return list_events(params)
    elif action == "albums":
        return list_albums(params)
    elif action == "ratings":
        return list_ratings(params)
    elif action == "rescan":
        import_library(get_iphoto_library())
        plugin.endOfDirectory( handle = int(sys.argv[1]), succeeded = False )
        sys.exit(0)

    root_directory()

def root_directory():
    global BASE_URL,ICONS_PATH
    # add the artists entry
    item = gui.ListItem( "Events" )
    item.setInfo( type="Picture", infoLabels={ "Title": "Events" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url=BASE_URL+"?action=events", listitem = item,
                            isFolder = True)

    item = gui.ListItem( "Albums", thumbnailImage=ICONS_PATH+"/albums.png" )
    item.setInfo( type="Picture", infoLabels={ "Title": "Albums" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url=BASE_URL+"?action=albums", listitem = item, 
                            isFolder = True)

    item = gui.ListItem( "Ratings", thumbnailImage=ICONS_PATH+"/star.png" )
    item.setInfo( type="Picture", infoLabels={ "Title": "Ratings" } )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url=BASE_URL+"?action=ratings", listitem = item, 
                            isFolder = True)

    item = gui.ListItem( "<< Import My iPhoto Library >>", thumbnailImage="u:\\plugins\\pictures\\iPhoto\\default.tbn" )
    plugin.addDirectoryItem(handle = int(sys.argv[1]), url=BASE_URL+"?action=rescan", listitem = item, 
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
