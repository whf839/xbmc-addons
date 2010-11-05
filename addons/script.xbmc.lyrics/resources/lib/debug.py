""" debugging module """

__all__ = [ "XBMC", "XBMCGUI", "XBMCPLUGIN", "XBMCADDON" ]

import os
import re


class XBMC:
    LOGDEBUG = 0
    LOGNOTICE = 2
    LOGERROR = 4
    CONFIRMED = False
    REGION = { "datelong": "%A,%B %d, %Y", "time": "%I:%M%S %p", "tempunit": "F", "speedunit": "mph" }
    INFOLABEL = { "System.Date": "Friday, July 2, 2010" }

    class Player:
        @staticmethod
        def getTotalTime():
            return 60

        @staticmethod
        def getTime():
            return 10

    class Keyboard:
        def __init__( self, default, heading, hidden=False ):
            pass

        @staticmethod
        def doModal( autoclose=0 ):
            pass

        @staticmethod
        def isConfirmed():
            # only need to test once
            XBMC.CONFIRMED = not XBMC.CONFIRMED
            return XBMC.CONFIRMED

        @staticmethod
        def getText():
            return "ABBA"

    @staticmethod
    def log( msg, level=0 ):
        print msg

    @staticmethod
    def output( msg, level=0 ):
        print msg

    @staticmethod
    def executebuiltin( function ):
        pass

    @staticmethod
    def sleep( time ):
        pass

    @staticmethod
    def getLanguage():
        return "English"

    @staticmethod
    def getInfoLabel( infotag ):
        return XBMC.INFOLABEL.get( infotag.lower(), "Invalid Id" )

    @staticmethod
    def getCondVisibility( infotag ):
        return True

    @staticmethod
    def getCacheThumbName( path ):
        return "".join( [ char for char in path if char.isalnum() ] )

    @staticmethod
    def translatePath( path ):
        return ""

    @staticmethod
    def getRegion( id ):
        return XBMC.REGION.get( id.lower(), "Invalid Id" )


class XBMCGUI:

    class Window:
        @staticmethod
        def __init__( wId=0 ):
            pass

        @staticmethod
        def doModal():
            pass

        class getControl:
            @staticmethod
            def __init__( controlId ):
                pass

            @staticmethod
            def setLabel( label ):
                print label

            @staticmethod
            def reset():
                pass

            @staticmethod
            def setText( text ):
                print text

    class Dialog:
        @staticmethod
        def select( heading, items, autoclose=0 ):
            return 0

        @staticmethod
        def ok( heading, line1="", line2="", line3="" ):
            print "-" * 50
            print heading
            print "-" * 50
            print line1
            print line2
            print line3
            print "-" * 50

    class DialogProgress:
        @staticmethod
        def iscanceled():
            return False

        @staticmethod
        def close():
            pass

        @staticmethod
        def create( heading, line1="", line2="", line3="" ):
            print "-" * 50
            print heading
            print "-" * 50
            print line1
            print line2
            print line3
            print "-" * 50

        @staticmethod
        def update( percent, line1="", line2="", line3="" ):
            print "%d%%" % ( percent, )

class XBMCPLUGIN:
    pass

