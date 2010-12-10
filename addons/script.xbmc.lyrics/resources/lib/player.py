## Player module: main module

import sys
import xbmc
import xbmcgui
from threading import Timer
from resources.lib.song import Song


class XBMCPlayer( xbmc.Player ):
    """ 
        Subclass of XBMC Player class.
        Overrides onplayback events, for custom actions.
    """
    # visualisation window for setting lyrics properties
    WINDOW = xbmcgui.Window( 12006 )
    # control id's
    CONTROL_LIST = 110
    CONTROL_SAVE_LYRICS = 606

    def __init__( self, *args, **kwargs ):
        # init Player class
        xbmc.Player.__init__( self )
        # initialize timers
        self.lyric_timer = None
        self.fetch_timer = None
        # passing "<windowId>" from RunScript() means run in background
        self.use_gui = kwargs[ "gui" ]
        # set our Addon class
        self.Addon = kwargs[ "Addon" ]
        # log started action
        self._log_addon_action( "started" )
        # set title & logo
        self._set_addon_info()
        # set user preferences
        self._set_user_preferences()
        # initialize our Song class
        self.song = Song( self.Addon )
        # initialize our prefetched Song class, if user preference; we use a separate instance to avoid all the re-initializing
        self.prefetched_song = None
        if ( self.Addon.getSetting( "prefetch_lyrics" ) == "true" ):
            self.prefetched_song = Song( self.Addon, prefetch=True )
        # start
        if ( self.use_gui ):
            self._start_gui()
        else:
            self._start_background()

    def _log_addon_action( self, action ):
        # log addon info
        xbmc.log( "=" * 80, xbmc.LOGNOTICE )
        xbmc.log( "[ADD-ON] - %s %s! [%s]" % ( self.Addon.getAddonInfo( "Name" ), action, [ "BACKGROUND MODE (window=%s)" % ( sys.argv[ -1 ], ), "GUI MODE" ][ self.use_gui ] ), xbmc.LOGNOTICE )
        xbmc.log( "           Id: %s - Type: %s - Version: %s" % ( self.Addon.getAddonInfo( "Id" ), self.Addon.getAddonInfo( "Type" ), self.Addon.getAddonInfo( "Version" ) ), xbmc.LOGNOTICE )
        xbmc.log( "=" * 80, xbmc.LOGNOTICE )

    def _set_addon_info( self ):
        # set addon logo & name
        self.WINDOW.setProperty( "Addon.Logo", self.Addon.getAddonInfo( "Icon" ) )
        self.WINDOW.setProperty( "Addon.Name", self.Addon.getAddonInfo( "Name" ) )

    def _set_user_preferences( self ):
        # set user preference settings
        self.WINDOW.setProperty( "EnableKaraokeMode", self.Addon.getSetting( "enable_karaoke_mode" ) )

    def _start_gui( self ):
        # import gui module
        from resources.lib.gui import GUI
        # get our gui class
        self.gui = GUI( "custom_script.xbmc.lyrics-gui.xml", self.Addon.getAddonInfo( "Path" ), "default", "720p", Player=self )
        # show dialog
        self.gui.doModal()
        # free memory
        del self.gui

    def _start_background( self ):
        # set to True so script will continue
        self.loop = True
        # set window id
        self.window_id = int( sys.argv[ 1 ] ) + 10000
        # get list control
        try:
            window = xbmcgui.Window( self.window_id )
            listcontrol = window.getControl( self.CONTROL_LIST )
        except:
            listcontrol = None
        # start
        self.startup( listcontrol )
        # loop here to keep script running
        while self.loop:
            # 100 msecs seems like a good number FIXME: play with this
            xbmc.sleep( 100 )

    def startup( self, listcontrol=None ):
        # set listcontrol
        self.listcontrol = [ None, listcontrol ][ self.Addon.getSetting( "enable_karaoke_mode" ) == "true" ]
        # start
        self.onPlayBackStarted()

    def onPlayBackStarted( self ):
        # handle start event
        self._handle_onplayback_event( "started" )

    def onPlayBackResumed( self ):
        # handle resumed event
        self._handle_onplayback_event( "resumed" )

    def onPlayBackPaused( self ):
        # handle paused event
        self._handle_onplayback_event( "paused" )

    def onPlayBackStopped( self ):
        # handle stopped event
        self._handle_onplayback_event( "stopped" )

    def onPlayBackEnded( self ):
        # handle ended event
        self._handle_onplayback_event( "ended" )

    def onPlayBackSpeedChanged( self ):
        # handle FF/RW event
        self._handle_onplayback_event( "speedchanged" )

    def _handle_onplayback_event( self, event ):
        # cancel any timer
        self.cancel_timers()
        # log event
        xbmc.log( "XBMCPlayer::_handle_onplayback_event (event=%s)" % ( event, ), xbmc.LOGDEBUG )
        # on song change fetch lyrics
        if ( event == "started" ):
            # do we have any unsaved tagged lyrics
            if ( self.use_gui ):
                self.gui.save_user_tagged_lyrics( ask=True )
            # set new timer (we use this incase user is skipping thru songs)
            self.fetch_timer = Timer( float( self.Addon.getSetting( "fetch_lyrics_delay" ) ) / 1000, self._fetch_lyrics )
            # start timer
            self.fetch_timer.start()
        # on resume from FF/RW we need to reset any timers
        elif ( event == "resumed" ):
            # update lyric if karaoke mode is enabled
            self._update_lyric()
        # on pause?
        elif ( event == "paused" ):
            pass
        # if music has ended we want to clear lyrics
        elif ( event in [ "stopped", "ended" ] ):
            # give time for xbmc in case a glitch in a song fired the event (only seems to happen with crossfading enabled)
            xbmc.sleep( 300 )
            # if we're still playing continue
            if ( self.isPlayingAudio() ): return
            # do we have any unsaved tagged lyrics
            if ( self.use_gui ):
                self.gui.save_user_tagged_lyrics( ask=True )
            # clear existing properties
            self._set_properties()
            # close dialog
            if ( self.use_gui ):
                # close the python gui
                self.gui.close_dialog()
            else:
                # set to False so script will exit
                self.loop = False
                # close window
                xbmc.executebuiltin( "Dialog.Close(%d)" % ( self.window_id, ) )
            # log ended action
            self._log_addon_action( "ended" )
        # on speedchanged?
        elif ( event == "speedchanged" ):
            pass

    def _set_properties( self, lyrics="", tags=list(), lrc_lyrics=False, message="", website="", status=True, prefetched=False ):
        # set informational properties
        self._set_info_properties( message, website, status, prefetched )
        # we set the properties on the visualisation window
        self.WINDOW.setProperty( "Autoscroll", str( not lrc_lyrics and len( tags ) > 0 ) )
        self.WINDOW.setProperty( "KaraokeMode", str( self.Addon.getSetting( "enable_karaoke_mode" ) == "true" and len( tags ) > 0 and status ) )
        self.WINDOW.setProperty( "AllowTagging", str( self.Addon.getSetting( "enable_karaoke_mode" ) == "true" and self.Addon.getSetting( "lyrics_allow_tagging" ) == "true" and self.Addon.getSetting( "autoscroll_lyrics" ) == "false" and self.use_gui and len( tags ) == 0 and status and lyrics is not None ) )
        # if lyrics is None we only set messages
        if ( lyrics is not None ):
            # set lyrics property for textbox control
            self.WINDOW.setProperty( "Lyrics", lyrics )
            # fill list if karaoke mode is enabled
            self._set_karaoke_lyrics( lyrics, tags )

    def _set_info_properties( self, message, website="", status=True, prefetched=False, prefetching=False ):
        # set informational properties
        self.WINDOW.setProperty( "Message", message )
        self.WINDOW.setProperty( "Website", website )
        self.WINDOW.setProperty( "Success", str( status ) )
        self.WINDOW.setProperty( "Prefetched", str( prefetched ) )
        self.WINDOW.setProperty( "Prefetching", str( prefetching ) )

    def _set_karaoke_lyrics( self, lyrics, tags ):
        # if no list control or not user preference skip
        if ( self.listcontrol is None or self.Addon.getSetting( "enable_karaoke_mode" ) != "true" or ( not self.use_gui and not xbmc.getCondVisibility( "Window.IsActive(%d)" % ( self.window_id, ) ) ) ): return
        # clear list
        self.listcontrol.reset()
        # we add a title and a blank non lyric so the first lyric isn't highlighted til it's time, only for LRC tagged lyrics
        if ( tags and tags[ 0 ] > 0 ):
            lyrics = "[I] [%s] [/I]\n\n%s" % ( self.song.title, lyrics, )
            tags.insert( 0, tags[ 0 ] ) 
            tags.insert( 0, 0 ) 
        # set tags, we need to use a separate tags variable so we can pass none at end of music
        self.lyric_tags = tags
        # add lyrics
        self.listcontrol.addItems( lyrics.splitlines() )
        # select proper lyric
        self._update_lyric()

    def _update_lyric( self ):
        # if no time tags, return
        if ( not self.isPlayingAudio() or not self.lyric_tags or self.listcontrol is None or self.Addon.getSetting( "enable_karaoke_mode" ) != "true" or ( not self.use_gui and not xbmc.getCondVisibility( "Window.IsActive(%d)" % ( self.window_id, ) ) ) ): return
        # get current time
        current = self.getTime()
        # get position
        pos = [ count for count, tag in enumerate( self.lyric_tags + [ current + 1 ] ) if ( tag > current ) ][ 0 ]
        # select listitem
        self.listcontrol.selectItem( pos - 1 )
        # return if no more lyrics
        if ( pos == len( self.lyric_tags ) ): return
        # calculate update time, additional time necessary to limit the number of repeat timer events
        update = self.lyric_tags[ pos ] - current + 0.02
        # set new timer
        self.lyric_timer = Timer( update, self._update_lyric )
        # start timer
        self.lyric_timer.start()

    def cancel_timers( self ):
        # if there's a timer cancel it
        if ( self.lyric_timer is not None ):
            self.lyric_timer.cancel()
        if ( self.fetch_timer is not None ):
            self.fetch_timer.cancel()

    def _fetch_lyrics( self ):
        # set fetching lyrics message
        self._set_properties( message=self.Addon.getLocalizedString( 30800 ) % ( unicode( xbmc.getInfoLabel( "MusicPlayer.Title" ), "UTF-8" ), ) )
        # fetch lyrics
        self.song.get_song_info()
        # set lyrics and messages
        self._set_properties( self.song.lyrics, self.song.lyric_tags, self.song.lrc_lyrics, self.song.message, self.song.website, self.song.status, self.song.prefetched )
        # prefetch next song
        if ( self.prefetched_song is not None and xbmc.getCondVisibility( "MusicPlayer.HasNext" ) ):
            # set new timer FIXME: is 10 seconds a good time?
            self.fetch_timer = Timer( 10, self._prefetch_lyrics, ( self.song.message, self.song.website, self.song.status, self.song.prefetched, ) )
            # start timer
            self.fetch_timer.start()

    def _prefetch_lyrics( self, message, website, status, prefetched ):
        # set prefetching message
        self._set_info_properties( message=self.Addon.getLocalizedString( 30805 ) % ( unicode( xbmc.getInfoLabel( "MusicPlayer.Offset(1).Title" ), "UTF-8" ), ), status=status, prefetching=True )
        # fetch next songs lyrics
        self.prefetched_song.get_song_info()
        # set previous properties
        self._set_info_properties( message, website, status, prefetched )

    def save_user_tagged_lyrics( self, lyrics ):
        # set default saved lyrics message
        self.song.message = self.Addon.getLocalizedString( 30863 )
        # set song's lyrics
        self.song.lyrics = lyrics
        # save lyrics
        self.song.Lyrics.save_lyrics( self.song )
        # set new message
        self._set_properties( lyrics=None, message=self.song.message )


if ( __name__ == "__main__" ):
    # start callback class
    XBMCPlayer( xbmc.PLAYER_CORE_PAPLAYER )
