""" Utilities module """

import sys
import os

try:
    import xbmc
    import xbmcgui
    try:
        import xbmcaddon
    except:
        # get xbox compatibility module
        from xbox import *
        xbmcaddon = XBMCADDON()
except:
    # get dummy xbmc modules (Debugging)
    from debug import *
    xbmc = XBMC()
    xbmcgui = XBMCGUI()
    xbmcaddon = XBMCADDON()

# Addon class
Addon = xbmcaddon.Addon( id=os.path.basename( os.path.dirname( os.path.dirname( os.getcwd() ) ) ) )


class Viewer:
    # we need regex for parsing info
    import re
    # window constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__( self, *args, **kwargs ):
        # activate the text viewer window
        xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
        # get window
        window = xbmcgui.Window( self.WINDOW )
        # give window time to initialize
        xbmc.sleep( 100 )
        # set heading
        window.getControl( self.CONTROL_LABEL ).setLabel( "%s - %s" % ( { "updates": Addon.getLocalizedString( 30765 ), "changelog": Addon.getLocalizedString( 30766 ), "readme": Addon.getLocalizedString( 30767 ), "license": Addon.getLocalizedString( 30768 ) }[ kwargs[ "kind" ] ], Addon.getAddonInfo( "Name" ), ) )
        # set fetching message
        window.getControl( self.CONTROL_TEXTBOX ).setText( { "updates": Addon.getLocalizedString( 30760 ), "changelog": Addon.getLocalizedString( 30761 ), "readme": Addon.getLocalizedString( 30762 ), "license": Addon.getLocalizedString( 30763 ) }[ kwargs[ "kind" ] ] )
        # set header
        try:
            # fetch correct info
            if ( kwargs[ "kind" ] in [ "readme", "license" ] ):
                text = self._fetch_text_file( kwargs[ "kind" ] )
            else:
                text = self._fetch_changelog( kwargs[ "kind" ] )
        except Exception, e:
            # set error message
            text = Addon.getLocalizedString( 30770 ) % ( { "updates": Addon.getLocalizedString( 30765 ), "changelog": Addon.getLocalizedString( 30766 ), "readme": Addon.getLocalizedString( 30767 ), "license": Addon.getLocalizedString( 30768 ) }[ kwargs[ "kind" ] ], e, )
        # set text
        window.getControl( self.CONTROL_TEXTBOX ).setText( text )

    def _fetch_text_file( self, kind ):
        # set path, first try translated version
        _path = os.path.join( os.getcwd(), "../../%s-%s.txt" ) % ( kind, xbmc.getLanguage()[ : 2 ].lower(), )
        # if doesn't exist, use default
        if ( not os.path.isfile( _path ) ):
            _path = os.path.join( os.getcwd(), "../../%s.txt" % ( kind, ) )
        # read  file
        text = open( _path, "r" ).read()
        # return colorized result
        return text##self._colorize_text( text )

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
            # get actual addon root dir
            _path = os.path.dirname( os.path.dirname( os.getcwd() ) )
            # grab current revision and repo url
            info = client.info( path=_path )
            # fetch changelog for current revision
            if ( kind == "changelog" ):
                log = client.log( url_or_path=info[ "url" ], limit=25, revision_start=pysvn.Revision( pysvn.opt_revision_kind.number, info[ "commit_revision" ].number ) )
            # updates
            else:
                log = client.log( url_or_path=info[ "url" ], limit=25, revision_end=pysvn.Revision( pysvn.opt_revision_kind.number, info[ "commit_revision" ].number + 1 ) )
        except:
            # changelog
            log = client.log( url_or_path="http://xbmc-addons.googlecode.com/svn/addons/%s" % ( Addon.getAddonInfo( "Id" ), ), limit=25 )
        # if no entries set user message
        if ( len( log ) ):
            # initialize our log variable
            changelog = "%s\n" % ( "-" * 150, )
        else:
            # should only happen for "updates" and there are none
            changelog = Addon.getLocalizedString( 30704 )
        # we need to compile so we can add DOTALL
        clean_entry = self.re.compile( "\[.+?\][\s]+(?P<name>[^\[]+)(?:\[.+)?", self.re.DOTALL )
        # iterate thru and format each message
        for entry in log:
            # add heading
            changelog += "r%d - %s - %s\n\n" % ( entry[ "revision" ].number, datetime.datetime.fromtimestamp( entry[ "date" ] ).strftime( date_format ), entry[ "author" ], )
            # add formatted message
            changelog += "\n".join( [ self.re.sub( "(?P<name>^[a-zA-Z])", "- \\1", line.lstrip( " -" ) ) for line in clean_entry.sub( "\\1", entry[ "message" ] ).strip().splitlines() ] )
            # add separator
            changelog += "\n%s\n" % ( "-" * 150, )
        # return colorized result
        return self._colorize_text( changelog )

    def _pysvn_cancel_callback( self ):
        # check if user cancelled operation
        return False

    def _colorize_text( self, text ):
        # format text using colors
        text = self.re.sub( "(?P<name>r[0-9]+ - .+?)(?P<name2>[\r\n]+)", "[COLOR FF0084FF]\\1[/COLOR]\\2", text )
        text = self.re.sub( "(?P<name>http://[\S]+)", "[COLOR FFEB9E17]\\1[/COLOR]", text )
        text = self.re.sub( "(?P<name>[^\]]r[0-9]+)", "[COLOR FFEB9E17]\\1[/COLOR]", text )
        text = self.re.sub( "(?P<name>\".+?\")", "[COLOR FFEB9E17]\\1[/COLOR]", text )
        text = self.re.sub( "(?P<name>[A-Z ]+:)[\r\n]+", "[COLOR FF0084FF][B]\\1[/B][/COLOR]\n", text )
        text = self.re.sub( "(?P<name> - )", "[COLOR FFFFFFFF]\\1[/COLOR]", text )
        text = self.re.sub( "(?P<name>-[-]+)", "[COLOR FFFFFFFF]\\1[/COLOR]", text )
        # return colorized text
        return text


if ( __name__ == "__main__" ):
    # need this while debugging
    if ( len( sys.argv ) == 1 ):
        sys.argv.append( "view=updates" )
    # show info
    if ( sys.argv[ 1 ] in [ "view=updates", "view=changelog", "view=readme", "view=license" ] ):
        Viewer( kind=sys.argv[ 1 ].split( "=" )[ 1 ] )
