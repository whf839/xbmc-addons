# main import's
import sys
import os

try:
    import xbmcaddon
except:
    # get xbox compatibility module
    from resources.lib.xbox import *
    xbmcaddon = XBMCADDON()

# Script constants
__scriptname__ = "Apple Movie Trailers"
__author__ = "Apple Movie Trailers (AMT) Team"
__url__ = "http://code.google.com/p/xbmc-scripting/"
__svn_url__ = "http://xbmc-scripting.googlecode.com/svn/trunk/Apple%20Movie%20Trailers"
__credits__ = "XBMC TEAM, freenode/#xbmc-scripting"
__version__ = "2.0.0"
__XBMC_Revision__ = "31632"

def _log_start():
    # spam plugin statistics to log
    xbmc.log( "[SCRIPT] '%s: Version - %s' initialized!" % ( __scriptname__, __version__, ), xbmc.LOGNOTICE )

# Shared resources
BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

# create our language object
__Addon__ = xbmcaddon.Addon( id=os.path.basename( os.getcwd() ) )

# Main team credits
__credits_l1__ = __Addon__.getLocalizedString( 910 )#"Head Developer & Coder"
__credits_r1__ = "Killarny"
__credits_l2__ = __Addon__.getLocalizedString( 911 )#"Coder & Skinning"
__credits_r2__ = "Nuka1195"
__credits_l3__ = __Addon__.getLocalizedString( 912 )#"Graphics & Skinning"
__credits_r3__ = "Pike"

# additional credits
__add_credits_l1__ = __Addon__.getLocalizedString( 1 )#"Xbox Media Center"
__add_credits_r1__ = "Team XBMC"
__add_credits_l2__ = __Addon__.getLocalizedString( 913 )#"Usability"
__add_credits_r2__ = "Spiff & JMarshall"
__add_credits_l3__ = __Addon__.getLocalizedString( 914 )#"Language File"
__add_credits_r3__ = __Addon__.getLocalizedString( 2 )#"Translators name"


# Start the main gui
if __name__ == "__main__":
    # only run if compatible
    _log_start()
    # main window
    import gui
