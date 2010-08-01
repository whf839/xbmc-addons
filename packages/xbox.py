""" xbox compatibilty module """

import xbmc
import os
import re

# language method
_L_ = xbmc.Language( os.getcwd() ).getLocalizedString
# settings method
_S_ = xbmc.Settings( os.getcwd() )


class XBMCADDON:
    """
        xbmcaddon module class
    """
    # dictionary to hold addon info
    INFO = {}

    class Addon:
        """
            Class to emulate xbmcaddon.Addon methods.
        """
        def __init__( self, id ):
            # TODO: do we want to use id for anything?
            # parse addon.xml and set all addon info
            self._set_addon_info( id )

        def _set_addon_info( self, id ):
            # path of main addon
            _path = os.getcwd()
            # get source
            xml = open( os.path.join( _path, "addon.xml" ), "r" ).read()
            # regex's TODO: maybe parse with an xml parser instead of re
            addon_regex = re.compile( "<addon id=\"([^\"]+)\".+?name=\"([^\"]+)\".+?version=\"([^\"]+)\".+?provider-name=\"([^\"]+)\".*?>", re.DOTALL )
            metadata_summary_regex = re.compile( "<summary>([^<]*)</summary>", re.DOTALL )
            metadata_disclaimer_regex = re.compile( "<disclaimer>([^<]*)</disclaimer>", re.DOTALL )
            metadata_description_regex = re.compile( "<description>([^<]*)</description>", re.DOTALL )
            metadata_type_regex = re.compile( "<extension point=\"([^\"]+)\" library=\"([^\"]+)\"/>", re.DOTALL )
            # set addon.xml info into dictionary
            XBMCADDON.INFO[ "id" ], XBMCADDON.INFO[ "name" ], XBMCADDON.INFO[ "version" ], XBMCADDON.INFO[ "author" ] = addon_regex.search( xml ).groups( 1 )
            XBMCADDON.INFO[ "type" ] = metadata_type_regex.search( xml ).group( 1 )
            XBMCADDON.INFO[ "summary" ] = metadata_summary_regex.search( xml ).group( 1 )
            XBMCADDON.INFO[ "disclaimer" ] = metadata_disclaimer_regex.search( xml ).group( 1 )
            XBMCADDON.INFO[ "description" ] = metadata_description_regex.search( xml ).group( 1 )
            # set other info
            XBMCADDON.INFO[ "path" ] = _path
            XBMCADDON.INFO[ "profile" ] = "special://profile/addon_data/%s" % ( os.path.basename( _path ), )
            XBMCADDON.INFO[ "icon" ] = os.path.join( _path, "icon.png" )
            XBMCADDON.INFO[ "fanart" ] = os.path.join( _path, "fanart.jpg" )
            XBMCADDON.INFO[ "changelog" ] = os.path.join( _path, "changelog.txt" )

        @staticmethod
        def getLocalizedString( id ):
            return _L_( id )

        @staticmethod
        def getSetting( id ):
            return _S_.getSetting( id )

        @staticmethod
        def setSetting( id, value ):
            _S_.setSetting( id, value )

        @staticmethod
        def openSettings():
            _S_.openSettings()

        @staticmethod
        def getAddonInfo( id ):
            return XBMCADDON.INFO[ id.lower() ]
