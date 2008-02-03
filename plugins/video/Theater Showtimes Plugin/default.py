"""
Showtimes plugin/windowxml hybrid to fetch movie showtimes and IMDb info

Nuka1195
"""

# Script constants
__plugin__ = "Theater Showtimes Plugin"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/video/Theater%20Showtimes%20Plugin"
__credits__ = "Team XBMC/Jezz_X"
__version__ = "1.0"
__svn_revision__ = 0

#main imports
import sys
import os

import xbmc
import xbmcgui
import xbmcplugin

from random import randrange

from showtimesAPI import IMDbClient
from pysqlite2 import dbapi2 as sqlite

import traceback


class GUI( xbmcgui.WindowXML ):
    # we need to store the strings as they do not exists after the call to endOfDirector()
    # main strings
    strings = {}
    for stringId in range( 30000, 30029 ):
        strings[ stringId ] = xbmc.getLocalizedString( stringId )
    # error message strings
    for stringId in range( 30100, 30102 ):
        strings[ stringId ] = xbmc.getLocalizedString( stringId )

    # end the directory (failed) since this does not fill a media list
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=False )

    # action button codes
    CANCEL_DIALOG = ( 247, 275, 61467, )
    THEATER_LIST = ( 216, 257, 61448, )

    # control constants
    CONTROL_TITLE_LABEL = 10
    CONTROL_INFO_LIST = 100
    CONTROL_INFO_LIST_SCROLLBAR = 101
    CONTROL_INFO_LABEL1 = 200
    CONTROL_INFO_LABEL2 = 201
    CONTROL_INFO_LABEL3 = 202
    CONTROL_INFO_LABEL4 = 203
    CONTROL_BUTTON_PLOT = 401
    CONTROL_BUTTON_DETAILS = 402
    CONTROL_BUTTON_CAST = 403
    CONTROL_BUTTON_OTHER = 404
    CONTROL_INFO_PLOT = 301
    CONTROL_INFO_DETAILS = 302
    CONTROL_INFO_CAST = 303
    CONTROL_INFO_OTHER = 304
    
    CONTROL_BUTTON_TRAILER = 500

    # play trailer search query
    TRAILER_SQL = "SELECT * FROM movies WHERE movies.title LIKE ?;"

    def __init__( self, *args, **kwargs ):
        #xbmcgui.lock()
        self.startup = True
        self._get_settings()
        self._get_scraper()
        self._get_imdb_fetcher()
        #xbmcgui.unlock()

    def onInit( self ):
        if ( self.startup ):
            self.startup = False
            self._set_controls_labels()
            # set the play trailer buttons status
            self._set_trailer_button()
            self._show_dialog()
            self._show_info( self.CONTROL_BUTTON_PLOT )

    def _set_controls_labels( self ):
        self.getControl( self.CONTROL_TITLE_LABEL ).setLabel( self.strings[ 30000 ] )
        self.getControl( self.CONTROL_BUTTON_PLOT ).setLabel( self.strings[ 30013 ] )
        self.getControl( self.CONTROL_BUTTON_DETAILS ).setLabel( self.strings[ 30014 ] )
        self.getControl( self.CONTROL_BUTTON_CAST ).setLabel( self.strings[ 30015 ] )
        self.getControl( self.CONTROL_BUTTON_OTHER ).setLabel( self.strings[ 30016 ] )

    def _get_settings( self ):
        self.settings = {}
        self.settings[ "local" ] = xbmcplugin.getSetting( "local" )
        self.settings[ "scraper" ] = xbmcplugin.getSetting( "scraper" )
        self.settings[ "day" ] = int( xbmcplugin.getSetting( "day" ) )
        self.settings[ "autoshow" ] = xbmcplugin.getSetting( "autoshow" ) == "true"
        self.settings[ "trailer" ] = xbmcplugin.getSetting( "trailer" ) == "true"
        self.settings[ "amt_db_path" ] = xbmcplugin.getSetting( "amt_db_path" )
        self.settings[ "quality" ] = int( xbmcplugin.getSetting( "quality" ) )
        self.settings[ "only_hd" ] = xbmcplugin.getSetting( "only_hd" ) == "true"
        self.settings[ "play_all" ] = xbmcplugin.getSetting( "play_all" ) == "true"
        self.theater_list = {}

    def _get_scraper( self ):
        exec "from showtimesAPI.scrapers.%s import showtimesScraper" % self.settings[ "scraper" ]
        self.ShowtimesFetcher = showtimesScraper.ShowtimesFetcher()

    def _get_imdb_fetcher( self ):
        self.IMDbFetcher = IMDbClient.IMDbFetcher()

    def _show_dialog( self ):
        try:
            self.getControl( self.CONTROL_INFO_LABEL1 ).setLabel( self.strings[ 30001 ] )
            self.getControl( self.CONTROL_INFO_LABEL2 ).setLabel( u"%s: %s" % ( self.strings[ 30005 ], self.settings[ "local" ] ), )
            self.getControl( self.CONTROL_INFO_LABEL3 ).setLabel( u"" )
            self.getControl( self.CONTROL_INFO_LABEL4 ).setLabel( u"" )
            self.getControl( self.CONTROL_INFO_LIST ).reset()
            self.getControl( self.CONTROL_INFO_LIST ).addItem( self.strings[ 30002 ] )
            self._get_theater_list()
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

    def _get_theater_list( self ):
        try:
            if ( not self.theater_list ):
                self.theater_list = self.ShowtimesFetcher.get_theater_list( self.settings[ "local" ] )
            self.movie_showtimes = self.theater_list
            self.imdb = ""
            self._fill_list()
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

    def _get_selection( self, choice ):
        try:
            self.getControl( self.CONTROL_INFO_LABEL1 ).setLabel( choice )
            div1 = ( u"", u" - ", )[ self.movie_showtimes[ choice ].mpaa != "" ]
            div2 = ( u"", u" - ", )[ self.movie_showtimes[ choice ].genre != "" ]
            self.imdb = self.movie_showtimes[ choice ].imdb
            self.getControl( self.CONTROL_INFO_LABEL2 ).setLabel( u"%s%s%s%s%s" % ( self.movie_showtimes[ choice ].duration, div1, self.movie_showtimes[ choice ].mpaa, div2, self.movie_showtimes[ choice ].genre, ) )
            self.getControl( self.CONTROL_INFO_LABEL3 ).setLabel( u"%s:" % self.strings[ 30004 ] )
            self.getControl( self.CONTROL_INFO_LABEL4 ).setLabel( self.movie_showtimes[ choice ].label2 )
            self.getControl( self.CONTROL_INFO_LIST ).reset()
            self.getControl( self.CONTROL_INFO_LIST ).addItem( self.strings[ 30003 ] )
            date, self.movie_showtimes = self.ShowtimesFetcher.get_selection( self.movie_showtimes[ choice ].url, self.settings[ "day" ] )
            self.getControl( self.CONTROL_INFO_LABEL3 ).setLabel( u"%s: %s" % ( self.strings[ 30004 ], date, ) )
            self._fill_list()
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

    def _fill_list( self ):
        try:
            xbmcgui.lock()
            self.getControl( self.CONTROL_INFO_LIST ).reset()
            if ( self.movie_showtimes ):
                self.theaters = self.movie_showtimes.keys()
                self.theaters.sort()
                for count, theater in enumerate( self.theaters ):
                    # fetch movie details
                    info = self._get_details( self.theaters[ count ] )
                    # create our listitem
                    listitem = xbmcgui.ListItem( theater, self.movie_showtimes[ theater ].label2, iconImage="a", thumbnailImage="a" )
                    if ( info is None ):
                        # fill in all the info
                        listitem.setInfo( type="Video", infoLabels={ "Duration": self.movie_showtimes[ theater ].duration, "TVShowTitle": self.movie_showtimes[ theater ].mpaa, "Genre": self.movie_showtimes[ theater ].genre, "Premiered": self.movie_showtimes[ theater ].premiered } )
                    else:
                        if ( info.plot == "" ):
                            info.plot = self.strings[ 30101 ]
                        # set plotoutline to all info that isn't covered by an infolabel
                        other = self._create_other( info )
                        # here we download the thumb and set the value to it's cached filepath
                        listitem.setThumbnailImage( info.poster )
                        # set the infolabels
                        listitem.setInfo( type="Video", infoLabels={ "Title": info.title, "Premiered": self.movie_showtimes[ theater ].premiered, "TVShowTitle": self.movie_showtimes[ theater ].mpaa, "Plot": info.plot, "Duration": info.duration, "MPAA": info.mpaa, "Genre": info.genre, "Director": info.director, "Writer": info.writer, "Studio": info.studio, "Year": info.year, "Rating": info.user_rating, "Votes": info.user_votes, "Tagline": info.tagline, "Cast": info.cast, "Trailer": info.trailer } )
                        # set the other info
                        listitem.setProperty( "OtherInfo", other )
                    self.getControl( self.CONTROL_INFO_LIST ).addItem( listitem )
            else:
                self.getControl( self.CONTROL_INFO_LIST ).addItem( self.strings[ 30006 ] )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        self._fill_cast( self.getControl( self.CONTROL_INFO_LIST ).getListItem( 0 ) )
        xbmcgui.unlock()

    def _get_details( self, choice ):
        info = None
        # initially set our imdb url to the users selection
        imdb = self.movie_showtimes[ choice ].imdb
        # if it was a theater, set it to our stored imdb url
        if ( not imdb ):
            imdb = self.imdb
        if ( imdb ):
            # fetch movie details
            info = self.IMDbFetcher.fetch_info( imdb )
        return info

    def _set_trailer_button( self, trailer=None ):
        # set the play trailer buttons enabled status
        self.getControl( self.CONTROL_BUTTON_TRAILER ).setEnabled( trailer is not None and ( trailer != "" or self.settings[ "trailer" ] ) )
        
    def _fill_cast( self, listitem ):
        xbmcgui.lock()
        # clear the cast list
        self.getControl( self.CONTROL_INFO_CAST ).reset()
        # grab the cast from the main lists listitem, we use this for actor thumbs
        cast = xbmc.getInfoLabel( "Container(100).ListItem.Cast" )
        # if cast exists we fill the cast list
        if ( cast ):
            # we set these class variables for the player
            self.title = xbmc.getInfoLabel( "Container(100).ListItem.Title" )
            self.genre = xbmc.getInfoLabel( "Container(100).ListItem.Genre" )
            self.plot = xbmc.getInfoLabel( "Container(100).ListItem.Plot" )
            self.director = xbmc.getInfoLabel( "Container(100).ListItem.Director" )
            self.year = int( xbmc.getInfoLabel( "Container(100).ListItem.Year" ) )
            self.trailer = xbmc.getInfoImage( "Container(100).ListItem.Trailer" )
            self.thumb = xbmc.getInfoImage( "Container(100).ListItem.Thumb" )
            # we actually use the ListItem.CastAndRole infolabel to fill the list
            role = xbmc.getInfoLabel( "Container(100).ListItem.CastAndRole" ).split( "\n" )
            # enumerate through our cast list and set cast and role
            for count, actor in enumerate( cast.split( "\n" ) ):
                # create the actor cached thumb
                actor_path = xbmc.translatePath( os.path.join( "P:\\Thumbnails", "Video", xbmc.getCacheThumbName( "actor" + actor )[ 0 ], xbmc.getCacheThumbName( "actor" + actor ) ) )
                # if an actor thumb exists use it, else use the default thumb
                actor_thumbnail = ( "DefaultActorBig.png", actor_path, )[ os.path.isfile( actor_path ) ]
                # set the default icon
                actor_icon = "DefaultActorBig.png"
                # add the item to our cast list
                self.getControl( self.CONTROL_INFO_CAST ).addItem( xbmcgui.ListItem( role[ count ], iconImage=actor_icon, thumbnailImage=actor_thumbnail ) )
            # set the play trailer buttons status
            self._set_trailer_button( self.trailer )
        xbmcgui.unlock()

    def _create_other( self, info ):
        # here we set all items that do not have an infolabel, we only set the items that have a value
        other = ""
        if ( info ):
            if ( info.movie_meter ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30018 ], info.movie_meter, )
            if ( info.goofs ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30019 ], info.goofs, )
            if ( info.trivia ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30020 ], info.trivia, )
            if ( info.quotes ):
                other += "[B]%s:[/B]\n" % ( self.strings[ 30021 ], )
                for quote in info.quotes:
                    other += " - %s\n" % ( quote, )
                other += "\n"
            if ( info.user_comments ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30022 ], info.user_comments, )
            if ( info.locations ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30023 ], info.locations, )
            if ( info.aspect_ratio ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30024 ], info.aspect_ratio, )
            if ( info.sound_mix ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30025 ], info.sound_mix, )
            if ( info.language ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30026 ], info.language, )
            if ( info.awards ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30027 ], info.awards, )
            if ( info.certification ):
                other += "[B]%s:[/B] %s\n\n" % ( self.strings[ 30028 ], info.certification, )
        return other

    def _show_info( self, controlId ):
        xbmcgui.lock()
        self.getControl( self.CONTROL_INFO_PLOT ).setVisible( controlId == self.CONTROL_BUTTON_PLOT )
        self.getControl( self.CONTROL_INFO_DETAILS ).setVisible( controlId == self.CONTROL_BUTTON_DETAILS )
        self.getControl( self.CONTROL_INFO_CAST ).setVisible( controlId == self.CONTROL_BUTTON_CAST )
        self.getControl( self.CONTROL_INFO_OTHER ).setVisible( controlId == self.CONTROL_BUTTON_OTHER )
        #self.getControl( self.CONTROL_BUTTON_PLOT ).setEnabled( controlId != self.CONTROL_BUTTON_PLOT )
        #self.getControl( self.CONTROL_BUTTON_DETAILS ).setEnabled( controlId != self.CONTROL_BUTTON_DETAILS )
        #self.getControl( self.CONTROL_BUTTON_CAST ).setEnabled( controlId != self.CONTROL_BUTTON_CAST )
        #self.getControl( self.CONTROL_BUTTON_OTHER ).setEnabled( controlId != self.CONTROL_BUTTON_OTHER )
        xbmcgui.unlock()

    def _play_trailer( self ):
        thumbnail = self.thumb
        trailers = [ self.trailer ]
        if ( self.settings[ "trailer" ] ):
            title = "%"
            for char in self.title:
                if ( not char.isalnum() ):
                    title += "%"
                else:
                    title += char
            title += "%"
            records = Records( db_path=self.settings[ "amt_db_path" ] )
            result = records.fetch( self.TRAILER_SQL, ( title, ) )
            records.close()
            if ( result ):
                trailers = self._get_trailer_url( result[ 0 ], eval( result[ 3 ] ), eval( result[ 13 ] ) )
                # set the thumbnail
                if ( result[ 4 ] and result[ 4 ] is not None ):
                    thumbnail = xbmc.translatePath( os.path.join( "Q:\\UserData", "script_data", "Apple Movie Trailers", ".cache", result[ 4 ][ 0 ], result[ 4 ] ) )
        if ( trailers ):
            # set the default icon
            icon = "DefaultVideo.png"
            # create our playlist
            playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
            # clear any possible entries
            playlist.clear()
            # enumerate thru and add our item
            for count, trailer in enumerate( trailers ):
                # only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
                listitem = xbmcgui.ListItem( self.title, iconImage=icon, thumbnailImage=thumbnail )
                # set the key information
                listitem.setInfo( "video", { "Title": "%s%s" % ( self.title, ( "", " (%s %d)" % ( self.strings[ 30017 ], count + 1, ) )[ len( trailers ) > 1 ], ), "Genre": self.genre, "Director": self.director, "PlotOutline": self.plot, "Year": self.year } )
                # add our item
                playlist.add( trailer, listitem )
            # mark the video watched
            #if ( self.settings[ "mark_watched" ] ):
            #    self._mark_watched()
            # we're finished
            # play the playlist (TODO: when playlist can set the player core, add this back in)
            xbmc.Player().play( playlist )
        else:
            xbmcgui.Dialog().ok( self.strings[ 30000 ], self.strings[ 30100 ] )

    def _get_trailer_url( self, idMovie, trailer_urls, saved_trailers ):
        # pick a random url (only really applies to multiple urls)
        rnd = randrange( len( trailer_urls ) )
        total = rnd + 1
        urls = []
        # if play_all is enabled we want to cycle through all the videos
        if ( self.settings[ "play_all" ] and len( trailer_urls ) > 1 ):
            rnd = 0
            total = len( trailer_urls )
        for count in range( rnd, total ):
            # get intial choice
            choice = ( self.settings[ "quality" ], len( trailer_urls[ count ] ) - 1, )[ self.settings[ "quality" ] >= len( trailer_urls[ count ] ) ]
            # if quality is non progressive
            if ( self.settings[ "quality" ] <= 2 ):
                # select the correct non progressive trailer
                while ( trailer_urls[ count ][ choice ].endswith( "p.mov" ) and choice != -1 ): choice -= 1
            # quality is progressive
            else:
                # select the proper progressive quality
                quality = ( "480p", "720p", "1080p", )[ self.settings[ "quality" ] - 3 ]
                # select the correct progressive trailer
                while ( quality not in trailer_urls[ count ][ choice ] and trailer_urls[ count ][ choice ].endswith( "p.mov" ) and choice != -1 ): choice -= 1
            # if there was a valid trailer set it
            if ( choice >= 0 and ( not self.settings[ "only_hd" ] or self.settings[ "quality" ] < 4 or ( self.settings[ "only_hd" ] and self.settings[ "quality" ] > 3 and ( "720p.mov" in trailer_urls[ count ][ choice ] or "1080p.mov" in trailer_urls[ count ][ choice ] ) ) ) ):
                urls += [ trailer_urls[ count ][ choice ] ]
        # sort the urls, same as in main script
        urls.sort()
        # initialize our new list
        url_list = []
        # enumerate through the urls and check if a saved trailer exists
        for url in urls:
            for trailer in saved_trailers:
                # if a saved trailer with the exact http address exists, use the saved trailer
                if ( url == trailer[ 1 ] ):
                    url = trailer[ 0 ]
                    break
            # add our url to the new list
            url_list += [ url ]
        return url_list

    def _close_dialog( self ):
        self.close()

    def onClick( self, controlId ):
        if ( controlId == self.CONTROL_INFO_LIST ):
            self._get_selection( self.theaters[ self.getControl( controlId ).getSelectedPosition() ] )
        elif ( controlId in ( self.CONTROL_BUTTON_PLOT, self.CONTROL_BUTTON_DETAILS, self.CONTROL_BUTTON_CAST, self.CONTROL_BUTTON_OTHER ) ):
            self._show_info( controlId )
        elif ( controlId == self.CONTROL_BUTTON_TRAILER ):
            self._play_trailer()

    def onFocus( self, controlId ):
        xbmc.sleep( 5 )
        self.controlId = self.getFocusId()
        if ( self.settings[ "autoshow" ] and controlId in ( self.CONTROL_BUTTON_PLOT, self.CONTROL_BUTTON_DETAILS, self.CONTROL_BUTTON_CAST, self.CONTROL_BUTTON_OTHER ) ):
            self._show_info( controlId )

    def onAction( self, action ):
        if ( action.getButtonCode() in self.CANCEL_DIALOG ):
            self._close_dialog()
        elif ( action.getButtonCode() in self.THEATER_LIST ):
            self._show_dialog()
        elif ( self.controlId in ( self.CONTROL_INFO_LIST, self.CONTROL_INFO_LIST_SCROLLBAR, ) ):
            self._fill_cast( self.getControl( self.CONTROL_INFO_LIST ).getSelectedItem() )


class Records:
    def __init__( self, *args, **kwargs ):
        self.connect( kwargs[ "db_path" ] )

    def connect( self, db_path ):
        self.db = sqlite.connect( db_path )
        self.cursor = self.db.cursor()
    
    def close( self ):
        self.db.close()
    
    def fetch( self, sql, params=None ):
        try:
            if ( params is not None ): self.cursor.execute( sql, params )
            else: self.cursor.execute( sql )
            retval = self.cursor.fetchone()
        except:
            retval = None
        return retval


if ( __name__ == "__main__" ):
    ui = GUI( "script-%s-main.xml" % ( __plugin__.replace( " ", "_" ), ), os.path.join( os.getcwd().replace( ";", "" ), "resources" ), "Default", False )
    ui.doModal()
    del ui
