# main imports
import os
import xbmcgui
import xbmc

import threading
import binascii
from random import shuffle
import re

_ = xbmc.Language( scriptPath=os.getcwd() ).getLocalizedString


class Trivia( xbmcgui.WindowXML ):
    # special action codes
    ACTION_NEXT_SLIDE = ( 7, )
    ACTION_EXIT_SCRIPT = ( 9, 10, )

    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXML.__init__( self, *args, **kwargs )
        # update dialog
        kwargs[ "dialog" ].update( -1, _( 32510 ) )
        self.settings = kwargs[ "settings" ]
        self.playlist = kwargs[ "playlist" ]
        # initialize our class variable
        self._init_variables()
        # get the slides
        self._get_slides( [ self.settings[ "trivia_path" ] ] )
        # shuffle and format playlist
        self._shuffle_slides()
        # start our trvia quiz timer
        self._get_global_timer( self.settings[ "trivia_total_time" ] * 60, self._exit_trivia)
        # close dialog
        kwargs[ "dialog" ].close()

    def onInit( self ):
        # start slideshow
        self._next_slide()
        # start music
        self._start_music()

    def _init_variables( self ):
        self.global_timer = None
        self.slide_timer = None
        self.exiting = False
        self.current_volume = None
        self.slide_playlist = []
        self.tmp_slides = []
        self.image_count = 0

    def _start_music( self ):
        # did user set this preference
        if ( self.settings[ "trivia_music" ] ):
            # get the current volume
            self.current_volume = int( xbmc.executehttpapi( "GetVolume" ).replace( "<li>", "" ) )
            # calculate the new volume
            volume = self.current_volume * ( float( self.settings[ "trivia_music_volume" ] ) / 100 )
            # set the volume percent of current volume
            xbmc.executebuiltin( "XBMC.SetVolume(%d)" % ( volume, ) )
            # play music
            xbmc.Player().play( self.settings[ "trivia_music" ] )

    def _get_slides( self, paths ):
        # enumerate thru paths and fetch slides recursively
        for path in paths:
            # initialize type variables
            questions = []
            clues = []
            answers = []
            folders = []
            # get the directory listing
            entries = xbmc.executehttpapi( "GetDirectory(%s)" % ( path, ) ).split( "\n" )
            # sort in case
            entries.sort()
            # read slides.xml if available
            slidesxml_exists = ( xbmc.executehttpapi( "FileExists(%sslides.xml)" % ( path, ) ) == "<li>True" )
            if ( slidesxml_exists ):
                # fetch data
                xml_data = binascii.a2b_base64( xbmc.executehttpapi( "FileDownload(%sslides.xml,bare)" % ( path, ) ) )
                # read formats
                question_format = re.findall( "<question format=\"([^\"]+)\" />", xml_data )[ 0 ]
                clue_format = re.findall( "<clue format=\"([^\"]+)\" />", xml_data )[ 0 ]
                answer_format = re.findall( "<answer format=\"([^\"]+)\" />", xml_data )[ 0 ]
            # enumerate through our entries list and separate question, clue, answer
            for entry in entries:
                # remove <li> from item
                entry = entry.replace( "<li>", "" )
                # if folder add to our folder list to recursively fetch slides
                if ( entry.endswith( "/" ) ):
                    folders += [ entry.replace( "<li>", "" ) ]
                # sliders.xml was included, so check it
                elif ( slidesxml_exists ):
                    # question
                    if ( entry.endswith( question_format ) ):
                        questions += [ entry ]
                    # clue
                    elif ( entry.endswith( clue_format ) ):
                        clues += [ entry ]
                    # answer
                    elif ( entry.endswith( answer_format ) ):
                        answers += [ entry ]
                # add the file as a question TODO: maybe check for valid picture format?
                elif ( entry and os.path.splitext( entry )[ 1 ] in xbmc.getSupportedMedia( "picture" ) ):
                    questions += [ entry ]
            # group the appropriate slides into their own list and order them question, clue, answer
            for count, question in enumerate( questions ):
                # reset our list
                slide = []
                # add question (regular slides will be added to questions)
                slide += [ question ]
                # only add clue if it's not blank
                if ( len( clues ) > count ):
                    slide += [ clues[ count ] ]
                # only add answer if it's not blank
                if ( len( answers ) > count ):
                    slide += [ answers[ count ] ]
                # add our slide group
                self.tmp_slides += [ slide ]
        # if there are folders call again (we want recursive)
        if ( folders ):
            self._get_slides( folders )

    def _shuffle_slides( self ):
        # randomize the groups and create our play list
        shuffle( self.tmp_slides )
        # now create our final playlist
        for slide in self.tmp_slides:
            self.slide_playlist += slide

    def _next_slide( self ):
        # if no more slides, exit
        if ( self.image_count == len( self.slide_playlist ) ):
            self._exit_trivia()
        else:
            # cancel timer if it's running
            if ( self.slide_timer is not None ):
                self.slide_timer.cancel()
            # set the property the image control uses
            xbmcgui.Window( xbmcgui.getCurrentWindowId() ).setProperty( "Slide", self.slide_playlist[ self.image_count ] )
            # increment count
            self.image_count += 1
            # start slide timer
            self._get_slide_timer()

    def _get_slide_timer( self ):
        self.slide_timer = threading.Timer( self.settings[ "trivia_slide_time" ], self._next_slide,() )
        self.slide_timer.start()

    def _get_global_timer( self, time, function ):
        self.global_timer = threading.Timer( time, function,() )
        self.global_timer.start()

    def _exit_trivia( self ):
        # notify we are exiting
        self.exiting = True
        # cancel timers
        self._cancel_timers()
        # set the volume back to original
        xbmc.executebuiltin( "XBMC.SetVolume(%d)" % ( self.current_volume, ) )
        # show an end image
        self._show_end_image()

    def _show_end_image( self ):
        # set the end of trivia slide show image
        if ( self.settings[ "trivia_end_image" ] ):
            xbmcgui.Window( xbmcgui.getCurrentWindowId() ).setProperty( "Slide", self.settings[ "trivia_end_image" ] )
            # set a default timeout
            time = self.settings[ "trivia_slide_time" ]
            # play end of slideshow music
            if ( self.settings[ "trivia_end_music" ] ):
                xbmc.Player().play( self.settings[ "trivia_end_music" ] )
                # set time based on how long the song is
                time = xbmc.Player( xbmc.PLAYLIST_MUSIC ).getTotalTime()
            # start a timer to play video playlist
            self._get_global_timer( time, self._play_video_playlist )

    def _play_video_playlist( self ):
        # set this to -1 as True and False are taken
        self.exiting = -1
        # cancel timers
        self._cancel_timers()
        # we play the video playlist here so the screen does not flash
        xbmc.Player().play( self.playlist )
        # close trivia slide show
        self.close()

    def _cancel_timers( self ):
        # cancel all timers
        if ( self.slide_timer is not None ):
            self.slide_timer.cancel()
        if ( self.global_timer is not None ):
            self.global_timer.cancel()

    def onClick( self, controlId ):
        pass

    def onFocus( self, controlId ):
        pass

    def onAction( self, action ):
        if ( action in self.ACTION_EXIT_SCRIPT and not self.exiting ):
            self._exit_trivia()
        elif ( action in self.ACTION_EXIT_SCRIPT and self.exiting is True ):
            self._play_video_playlist()
        elif ( action in self.ACTION_NEXT_SLIDE and not self.exiting ):
            self._next_slide()

