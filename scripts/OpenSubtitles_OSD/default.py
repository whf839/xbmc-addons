import sys
import os
import xbmc
import string

__scriptname__ = "OpenSubtitles_OSD"
__author__ = "Amet"
__url__ = "http://code.google.com/p/opensubtitles-osd/"
__svn_url__ = "http://xbmc-addons.googlecode.com/svn/trunk/scripts/OpenSubtitles_OSD"
__credits__ = ""
__version__ = "1.36"

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )

sys.path.append (BASE_RESOURCE_PATH)




__language__ = xbmc.Language( os.getcwd() ).getLocalizedString
_ = sys.modules[ "__main__" ].__language__
__settings__ = xbmc.Settings( path=os.getcwd() )



#############-----------------Is script runing from OSD? -------------------------------###############


if  not xbmc.getCondVisibility('videoplayer.isfullscreen') :

	import xbmcgui
	dialog = xbmcgui.Dialog()
	selected = dialog.ok("OpenSubtitles_OSD", "This script needs to run from OSD" ,"For More Info Visit ", "http://code.google.com/p/opensubtitles-osd/" )




else:
   window = False
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
   if ( skin1.find( "alaska" ) > -1 ):
	skin = "Aeon"	
   
   if __settings__.getSetting( "debug" ) == "true":	
   		print "OpenSubtitles_OSD version [" +  __version__ +"]"
   		print "Skin Folder: [ " + skin1 +" ]"
   		print "OpenSubtitles_OSD skin XML: [ " + skin +" ]"
   		debug = True
   else:
    	debug = False   
   

###-------------------Extract Media files -----------------------------------################
   
   mediafolder = os.path.join("special://home/scripts/", __scriptname__ ,"resources","skins" , "Default" , "media" )
   
   if not os.path.exists(mediafolder):
   
		import unzip
		zip_file = os.path.join("special://home/scripts/", __scriptname__ ,"resources","lib" , "media.zip" )
		un = unzip.unzip()	
		un.extract_med( zip_file, mediafolder )

###-------------------------- Set Search String and Path string -------------################

   if ( __name__ == "__main__" ):
	
		
		search_string = ""
		
		if len(xbmc.getInfoLabel("VideoPlayer.TVshowtitle")) > 1: # TvShow
	
				year = 0
				season = str(xbmc.getInfoLabel("VideoPlayer.Season"))
				episode = str (xbmc.getInfoLabel("VideoPlayer.Episode"))
				showname = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")
				
				epchck = episode.lower()
				if epchck.find("s") > -1: # Check if season is "Special"
					season = "0"
					episode = episode.replace("s","")
					episode = episode.replace("S","")
				if ( int( season ) < 10 ):
					search_string = "S0" + season
				else:
					search_string = "S" + season
	
				if ( int( episode ) < 10 ):
					search_string = search_string + "E0" + episode
				else:
					search_string = search_string + "E" + episode
	
				search_string = showname + "+" + search_string 	
			
		else: # Movie or not in Library
		
				year = xbmc.getInfoLabel("VideoPlayer.Year")
				title = xbmc.getInfoLabel("VideoPlayer.Title")
	
				if str(year) == "": # Not in Library
					from utilities import getMovieTitleAndYear
					search_string, year = getMovieTitleAndYear( title )
					
				else: # Movie in Library
					search_string = title
						
		search_string = search_string.replace(" ","+")
	
	
	#### ------------------------------ Get User Settings ---------------------------#####
	
		temp = False
	
		movieFullPath = xbmc.Player().getPlayingFile()
		if (movieFullPath.find("http://") > -1 ) or (movieFullPath.find("smb://") > -1 ) or (movieFullPath.find("rar://") > -1 ):
			temp = True
		
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
	
		if not xbmc.getCondVisibility('Player.Paused') : xbmc.Player().pause() #Pause if not paused
		
		ui = gui.GUI( "script-OpenSubtitles_OSD-"+ skin +".xml" , os.getcwd(), "Default")
		service_present = ui.set_allparam ( movieFullPath,search_string,temp,sub_folder, year, debug )
		if service_present > -1 : ui.doModal()
		
		if xbmc.getCondVisibility('Player.Paused'): xbmc.Player().pause() # if Paused, un-pause
		del ui
		sys.modules.clear()
