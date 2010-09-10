""" XBMC Lyrics """

import sys
import os
import xbmc
import xbmcgui

try:
    import xbmcaddon
except:
    # get xbox compatibility module
    from resources.lib.xbox import *
    xbmcaddon = XBMCADDON()

from threading import Timer
from resources.lib.song import Song


class XBMCPlayer( xbmc.Player ):
    """ 
        Subclass of XBMC Player class.
        Overrides onplayback events, for custom actions.
    """
    # visualisation window for setting lyrics properties
    WINDOW = xbmcgui.Window( 12006 )
    # Addon class
    Addon = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )
    # control id's
    CONTROL_LIST = 110
    CONTROL_SAVE_LYRICS = 606

    def __init__( self, *args, **kwargs ):
        # init Player class
        xbmc.Player.__init__( self )
        # passing "{windowId}" from RunScript() means run in background
        self.use_gui = len( sys.argv ) == 1
        # log started action
        self._log_addon_action( "started" )
        # initialize timer
        self.timer = None
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

    def _handle_onplayback_event( self, event ):
        # cancel any timer
        self.cancel_timer()
        # log event
        xbmc.log( "XBMCPlayer::_handle_onplayback_event (event=%s)" % ( event, ), xbmc.LOGDEBUG )
        # on song change fetch lyrics
        if ( event == "started" ):
            # do we have any unsaved tagged lyrics
            if ( self.use_gui ):
                self.gui.save_user_tagged_lyrics( ask=True )
            # set fetching lyrics message
            self._set_properties( message=self.Addon.getLocalizedString( 30800 ) )
            # necessary for xbmc to catch up
            xbmc.sleep( 100 )
            # fetch lyrics
            self.song.get_song_info()
            # set lyrics and messages
            self._set_properties( self.song.lyrics, self.song.lrc_lyrics, self.song.website, self.song.message, self.song.status, self.song.lyric_tags, self.song.prefetched )
            # prefetch next song
            if ( self.prefetched_song is not None ):
                self.prefetched_song.get_song_info()
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

    def _set_properties( self, lyrics="", lrc_lyrics=False, website="", message="", status=True, tags=list(), prefetched=False ):
        # we set the properties on the visualisation window
        self.WINDOW.setProperty( "Message", message )
        self.WINDOW.setProperty( "Success", str( status ) )
        self.WINDOW.setProperty( "Autoscroll", str( not lrc_lyrics and len( tags ) > 0 ) )
        self.WINDOW.setProperty( "KaraokeMode", str( self.Addon.getSetting( "enable_karaoke_mode" ) == "true" and len( tags ) > 0 and status ) )
        self.WINDOW.setProperty( "AllowTagging", str( self.Addon.getSetting( "enable_karaoke_mode" ) == "true" and self.Addon.getSetting( "lyrics_allow_tagging" ) == "true" and self.use_gui and len( tags ) == 0 and status and lyrics is not None ) )
        # if lyrics is None we only set messages
        if ( lyrics is not None ):
            # set lyrics property for textbox control
            self.WINDOW.setProperty( "Lyrics", lyrics )
            # set informational properties
            self.WINDOW.setProperty( "Website", website )
            self.WINDOW.setProperty( "Prefetched", str( prefetched ) )
            # fill list if karaoke mode is enabled
            self._set_karaoke_lyrics( lyrics, tags )

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
        # no more lyrics
        if ( pos == len( self.lyric_tags ) ): return
        # calculate update time, additional time necessary so one timer event fires per lyric
        update = self.lyric_tags[ pos ] - current + 0.05
        # set new timer
        self.timer = Timer( update, self._update_lyric )
        # start timer
        self.timer.start()

    def cancel_timer( self ):
        # if there's a timer cancel it
        if ( self.timer is not None ):
            self.timer.cancel()

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
