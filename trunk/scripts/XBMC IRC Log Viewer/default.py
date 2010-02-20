# Script constants
__script__ = "XBMC IRC Log Viewer"
__author__ = "nuka1195"
__url__ = ""
__svn_url__ = ""
__credits__ = "Team XBMC/TSlayer"
__version__ = "1.1"
__svn_revision__ = 0

#main imports
import sys
import os

import xbmc
import xbmcgui
import xbmcplugin

import urllib2
import re
from htmllib import HTMLParser


class GUI( xbmcgui.WindowXMLDialog ):
    # base url
    BASE_LOG_URL = "http://xbmc%s.newsforyou.com%s"

    # action button codes
    ACTION_CANCEL_DIALOG = ( 9, 10, )
    ACTION_REFRESH_MESSAGES_LIST = ( 117, )

    CONTROL_LABEL_HEADING = 10
    CONTROL_LIST_LOGS = 100
    CONTROL_LIST_LOGS_SCROLLBAR = 101
    CONTROL_LIST_MESSAGES = 110
    CONTROL_LIST_MESSAGES_SCROLLBAR = 111
    CONTROL_LABEL_LOG_TITLE = 200
    CONTROL_BUTTON_LINUX = 401
    CONTROL_BUTTON_SCRIPTING = 402
    CONTROL_BUTTON_XBMC = 403
    CONTROL_BUTTON_PVR = 404
    CONTROL_RADIOBUTTON_FILTER = 500
    CONTROL_BUTTON_HIGHLIGHT = 501

    def __init__( self, *args, **kwargs ):
        #xbmcgui.lock()
        self.startup = True
        self.selected = -1
        #xbmcgui.unlock()

    def onInit( self ):
        if ( self.startup ):
            self.startup = False
            self._show_dialog()

    def _show_dialog( self ):
        self.domain = ( "logs", "/", )
        self._get_log_list( "#xbmc" )

    def _get_log_list( self, channel ):
        try:
            self.getControl( self.CONTROL_LABEL_HEADING ).setLabel( "%s - (%s)" % ( __script__, channel, ) )
            self.getControl( self.CONTROL_LIST_LOGS ).reset()
            self.getControl( self.CONTROL_LIST_MESSAGES ).reset()
            self.getControl( self.CONTROL_LABEL_LOG_TITLE ).setLabel( "" )
            self.getControl( self.CONTROL_LIST_LOGS ).addItem( "Fetching log list..." )
            xbmcgui.lock()
            htmlSource = self._fetch_info( url=self.BASE_LOG_URL % self.domain )
            log_list = self._parse_list( htmlSource )
            self.getControl( self.CONTROL_LIST_LOGS ).reset()
            for log in log_list:
                # create our listitem
                listitem = xbmcgui.ListItem( log[ 1 ], log[ 0 ] )
                self.getControl( self.CONTROL_LIST_LOGS ).addItem( listitem )
            self.setFocus( self.getControl( self.CONTROL_LIST_LOGS ) )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            self.setFocus( self.getControl( self.CONTROL_BUTTON_XBMC ) )
        xbmcgui.unlock()

    def _get_selection( self, url, date, selected, keep=False ):
        try:
            if ( self.selected >= 0 ):
                self.getControl( self.CONTROL_LIST_LOGS ).getListItem( self.selected ).select( False )
            self.getControl( self.CONTROL_LIST_LOGS ).getListItem( selected ).select( True )
            pos = 0
            if ( keep ):
                pos = self.getControl( self.CONTROL_LIST_MESSAGES ).getSelectedPosition()
            self.getControl( self.CONTROL_LIST_MESSAGES ).reset()
            xbmcgui.lock()
            htmlSource = self._fetch_info( url=self.BASE_LOG_URL % self.domain + url )
            log_date, messages = self._parse_log( htmlSource )
            self.url = url
            self.date = date
            self.selected = selected
            filter_login = xbmc.getInfoLabel( "Skin.HasSetting(IRCLogViewerFilter)" )
            highlight_user = xbmc.getInfoLabel( "Skin.String(IRCLogViewerHighlight)" )
            for message in messages:
                select = False
                # create our listitem
                if ( message[ 2 ].startswith( "color: #" ) ):
                    if ( highlight_user and highlight_user.lower() not in message[ 1 ].lower() and highlight_user.lower() in message[ 3 ].lower() ):
                        select = True
                        formatter = "%s"
                    else:
                        formatter = "[COLOR=FF%s]%%s[/COLOR]" % ( message[ 2 ].split( "color: #" )[ 1 ], )
                    msg = formatter % ( self._clean_text( message[ 3 ] ), )
                    time = formatter % ( message[ 0 ], )
                    user = formatter % ( message[ 1 ], )
                elif ( message[ 1 ].startswith( "Action: " ) ):
                    msg = self._clean_text( message[ 1 ] )
                    time = message[ 0 ]
                    user = message[ 1 ].split( " " )[ 1 ]
                else:
                    if ( filter_login ): continue
                    msg = self._clean_text( message[ 1 ] )
                    time = message[ 0 ]
                    user = message[ 1 ].split( " " )[ 0 ]
                listitem = xbmcgui.ListItem( time, user )
                listitem.setProperty( "Message", msg )
                listitem.select( select )
                self.getControl( self.CONTROL_LIST_MESSAGES ).addItem( listitem )
            if ( self.getControl( self.CONTROL_LIST_MESSAGES ).size() == 0 ):
                listitem = xbmcgui.ListItem( "--:--", "xbmcfaq" )
                listitem.setProperty( "Message", "There are no messages to display!" )
                self.getControl( self.CONTROL_LIST_MESSAGES ).addItem( listitem )
            self.getControl( self.CONTROL_LABEL_LOG_TITLE ).setLabel( date )
            self.setFocus( self.getControl( self.CONTROL_LIST_MESSAGES ) )
            self.getControl( self.CONTROL_LIST_MESSAGES ).selectItem( pos )
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
        xbmcgui.unlock()

    def _clean_text( self, text ):
        try:
            text = text.replace( "&nbsp;", " " )
            text = text.strip()
            parser = HTMLParser( None )
            parser.save_bgn()
            parser.feed( text )
            return parser.save_end()
        except:
            return text

    def _fetch_info( self, url ):
        try:
            # we post the needed authentication request to our uri
            request = urllib2.Request( url )
            # create an opener object to grab the source
            opener = urllib2.build_opener().open( request )
            # read source
            htmlSource = opener.read()
            # close opener
            opener.close()
            # return the htmlSource
            return htmlSource
        except:
            # oops return an empty string
            print "ERROR: %s::%s (%d) - %s" % ( __name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return ""

    def _parse_list( self, htmlSource ):
        pattern = '<li><a href="([^"]*)">([^<]*)</a>'
        logs = re.findall( pattern, htmlSource )
        return logs

    def _parse_log( self, htmlSource ):
        date_pattern = '<h1>([^<]*)</h1>'
        #message_pattern = '<tr id="t([0-9]{2}:[0-9]{2})">[^>]*>([^<]*)<.*?style="color: ([^"]*)">(.*?)</td>'
        message_pattern = '<tr id="t([0-9]{2}:[0-9]{2})">[^>]*>([^<]*)<.*?[style="color: |</td>]([^"]*)">(.*?)</td>'
        log_date = re.findall( date_pattern, htmlSource )[ 0 ]
        messages = re.findall( message_pattern, htmlSource )
        return log_date, messages

    def _get_keyboard( self, default="", heading="", hidden=False ):
        """ shows a keyboard and returns a value """
        keyboard = xbmc.Keyboard( default, heading, hidden )
        keyboard.doModal()
        if ( keyboard.isConfirmed() ):
            return keyboard.getText()
        return default

    def _get_highlight_user( self ):
        old_highlight_user = xbmc.getInfoLabel( "Skin.String(IRCLogViewerHighlight)" )
        new_highlight_user = self._get_keyboard( old_highlight_user, "Highlight User" )
        if ( old_highlight_user != new_highlight_user ):
            xbmc.executebuiltin( "Skin.SetString(IRCLogViewerHighlight,%s)" % ( new_highlight_user, ) )
            self._get_selection( self.url, self.date, self.selected, True )

    def _close_dialog( self ):
        self.close()

    def onClick( self, controlId ):
        if ( controlId == self.CONTROL_LIST_LOGS ):
            self._get_selection( self.getControl( controlId ).getSelectedItem().getLabel2(), self.getControl( controlId ).getSelectedItem().getLabel(), self.getControl( controlId ).getSelectedPosition() )
        elif ( controlId == self.CONTROL_BUTTON_LINUX ):
            self.domain = ( "", "/xbmc-linux/", )
            self._get_log_list( "#xbmc-linux" )
        elif ( controlId == self.CONTROL_BUTTON_SCRIPTING ):
            self.domain = ( "", "/xbmc-scripting/", )
            self._get_log_list( "#xbmc-scripting" )
        elif ( controlId == self.CONTROL_BUTTON_XBMC ):
            self.domain = ( "logs", "/", )
            self._get_log_list( "#xbmc" )
        elif ( controlId == self.CONTROL_BUTTON_PVR ):
            self.domain = ( "", "/xbmc-pvr/", )
            self._get_log_list( "#xbmc-pvr" )
        elif ( controlId == self.CONTROL_RADIOBUTTON_FILTER ):
            self._get_selection( self.url, self.date, self.selected, True )
        elif ( controlId == self.CONTROL_BUTTON_HIGHLIGHT ):
            self._get_highlight_user()

    def onFocus( self, controlId ):
        xbmc.sleep( 5 )
        self.controlId = self.getFocusId()

    def onAction( self, action ):
        if ( action in self.ACTION_CANCEL_DIALOG ):
            self._close_dialog()
        elif ( action in self.ACTION_REFRESH_MESSAGES_LIST and self.date == "Latest (bookmarkable)" ):
            self._get_selection( self.url, self.date, self.selected, True )
            


if ( __name__ == "__main__" ):
    ui = GUI( "script-%s-main.xml" % ( __script__.replace( " ", "_" ), ), os.getcwd(), "Default", False )
    ui.doModal()
    del ui