class XBMCADDON:
    # dictionary to hold addon info
    INFO = {}
    STRINGS = {}
    SETTINGS = { "primary_scraper": u"LyricsTime", "scraper_lyricwiki_gracenote": u"false", "scraper_lyricsmode": u"false", "scraper_lyricstime": u"false", "scraper_lyrdb": u"false", }

    class Addon:
        def __init__( self, id ):
            # TODO: do we want to use id for anything?
            # get proper cwd of addon
            cwd = self._get_cwd( id )
            # parse addon.xml and set all addon info
            self._set_addon_info( cwd)
            # parse addon.xml and set all addon strings
            self._set_addon_strings( cwd )

        def _get_cwd( self, id ):
            # get current working directory
            cwd = os.getcwd()
            # check if we're at root folder of addon
            if ( not os.path.isfile( os.path.join( cwd, "addon.xml" ) ) ):
                # we're not at root, assume resources/lib/
                cwd = os.path.dirname( os.path.dirname( os.getcwd() ) )
            # return proper cwd
            return cwd

        def _set_addon_info( self, cwd ):
            # get source
            xml = open( os.path.join( cwd, "addon.xml" ), "r" ).read()
            # set addon.xml info into dictionary
            XBMCADDON.INFO[ "id" ], XBMCADDON.INFO[ "name" ], XBMCADDON.INFO[ "version" ], XBMCADDON.INFO[ "author" ] = re.search( "<addon id=\"([^\"]+)\".+?name=\"([^\"]+)\".+?version=\"([^\"]+)\".+?provider-name=\"([^\"]+)\".*?>", xml, re.DOTALL ).groups( 1 )
            XBMCADDON.INFO[ "type" ], XBMCADDON.INFO[ "library" ] = re.search(  "<extension point=\"([^\"]+)\".+?library=\"([^\"]+)\".*?>", xml, re.DOTALL ).groups( 1 )
            # set any metadata
            for metadata in [ "disclaimer", "summary", "description" ]:
                data = re.findall( "<%s(?:.+?lang=\"(?:en|%s)\")?.*?>([^<]*)</%s>" % ( metadata, "en", metadata, ), xml, re.DOTALL )
                if ( data ):
                    XBMCADDON.INFO[ metadata ] = data[ -1 ]
                else:
                    XBMCADDON.INFO[ metadata ] = ""
            # set other info
            XBMCADDON.INFO[ "path" ] = cwd
            XBMCADDON.INFO[ "libpath" ] = os.path.join( cwd, XBMCADDON.INFO[ "library" ] )
            XBMCADDON.INFO[ "icon" ] = os.path.join( cwd, "icon.png" )
            XBMCADDON.INFO[ "fanart" ] = os.path.join( cwd, "fanart.jpg" )
            XBMCADDON.INFO[ "changelog" ] = os.path.join( cwd, "changelog.txt" )
            XBMCADDON.INFO[ "profile" ] = os.path.join( cwd, "profile" )

        def _set_addon_strings( self, cwd ):
            # get source
            xml = open( os.path.join( cwd, "resources", "language", "English", "strings.xml" ), "r" ).read()
            # create dictionary
            XBMCADDON.STRINGS = dict( re.findall( "<string id=\"([^\"]+)\">([^<]+)</string>", xml ) )

        @staticmethod
        def getLocalizedString( id ):
            return XBMCADDON.STRINGS.get( str( id ), "Invalid Id" )

        @staticmethod
        def getSetting( id ):
            return XBMCADDON.SETTINGS.get( id, "" )

        @staticmethod
        def setSetting( id, value ):
            XBMCADDON.SETTINGS[ id ] = value

        @staticmethod
        def openSettings():
            pass

        @staticmethod
        def getAddonInfo( id ):
            return XBMCADDON.INFO[ id.lower() ]


if ( __name__ == "__main__" ):
    xbmc = XBMC()
    xbmcgui = XBMCGUI()
    xbmcplugin = XBMCPLUGIN()
    Addon = XBMCADDON().Addon( "python.debug.module" )
    print Addon.getAddonInfo( "Id" )
    print Addon.getAddonInfo( "Type" )
    print Addon.getAddonInfo( "Author" )
    print Addon.getAddonInfo( "Name" )
    print Addon.getAddonInfo( "Version" )
    print Addon.getAddonInfo( "Summary" )
    print Addon.getAddonInfo( "Disclaimer" )
    print Addon.getAddonInfo( "Description" )
    print Addon.getAddonInfo( "Icon" )
    print Addon.getAddonInfo( "Fanart" )
    print Addon.getAddonInfo( "Changelog" )
    print Addon.getAddonInfo( "Path" )
    print Addon.getAddonInfo( "LibPath" )
    print Addon.getAddonInfo( "Library" )
    print Addon.getAddonInfo( "Profile" )
    print xbmc.getRegion( "datelong" )
    print Addon.getLocalizedString( 30760 )
