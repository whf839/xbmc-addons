## Viewer module

import xbmc
import xbmcgui
import re


class Viewer:
    """
        Viewer class: for viewing changelog, readme, license...
    """
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__( self, *args, **kwargs ):
        # activate the text viewer window
        xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
        # get window
        window = xbmcgui.Window( self.WINDOW )
        # set our Addon class
        self.Addon = kwargs[ "Addon" ]
        # give window time to initialize
        xbmc.sleep( 100 )
        # set message
        msg = { "updates": 30760, "changelog": 30761, "readme": 30762, "license": 30763, "properties": 30764 }[ kwargs[ "kind" ] ]
        # set heading
        window.getControl( self.CONTROL_LABEL ).setLabel( "%s - %s" % ( self.Addon.getLocalizedString( msg + 5 ), self.Addon.getAddonInfo( "Name" ), ) )
        # set fetching message
        window.getControl( self.CONTROL_TEXTBOX ).setText( self.Addon.getLocalizedString( msg ) )
        # fetch correct info
        try:
            if ( kwargs[ "kind" ] in [ "readme", "license" ] ):
                text = self._fetch_text_file( kwargs[ "kind" ] )
            elif ( kwargs[ "kind" ] in [ "updates", "changelog" ] ):
                text = self._fetch_changelog( kwargs[ "kind" ] )
            #elif ( kwargs[ "kind" ] == "properties" ):
            #    text = self._fetch_properties()
        except Exception, e:
            # set error message
            text = "%s[CR][CR]%s" % ( self.Addon.getLocalizedString( 30771 ) % ( self.Addon.getLocalizedString( msg + 5 ), ), e, )
        # set text
        window.getControl( self.CONTROL_TEXTBOX ).setText( text )

    def _fetch_text_file( self, kind ):
        # import required modules
        import os
        # set path, first try translated version
        _path = os.path.join( self.Addon.getAddonInfo( "Path" ), "%s-%s.txt" % ( kind, xbmc.getRegion( "locale" ), ) )
        # if doesn't exist, use default
        if ( not os.path.isfile( _path ) ):
            _path = os.path.join( self.Addon.getAddonInfo( "Path" ), "%s.txt" % ( kind, ) )
        # read  file
        text = open( _path, "r" ).read()
        # return text
        return text

    def _fetch_changelog( self, kind ):
        # import required modules
        import datetime
        import pysvn
        # get our regions format
        date_format = "%s %s" % ( xbmc.getRegion( "datelong" ), xbmc.getRegion( "time" ), )
        # get client
        client = pysvn.Client()
        client.callback_cancel = self._pysvn_cancel_callback
        try:
            # grab current revision and repo url
            info = client.info( path=self.Addon.getAddonInfo( "Path" ) )
            # fetch changelog for current revision
            if ( kind == "changelog" ):
                log = client.log( url_or_path=info[ "url" ], limit=25, revision_start=pysvn.Revision( pysvn.opt_revision_kind.number, info[ "commit_revision" ].number ) )
            # updates
            else:
                log = client.log( url_or_path=info[ "url" ], limit=25, revision_end=pysvn.Revision( pysvn.opt_revision_kind.number, info[ "commit_revision" ].number + 1 ) )
        except:
            # changelog
            log = client.log( url_or_path="http://xbmc-addons.googlecode.com/svn/addons/%s" % ( self.Addon.getAddonInfo( "Id" ), ), limit=25 )
        # if no entries set user message
        if ( len( log ) ):
            # initialize our log variable
            changelog = "%s\n" % ( "-" * 150, )
        else:
            # should only happen for "updates" and there are none
            changelog = self.Addon.getLocalizedString( 30704 )
        # we need to compile so we can add flags
        clean_entry = re.compile( "\[.+?\][\s]+(?P<name>[^\[]+)(?:\[.+)?", re.DOTALL )
        version = re.compile( "(Version.+)", re.IGNORECASE )
        # iterate thru and format each message
        for entry in log:
            # add version
            changelog += "%s\n" % ( version.search( entry[ "message" ] ).group( 1 ), )
            # add heading
            changelog += "r%d - %s - %s\n" % ( entry[ "revision" ].number, datetime.datetime.fromtimestamp( entry[ "date" ] ).strftime( date_format ), entry[ "author" ], )
            # add formatted message
            changelog += "\n".join( [ re.sub( "(?P<name>^[a-zA-Z])", "- \\1", line.lstrip( " -" ) ) for line in entry[ "message" ].strip().splitlines() if ( not line.startswith( "[" ) ) ] )
            # add separator
            changelog += "\n%s\n" % ( "-" * 150, )
        # return colorized result
        return self._colorize_text( changelog )

    def _pysvn_cancel_callback( self ):
        # check if user cancelled operation
        return False

    def _colorize_text( self, text ):
        # format text using colors
        text = re.sub( "(?P<name>Version:.+)[\r\n]+", "[COLOR FFEB9E17]\\1[/COLOR]\n\n", text )
        text = re.sub( "(?P<name>r[0-9]+ - .+?)(?P<name2>[\r\n]+)", "[COLOR FF0084FF]\\1[/COLOR]\\2", text )
        text = re.sub( "(?P<name>http://[\S]+)", "[COLOR FFEB9E17]\\1[/COLOR]", text )
        text = re.sub( "(?P<name>[^\]]r[0-9]+)", "[COLOR FFEB9E17]\\1[/COLOR]", text )
        text = re.sub( "(?P<name>\".+?\")", "[COLOR FFEB9E17]\\1[/COLOR]", text )
        text = re.sub( "(?P<name>[A-Z ]+:)[\r\n]+", "[COLOR FF0084FF][B]\\1[/B][/COLOR]\n", text )
        text = re.sub( "(?P<name> - )", "[COLOR FFFFFFFF]\\1[/COLOR]", text )
        text = re.sub( "(?P<name>-[-]+)", "[COLOR FFFFFFFF]\\1[/COLOR]", text )
        # return colorized text
        return text
