import sys
import os
import xbmcgui
##import xbmc
import string
##import xbmcplugin
__scriptname__ = "OpenSubtitles_OSD"
__author__ = "Amet"
__url__ = ""
__svn_url__ = "http://xbmc-scripting.googlecode.com/svn/trunk/scripts/OpenSubtitles_OSD"
__credits__ = ""
__version__ = "1.09"


BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)


import language
import unzip
import globals
__language__ = language.Language().localized
un = unzip.unzip()


if (xbmc.Player().isPlaying() == False) :
   errorDialog = xbmcgui.Dialog()
   errorDialog.ok("OpenSubtitles_OSD", "Nice try, try it again... :)")
   del errorDialog


else:
   xbmc.Player().pause()
   movieFullPath = xbmc.Player().getPlayingFile()
   
   videoInfoTag = xbmc.Player().getVideoInfoTag()

   skin = (str(xbmc.getSkinDir()))
   if ( skin.find( "ransparency" ) > -1 ):
	skin = "PM3.HD"
   if ( skin.find( "roject" ) > -1 ):
	skin = "PM3.HD"
   fallback = os.path.join("special://home/scripts/", __scriptname__ ,"resources","skins" ,  "PM3.HD" )
   mediafolder = os.path.join("special://home/scripts/", __scriptname__ ,"resources","skins" , skin , "media" )
   zip_file = os.path.join("special://home/scripts/", __scriptname__ ,"resources","lib" , "media.zip" )
   if not os.path.exists(mediafolder):
   	un.extract( zip_file, mediafolder )
   if ( __name__ == "__main__" ):

	import gui
	window = "main"

	search_string = ""
	path_string = ""
	if len( sys.argv ) > 1:
		tmp_string = sys.argv[1]
		tmp_string.strip()
		path_string = tmp_string[tmp_string.find( "[PATH]" ) + len( "[PATH]" ):tmp_string.find( "[/PATH]" )]
		if ( tmp_string.find( "[MOVIE]" ) > 0 ):
			search_string = tmp_string[tmp_string.find( "[MOVIE]" ) + len( "[MOVIE]" ):tmp_string.find( "[/MOVIE]" )]
			tmp_list = search_string.split()
			search_string = string.join( tmp_list, '+' )
		elif ( tmp_string.find( "[TV]" ) > 0 ):
			search_string = tmp_string[tmp_string.find( "[TV]" ) + len( "[TV]" ):tmp_string.find( "[/TV]" )]			
			tmp_list = search_string.split()
			tmp_string = tmp_list.pop( 0 )
			if ( int( tmp_string ) < 10 ):
				search_string = "S0" + tmp_string
			else:
				search_string = "S" + tmp_string
			tmp_string = tmp_list.pop( 0 )
			if ( int( tmp_string ) < 10 ):
				search_string = search_string + "E0" + tmp_string
			else:
				search_string = search_string + "E" + tmp_string
			search_string = string.join( tmp_list, '+' ) + "+" + search_string 
	search_string = os.path.splitext(search_string)[0]
	
	if (movieFullPath.find("http://") > -1 ):
		movieFullPath = "special://temp/"

	ui = gui.GUI( "script-OpenSubtitles_OSD-main.xml", os.getcwd(), (skin))
	ui.set_filepath( movieFullPath )
	ui.set_searchstring( search_string )
	ui.doModal()
	xbmc.Player().pause()
	del ui



