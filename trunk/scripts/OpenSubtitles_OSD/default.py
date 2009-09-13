import sys
import os
import xbmc
import string

__scriptname__ = "OpenSubtitles_OSD"
__author__ = "Amet"
__url__ = "http://code.google.com/p/opensubtitles-osd/"
__svn_url__ = "http://xbmc-scripting.googlecode.com/svn/trunk/scripts/OpenSubtitles_OSD"
__credits__ = ""
__version__ = "1.33"

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)




__language__ = xbmc.Language( os.getcwd() ).getLocalizedString
_ = sys.modules[ "__main__" ].__language__
__settings__ = xbmc.Settings( path=os.getcwd() )

print "OpenSubtitles_OSD version[ " +  __version__ +" ]"

#############-----------------Is script runing from OSD?---Reset to Defaults----------------------------###############

try: check = sys.argv
except:check = ""
if  check == "" or (xbmc.Player().isPlaying() == False):

	import xbmcgui
	dialog = xbmcgui.Dialog()
	selected = dialog.ok("OpenSubtitles_OSD", "This script needs to run from OSD" ,"For More Info Visit ", "http://code.google.com/p/opensubtitles-osd/" )




else:
   
   skin = "main"
   skin1 = str(xbmc.getSkinDir().lower())
   skin1 = skin1.replace("-"," ")
   skin1 = skin1.replace("."," ")
   skin1 = skin1.replace("_"," ")
   if ( skin1.find( "eedia" ) > -1 ):
	skin = "MiniMeedia"
   if ( skin1.find( "tream" ) > -1 ):
	skin = "MediaStream"
   if ( skin1.find( "edux" ) > -1 ):
	skin = "MediaStream_Redux"
   if ( skin1.find( "aeon" ) > -1 ):
	skin = "Aeon"
   print "Skin Folder: [" + skin1 +"]"
   print "OpenSubtitles_OSD skin XML: [" + skin +"]"


###-------------------Extract Media files -----------------------------------################
   
   mediafolder = os.path.join("special://home/scripts/", __scriptname__ ,"resources","skins" , "Default" , "media" )
   
   if not os.path.exists(mediafolder):
   
		import unzip
		zip_file = os.path.join("special://home/scripts/", __scriptname__ ,"resources","lib" , "media.zip" )
		un = unzip.unzip()	
		un.extract_med( zip_file, mediafolder )

###-------------------------- Set Search String and Path string -------------################

   if ( __name__ == "__main__" ):


	temp = False
	search_string = ""
	path_string = ""
	year = 0
	if len( sys.argv ) > 1:
		#year = 0
		tmp_string = sys.argv[1]
		tmp_string.strip()
		path_string = tmp_string[tmp_string.find( "[PATH]" ) + len( "[PATH]" ):tmp_string.find( "[/PATH]" )]
		if ( tmp_string.find( "[MOVIE]" ) > 0 ):
			from utilities import getMovieTitleAndYear
			search_string1 = tmp_string[tmp_string.find( "[MOVIE]" ) + len( "[MOVIE]" ):tmp_string.find( "[/MOVIE]" )]
			search_string, year = getMovieTitleAndYear( search_string1 )
			tmp_list = search_string.split()
			search_string = string.join( tmp_list, '+' )
			
		elif ( tmp_string.find( "[TV]" ) > 0 ):
			#year = 0
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
	search_string = search_string.replace(".","+")
	movieFullPath = xbmc.Player().getPlayingFile()
	if (movieFullPath.find("http://") > -1 ) or (movieFullPath.find("smb://") > -1 ) or (movieFullPath.find("rar://") > -1 ):
		temp = True

#### ------------------------------ Get User Languages,Path and Service ---------------------------#####

	
	path = __settings__.getSetting( "subfolder" ) == "true"
	
	if not path :
		sub_folder = xbmc.translatePath(__settings__.getSetting( "subfolderpath" ))
		if len(sub_folder) < 1 :
			sub_folder = os.path.dirname( movieFullPath )
			
	
	else:
		if temp:
			import xbmcgui
			dialog = xbmcgui.Dialog()
			sub_folder = dialog.browse( 0, "Choose Subtitle folder", "files")
		else:
			sub_folder = os.path.dirname( movieFullPath )

#### ------------------------------ Get the main window going ---------------------------#####
	import gui
	if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause()
	ui = gui.GUI( "script-OpenSubtitles_OSD-"+ skin +".xml" , os.getcwd(), "Default")
	service_present = ui.set_allparam ( movieFullPath,search_string,temp,sub_folder, year )
	if service_present > -1 : ui.doModal()
	if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause()
	del ui
	sys.modules.clear()
