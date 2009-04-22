"""
    Plugin for viewing your Google Reader content.

    Based on Nuka1195's Plugin framework - Thanks.

    Written by BigBellyBilly
    Contact me at BigBellyBilly at gmail dot com - Bugs reports and suggestions welcome.
"""

# main imports
import sys
import xbmc

# plugin constants
__plugin__ = "GoogleReader"
__author__ = "BigBellyBilly"
__url__ = "http://code.google.com/p/xbmc-addons/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/programs/GoogleReader"
__version__ = "1.1.1"
__date__ = '23-04-2009'
__svn_revision__ = "$Revision$"
__XBMC_Revision__ = "19001"

def _check_compatible():
    try:
        # spam plugin statistics to log
        xbmc.log( "[PLUGIN] '%s: Version - %s-r%s' initialized!" % ( __plugin__, __version__, __svn_revision__.replace( "$", "" ).replace( "Revision:", "" ).strip() ), xbmc.LOGNOTICE )
        # get xbmc revision
        xbmc_version = xbmc.getInfoLabel( "System.BuildVersion" )
        xbmc_rev = 0
        xbmc_rev = int( xbmc_version.split( " " )[ 1 ].replace( "r", "" ) )
        # compatible?
        ok = xbmc_rev >= int( __XBMC_Revision__ )
    except:
        # error, so make compatible
        ok = True
    # spam revision info
    xbmc.log( "     ** Required XBMC Revision: r%s **" % ( __XBMC_Revision__, ), xbmc.LOGNOTICE )
    xbmc.log( "     ** Found XBMC Revision: r%d [%s] **" % ( xbmc_rev, ( "Not Compatible", "Compatible", )[ ok ], ), xbmc.LOGNOTICE )
    # if not compatible, inform user
    if ( not ok ):
        import xbmcgui
        xbmcgui.Dialog().ok( "%s - %s: %s" % ( __plugin__, xbmc.getLocalizedString( 30700 ), __version__, ), xbmc.getLocalizedString( 30701 ) % ( __plugin__, ), xbmc.getLocalizedString( 30702 ) % ( __XBMC_Revision__, ), xbmc.getLocalizedString( 30703 ) )
    #return result
    return ok

if ( __name__ == "__main__" ):
	if not sys.argv[ 2 ]:
		# check for compatibility, only need to check this once
		if _check_compatible():
			from pluginAPI import xbmcplugin_categories as plugin
	elif ( sys.argv[ 2 ] in ("?info=readme.txt", "?info=changelog.txt") ):
		# view readme / changelog in a window
		try:
			import os
			from pluginAPI.TextView import TextViewDialog
			filename = sys.argv[ 2 ].split('=')[1]      # get filename
			filepath = os.getcwd() + "/resources/" + filename
			TextViewDialog("DialogScriptInfo.xml", os.getcwd()).ask( title=filename, fn=filepath )
		except:
			print str(sys.exc_info()[ 1 ])
	elif "show_item" in sys.argv[ 2 ]:
		from pluginAPI import xbmcplugin_show_item as plugin
	else:
		from pluginAPI import xbmcplugin_categories as plugin

	try:
		plugin.Main()
	except: pass
