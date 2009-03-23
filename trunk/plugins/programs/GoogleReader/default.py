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
__version__ = "0.1"
__date__ = '23-03-2009'
xbmc.log( "[PLUGIN] %s: v%s Dated: %s initialized!" % ( __plugin__, __version__, __date__), xbmc.LOGNOTICE )

if ( __name__ == "__main__" ):
	ok = True
	if not sys.argv[ 2 ]:
		from pluginAPI.bbbLib import checkBuildDate
		ok = checkBuildDate(__plugin__, "01-03-2009")		# DD-MM-YYY
		if ok:
			from pluginAPI import xbmcplugin_categories as plugin
	elif "show_item" in sys.argv[ 2 ]:
		from pluginAPI import xbmcplugin_show_item as plugin
	else:
		from pluginAPI import xbmcplugin_categories as plugin
	if ok:
		plugin.Main()
