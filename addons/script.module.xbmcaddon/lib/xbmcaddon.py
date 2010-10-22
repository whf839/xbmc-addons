## xbmcaddon emulator module for xbmc4xbox

__all__ = [ "Addon" ]
__author__ = "nuka1195"

import os
import xbmc
import re
import locale

# get current working directory
cwd = os.getcwd()
# check if we're at root folder of addon
if ( not os.path.isfile( os.path.join( cwd, "addon.xml" ) ) ):
    # we're not at root, assume resources/lib/
    cwd = os.path.dirname( os.path.dirname( os.getcwd() ) )

# language module
_language_ = xbmc.Language( cwd ).getLocalizedString
# settings module, try catch necessary as not all scripts have settings
try:
    _settings_ = xbmc.Settings( cwd )
except:
    _settings_ = None


class Addon:
    """
        Addon(id) -- Creates a new Addon class.

        id          : string - id of the addon.

        example:
         - self.Addon = xbmcaddon.Addon(id="script.xbmc.lyrics")
    """
    # dictionary to hold addon info
    _info = {}
    
    def __init__( self, id ):
        """
            Initializer for passing the addon's id and setting addon info.
            Currently id is not used for xbmc4xbox.
        """
        # TODO: do we want to use id for anything?
        # parse addon.xml and set all addon info
        self._set_addon_info( id )

    def _set_addon_info( self, id ):
        # get source
        xml = open( os.path.join( cwd, "addon.xml" ), "r" ).read()
        # set addon.xml info into dictionary
        self._info[ "id" ], self._info[ "name" ], self._info[ "version" ], self._info[ "author" ] = re.search( "<addon.+?id=\"([^\"]+)\".+?name=\"([^\"]+)\".+?version=\"([^\"]+)\".+?provider-name=\"([^\"]+)\".*?>", xml, re.DOTALL ).groups( 1 )
        self._info[ "type" ], self._info[ "library" ] = re.search( "<extension.+?point=\"([^\"]+)\".+?library=\"([^\"]+)\".*?>", xml, re.DOTALL ).groups( 1 )
        # reset this to default.py as that's what xbox uses
        self._info[ "library" ] = "default.py"
        # set any metadata
        for metadata in [ "disclaimer", "summary", "description" ]:
            data = re.findall( "<%s(?:.+?lang=\"(?:en|%s)\")?.*?>([^<]*)</%s>" % ( metadata, locale.getdefaultlocale()[ 0 ][ : 2 ], metadata, ), xml, re.DOTALL )
            if ( data ):
                self._info[ metadata ] = data[ -1 ]
            else:
                self._info[ metadata ] = ""
        # set other info
        self._info[ "path" ] = cwd
        self._info[ "libpath" ] = os.path.join( cwd, self._info[ "library" ] )
        self._info[ "icon" ] = os.path.join( cwd, "default.tbn" )
        self._info[ "fanart" ] = os.path.join( cwd, "fanart.jpg" )
        self._info[ "changelog" ] = os.path.join( cwd, "changelog.txt" )
        if ( cwd.startswith( "Q:\\plugins" ) and not cwd.startswith( "Q:\\plugins\\weather" ) ):
            self._info[ "profile" ] = "special://profile/plugin_data/%s/%s" % ( os.path.basename( os.path.dirname( cwd ) ), os.path.basename( cwd ), )
        else:
            self._info[ "profile" ] = "special://profile/script_data/%s" % ( os.path.basename( cwd ), )

    def getAddonInfo( self, id ):
        """
            getAddonInfo(id) -- Returns the value of an addon property as a string.

            id        : string - id of the property you want returned.

            *values for id: author, changelog, description, disclaimer, fanart. icon, id, libpath,
                            library, name, path, profile, stars, summary, type, version

            example:
              - profile_path = self.Addon.getAddonInfo(id="profile")
        """
        return self._info[ id.lower() ]

    @staticmethod
    def getLocalizedString( id ):
        """
            getLocalizedString(id) -- Returns the localized string as a unicode object.

            id             : integer - id# of the string you want to localize.

            example:
              - locstr = self.Addon.getLocalizedString(id=30000)
        """
        return _language_( id )

    @staticmethod
    def getSetting( id ):
        """
            getSetting(id) -- Returns the value of a setting as a unicode object.

            id        : string - id of the setting you want returned.

            example:
              - username = self.Addon.getSetting(id="username")
        """
        return _settings_.getSetting( id )

    @staticmethod
    def setSetting( id, value ):
        """
            setSetting(id, value) -- Sets a setting for this addon.

            id        : string - id of the setting you want to set.
            value     : string or unicode - value of the setting.

            example:
              - self.Addon.setSetting(id="username", value="nuka1195")
        """
        _settings_.setSetting( id, value )

    @staticmethod
    def openSettings():
        """
            openSettings() -- Opens this addons settings dialog.

            example:
              - self.Addon.openSettings()
        """
        _settings_.openSettings()
