"""
    XBMC Trac Changelog script
"""

import os
import sys
try:
    import xbmcgui
    import xbmc
    DEBUG = False
except:
    DEBUG = True
    
import urllib
import re
from xml.sax.saxutils import escape


__scriptname__ = "XBMC Trac Changelog"
__author__ = "nuka1195"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/XBMC%20Trac%20Changelog"
__credits__ = "Team XBMC"
__version__ = "1.0"
__svn_revision__ = 0

resource_path = os.path.join( os.getcwd(), "resources" )


class ChangelogParser:
    # TODO: make these settings
    BASE_URL = "http://xbmc.org/trac/timeline?changeset=on&max=100&daysback=90&format=rss"
    ACTION_EXIT_SCRIPT = ( 9, 10, )

    def __init__( self, *args, **kwargs ):
        self.items = []

    def fetch_changelog( self ):
        try:
            # open socket
            if ( DEBUG and os.path.isfile ( os.path.join( os.getcwd(), "changelog.xml" ) ) ):
                usock = open( os.path.join( os.getcwd(), "changelog.xml" ), "r" )
            else:
                usock = urllib.urlopen( self.BASE_URL )
            #read xml source
            xmlSource = usock.read()
            # close socket
            usock.close()
            # save source for debugging
            if ( DEBUG and not os.path.isfile ( os.path.join( os.getcwd(), "changelog.xml" ) ) ):
                file_object = open( os.path.join( os.getcwd(), "changelog.xml" ), "w" )
                file_object.write( xmlSource )
                file_object.close()
            # parse source
            self._parse_xml_source( xmlSource )
        except Exception, e:
            print str( e )

    def _parse_xml_source( self, xmlSource ):
        regex_items = re.compile( '<item>(.*?)</item>', re.DOTALL )
        regex_revision = re.compile( '<title>Changeset \[([0-9]+)\]: ([^<]+)?</title>' )
        regex_author = re.compile( '<dc:creator>(.*?)</dc:creator>' )
        regex_date = re.compile( '<pubDate>(.*?)</pubDate>' )
        #regex_message = re.compile( '<description>&lt;p&gt;\n(.*?)\n&lt;/p&gt;.*?</description>', re.DOTALL )
        items = regex_items.findall( xmlSource )
        for item in items:
            try:
                revision  = regex_revision.findall( item )[ 0 ]
                author  = escape( regex_author.findall( item )[ 0 ] )
                date  = regex_date.findall( item )[ 0 ]
                #message  = escape( regex_message.findall( item )[ 0 ] )
                self.items += [ ( revision[ 0 ], author, date, revision[ 1 ], ) ]
            except:
                print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

if ( not DEBUG ):
    class GUI( xbmcgui.WindowXML ):
        ACTION_EXIT_SCRIPT = ( 9, 10, )

        def __init__( self, *args, **kwargs ):
            xbmcgui.WindowXML.__init__( self )
            self.dialog = xbmcgui.DialogProgress()
            self.dialog.create( __scriptname__, "Fetching changelog..." )

        def onInit( self ):
            items = self._fetch_changelog()
            self._add_items( items )
            self.dialog.close()

        def _fetch_changelog( self ):
            parser = ChangelogParser()
            parser.fetch_changelog()
            return parser.items

        def _add_items( self, items ):
            xbmcgui.lock()
            try:
                for revision, author, date, message in items:
                    self._add_item( revision, author, date, message )
            except:
                pass
            xbmcgui.unlock()

        def _add_item( self, revision, author, date, message ):
            listitem = xbmcgui.ListItem()
            listitem.setProperty( "revision", revision )
            listitem.setProperty( "author", author )
            listitem.setProperty( "date", date )
            listitem.setProperty( "message", message )
            try:
                self.getControl( 110 ).addItem( listitem )
            except:
                print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

        def onClick( self, controlId ):
            pass

        def onFocus( self, controlId ):
            pass

        def onAction( self, action ):
            try:
                if ( action in self.ACTION_EXIT_SCRIPT ):
                    self.close()
            except:
                print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )

if ( __name__ == "__main__" ):
    if ( not DEBUG ):
        ui = GUI( "script-XBMC_Trac_Changelog-main.xml", os.getcwd(), "Default" )
        ui.doModal()
        del ui
    else:
        parser = ChangelogParser()
        parser.fetch_changelog()
        for item in parser.items:
            print item

