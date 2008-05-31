"""
    Player module: plays the selected video
"""

import sys

# TODO: copy thumb if saving trailer
# TODO: we may need to store these in the addContextMenuItem() call, when using a mouse, if the user
# moves, before this module can be imported the selection can change.
# TODO: remove this when dialog issue is resolved
import xbmc
# set our title
g_title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
# set our studio (only works if the user is using the video library)
g_studio = unicode( xbmc.getInfoLabel( "ListItem.Studio" ), "utf-8" )
# set our studio (only works if the user is using the video library)
g_director = unicode( xbmc.getInfoLabel( "ListItem.Director" ), "utf-8" )
# set our genre (only works if the user is using the video library)
g_genre = unicode( xbmc.getInfoLabel( "ListItem.Genre" ), "utf-8" )
# set our rating (only works if the user is using the video library)
g_mpaa_rating = unicode( xbmc.getInfoLabel( "ListItem.MPAA" ), "utf-8" )
# set our thumbnail
g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
# set our plotoutline
g_plotoutline = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
# set movie url
g_movie_url = xbmc.getInfoLabel( "ListItem.FilenameAndPath" )

# create the progress dialog (we do it here so there is minimal delay with nothing displayed)
import xbmcgui
pDialog = xbmcgui.DialogProgress()
pDialog.create( sys.modules[ "__main__" ].__plugin__ )

import os
import xbmcplugin
import urllib


class Main:
    def __init__( self ):
        # get user preferences
        self._get_settings()
        # download the video
        filepath = self._download_video()
        # play the video
        self._play_video( filepath )

    def _get_settings( self ):
        self.settings = {}
        self.settings[ "download_mode" ] = int( xbmcplugin.getSetting( "download_mode" ) )
        self.settings[ "download_path" ] = xbmcplugin.getSetting( "download_path" )

    def _download_video( self ):
        try:
            # parse the extension
            ext = os.path.splitext( g_movie_url )[ 1 ]
            # if download_mode is temp, then download to cache folder
            if ( self.settings[ "download_mode" ] == 0 ):
                self.filepath = xbmc.translatePath( "Z:\\%s" % ( os.path.basename( g_movie_url ), ) )
            else:
                # get a valid filepath
                self.filepath = self._make_legal_filepath( g_title + ext )
            # only download if the trailer doesn't exist
            if ( not os.path.isfile( self.filepath ) ):
                # fetch the video
                urllib.urlretrieve( g_movie_url, self.filepath, self._report_hook )
            return self.filepath
        except:
            # filepath is not always released immediately, we may need to try more than one attempt, sleeping between
            urllib.urlcleanup()
            remove_tries = 3
            while remove_tries and os.path.isfile( self.filepath ):
                try:
                    os.remove( self.filepath )
                except:
                    remove_tries -= 1
                    xbmc.sleep( 1000 )
            pDialog.close()
            return ""

    def _report_hook( self, count, blocksize, totalsize ):
        percent = int( float( count * blocksize * 100) / totalsize )
        msg1 = xbmc.getLocalizedString( 30500 + self.settings[ "download_mode" ]  ) % ( os.path.split( self.filepath )[ 0 ], )
        msg2 = ( "", xbmc.getLocalizedString( 30502 ) % ( os.path.split( self.filepath )[ 1 ], ), )[ self.settings[ "download_mode" ] ]
        pDialog.update( percent, msg1, msg2 )
        if ( pDialog.iscanceled() ): raise

    def _make_legal_filepath( self, title ):
        import re
        # different os's have different illegal characters
        illegal_characters = { "xbox": '\\/,*=|<>?;:\"+', "win32": '\\/*|<>?:\"', "Linux": "/", "OS X": "/:" }
        # get the flavor of XBMC
        environment = os.environ.get( "OS", "xbox" )
        # clean the filename
        filename = re.sub( '[%s]' % ( illegal_characters[ environment ], ), "_", title )
        # TODO: maybe change the length to 37 and create a .conf file for xbox
        if ( environment == "xbox" and len( filename ) > 42 ):
            name, ext = os.path.splitext( filename )
            filename = name[ : 42 - len( ext ) ].strip() + ext
        return xbmc.translatePath( os.path.join( self.settings[ "download_path" ], filename ) )

    def _play_video( self, filepath ):
        if ( filepath ):
            # create our playlist
            playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
            # clear any possible entries
            playlist.clear()
            # set the default icon
            icon = "DefaultVideo.png"
            # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
            listitem = xbmcgui.ListItem( g_title, iconImage=icon, thumbnailImage=g_thumbnail )
            # set the key information
            listitem.setInfo( "video", { "Title": g_title, "Genre": g_genre, "Studio": g_studio, "Director": g_director, "MPAA": g_mpaa_rating, "Plotoutline": g_plotoutline } )
            # add item to our playlist
            playlist.add( filepath, listitem )
            # close dialog
            pDialog.close()
            # play item
            xbmc.Player().play( playlist )
