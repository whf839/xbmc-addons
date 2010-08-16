""" xbox compatibilty module """

import sys
import os
import xbmc
import re

def _append_module_paths():
    # main modules path
    modulepath = xbmc.translatePath( "special://home/scripts/.modules" )
    # get modules
    modules = os.listdir( modulepath )
    # loop thru and append the lib folder to path
    for module in modules:
        # make full path
        fullpath = os.path.join( modulepath, module, "lib" )
        # only add modules with a lib folder
        # FIXME: will this be the only format? (module.name/lib)
        if ( os.path.isdir( fullpath ) ):
            sys.path.append( fullpath )
# FIXME: do we want to add this directly in xbmc4xbox to match xbmc (this doesn't work properly)
_append_module_paths()

# path of main addon
_path = os.getcwd()
# check if we're at root folder of addon
if ( not os.path.isfile( os.path.join( _path, "addon.xml" ) ) ):
    # we're not at root, assume resources/lib/
    _path = os.path.dirname( os.path.dirname( os.getcwd() ) )

# language method
_L_ = xbmc.Language( _path ).getLocalizedString
# settings method, try catch necessary as not all scripts have settings
try:
    _S_ = xbmc.Settings( _path )
except:
    _S_ = None


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
            # get source
            xml = open( os.path.join( _path, "addon.xml" ), "r" ).read()
            # regex's
            addon_regex = re.compile( "<addon id=\"([^\"]+)\".+?name=\"([^\"]+)\".+?version=\"([^\"]+)\".+?provider-name=\"([^\"]+)\".*?>", re.DOTALL )
            metadata_type_regex = re.compile( "<extension point=\"([^\"]+)\".+?library=\"([^\"]+)\".*?>", re.DOTALL )
            metadata_summary_regex = re.compile( "<summary>([^<]*)</summary>", re.DOTALL )
            metadata_disclaimer_regex = re.compile( "<disclaimer>([^<]*)</disclaimer>", re.DOTALL )
            metadata_description_regex = re.compile( "<description>([^<]*)</description>", re.DOTALL )
            # set addon.xml info into dictionary
            XBMCADDON.INFO[ "id" ], XBMCADDON.INFO[ "name" ], XBMCADDON.INFO[ "version" ], XBMCADDON.INFO[ "author" ] = addon_regex.search( xml ).groups( 1 )
            XBMCADDON.INFO[ "type" ] = metadata_type_regex.search( xml ).group( 1 )
            XBMCADDON.INFO[ "summary" ] = metadata_summary_regex.search( xml ).group( 1 )
            XBMCADDON.INFO[ "disclaimer" ] = metadata_disclaimer_regex.search( xml ).group( 1 )
            XBMCADDON.INFO[ "description" ] = metadata_description_regex.search( xml ).group( 1 )
            # set other info
            XBMCADDON.INFO[ "path" ] = _path
            XBMCADDON.INFO[ "icon" ] = os.path.join( _path, "default.tbn" )
            XBMCADDON.INFO[ "fanart" ] = os.path.join( _path, "fanart.jpg" )
            XBMCADDON.INFO[ "changelog" ] = os.path.join( _path, "changelog.txt" )
            if ( _path.startswith( "Q:\\plugins" ) and not _path.startswith( "Q:\\plugins\\weather" ) ):
                XBMCADDON.INFO[ "profile" ] = "special://profile/plugin_data/%s/%s" % ( os.path.basename( os.path.dirname( _path ) ), os.path.basename( _path ), )
            else:
                XBMCADDON.INFO[ "profile" ] = "special://profile/script_data/%s" % ( os.path.basename( _path ), )

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
