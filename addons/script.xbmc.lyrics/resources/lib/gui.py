""" module for running in gui mode """

import xbmcgui


class GUI( xbmcgui.WindowXMLDialog ):
    # default actions
    ACTION_CLOSE_DIALOG = ( 9, 10, )

    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self )
        # set our Player class
        self.player = kwargs[ "Player" ]
        # we set these for faster performance
        # allow tagging?
        self.allow_tagging = self.player.Addon.getSetting( "lyrics_allow_tagging" ) == "true"
        # tag offset setting
        self.tag_offset = float( self.player.Addon.getSetting( "lyrics_tagging_offset" ) ) / 1000
        # clear gui attributes
        self._clear_gui_attributes()

    def onInit( self ):
        try:
            # grab list control (try catch is necessary in case skinner did not include a list control for karaoke mode)
            self.listcontrol = self.getControl( self.player.CONTROL_LIST )
        except:
            # no control, set to None
            self.listcontrol = None
        # start
        self.player.startup( self.listcontrol )

    def onAction( self, action ):
        # only action is close
        if ( action in self.ACTION_CLOSE_DIALOG ):
            self.close_dialog()

    def onClick( self, controlId ):
        # tag lyric
        if ( controlId == self.player.CONTROL_LIST and self.allow_tagging ):
            self._append_tagged_lyric()
        # save lyrics
        elif ( controlId == self.player.CONTROL_SAVE_LYRICS ):
            self.save_user_tagged_lyrics()

    def onFocus( self, controlId ):
        pass

    def _clear_gui_attributes( self, all=True ):
        # initialize these for tagging
        if ( all ): self.tagged_lyrics = list()
        self.non_lyrics = list()

    def _append_tagged_lyric( self ):
        # get current time
        current = self.player.getTime() + self.tag_offset
        # get current lyric
        lyric = unicode( self.listcontrol.getSelectedItem().getLabel(), "utf-8" )
        # mark as tagged
        self.listcontrol.getSelectedItem().setLabel2( u"\u221A" )
        # select next item
        self.listcontrol.selectItem( self.listcontrol.getSelectedPosition() + 1 )
        # if a non lyric line we don't want to highlight it
        if ( not lyric or lyric.startswith( "[" ) ):
            self.non_lyrics.append( lyric )
        else:
            # format tag
            tag = "[%d:%05.02f]" % ( int( current / 60 ), current % 60, )
            # set any non lyrics with tag
            for non_lyric in self.non_lyrics:
                self.tagged_lyrics.append( tag + non_lyric )
            # reset non lyrics
            self._clear_gui_attributes( False )
            # set current lyric with tag
            self.tagged_lyrics.append( tag + lyric )

    def save_user_tagged_lyrics( self, ask=False ):
        # only save if lyrics were tagged
        if ( self.tagged_lyrics ):
            # show a yes/no dialog if ask
            if ( ask ):
                ok = xbmcgui.Dialog().yesno( self.player.Addon.getAddonInfo( "Name" ), self.player.Addon.getLocalizedString( 30840 ), "", self.player.Addon.getLocalizedString( 30841 ) % ( self.player.song.title, ) )
            # are we go for saving
            if ( not ask or ok ):
                # join together and save lyrics
                self.player.save_user_tagged_lyrics( "\n".join( self.tagged_lyrics ) )
        # clear gui attributes
        self._clear_gui_attributes()

    def close_dialog( self ):
        # cancel any timer events
        self.player.cancel_timer()
        # close dialog
        self.close()
