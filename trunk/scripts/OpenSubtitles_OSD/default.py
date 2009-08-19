import sys
import os
import xbmcgui
import xbmc
import string
import xbmcplugin
from xml.dom import minidom
from xml.dom.minidom import Document

__scriptname__ = "OpenSubtitles_OSD"
__author__ = "Amet"
__url__ = ""
__svn_url__ = "http://xbmc-scripting.googlecode.com/svn/trunk/scripts/OpenSubtitles_OSD"
__credits__ = ""
__version__ = "1.25"
EXIT_SCRIPT = ( 6, 10, 247, 275, 61467, 216, 257, 61448, )
CANCEL_DIALOG = EXIT_SCRIPT + ( 216, 257, 61448, )

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)


import language
__language__ = language.Language().localized

import unzip
import globals
import gui
from utilities import *



langugestrings = [ "Albanian","Arabic","Belarusian","Bosnian","Bulgarian","Catalan","Chinese","Croatian","Czech","Danish","Dutch","English","Estonian","Finnish","French","German","Greek","Hebrew","Hindi","Hungarian","Icelandic","Indonesian","Italian","Japanese","Korean","Latvian","Lithuanian","Macedonian","Norwegian","Polish","Portuguese","PortugueseBrazil","Romanian","Russian","SerbianLatin","Slovak","Slovenian","Spanish","Swedish","Thai","Turkish","Ukrainian","Vietnamese"]




#############-----------------Start Def -------------------------###############


def setings_menu (langugestrings):
	
	dialog = xbmcgui.Dialog()
	langugestrings.append('last item')
	selected1 = dialog.select('Select Default Language 1', langugestrings)
	selected2 = dialog.select('Select Default Language 2', langugestrings)
	if not (langugestrings[selected1] == "last item") and not (langugestrings[selected2] == "last item") :
		##dialog.ok("Language Selection", "You Have Selected" + " " + langugestrings[selected1] + " and " + langugestrings[selected2])
		lang1 = langugestrings[selected1]
		lang2 = langugestrings[selected2]
	else:
		dialog.ok("Language Selection", "You Have Not Selected a Valid Language")
		lang1 = "English"
		lang2 = "English"
	
	selected = dialog.yesno("OpenSubtitles_OSD",'Would you like to set a custom path?')

	if selected == 1:
		path = dialog.browse( 0, "OpenSubtitles_OSD", "files")
	else:
		path = "Default_folder"
	
	dialog = xbmcgui.Dialog()
	possibleChoices = ["Sublight", "OpenSubtitles"]  
	choice = dialog.select("Please choose the prefered service", possibleChoices)
	if choice == 0:
		service = "Sublight"
	if choice == 1:
		service = "OpenSubtitles"
		
	set_lang = "1"
	save_languages (lang1,lang2, set_lang, path,service)
	return lang1,lang2, path ,service



def get_languages ():
	lang1 = ""
	lang2 = ""
	lang =  os.path.join( os.getcwd(), 'resources' , "languages.xml")
	xmldoc = minidom.parse(lang)
	lang_set = int(xmldoc.getElementsByTagName("lang_set")[0].firstChild.data)
	path = xmldoc.getElementsByTagName("folder")[0].firstChild.data
	if lang_set == 1:
		lang1 = xmldoc.getElementsByTagName("language1")[0].firstChild.data
		lang2 = xmldoc.getElementsByTagName("language2")[0].firstChild.data
		
	service = xmldoc.getElementsByTagName("service")[0].firstChild.data
	return lang1,lang2,lang_set,path,service




def save_languages (lang1,lang2,set_lang,path,service):

	doc = Document()

	wml = doc.createElement("language")
	doc.appendChild(wml)

	maincard = doc.createElement("card")
	maincard.setAttribute("id", "main")
	wml.appendChild(maincard)

	paragraph1 = doc.createElement("language1")
	maincard.appendChild(paragraph1)
	ptext = doc.createTextNode(lang1)
	paragraph1.appendChild(ptext)

	paragraph1 = doc.createElement("language2")
	maincard.appendChild(paragraph1)
	ptext = doc.createTextNode(lang2)
	paragraph1.appendChild(ptext)

	paragraph1 = doc.createElement("lang_set")
	maincard.appendChild(paragraph1)
	ptext = doc.createTextNode(set_lang)
	paragraph1.appendChild(ptext)

	paragraph1 = doc.createElement("folder")
	maincard.appendChild(paragraph1)
	ptext = doc.createTextNode(path)
	paragraph1.appendChild(ptext)
	
	paragraph1 = doc.createElement("service")
	maincard.appendChild(paragraph1)
	ptext = doc.createTextNode(service)
	paragraph1.appendChild(ptext)
	
	wdoc = doc.toxml()

	lang =  os.path.join( os.getcwd(), 'resources' , "languages.xml")
	os.remove( lang )
	file = open(lang,"w") 
	file.write(wdoc)
	file.close()



#############-----------------Is script runing from OSD?---Reset to Defaults----------------------------###############

try: check = sys.argv
except:check = ""
if  check == "":
   
	dialog = xbmcgui.Dialog()
	selected = dialog.yesno("OpenSubtitles_OSD",'Do you want to restore to Defaults')

	if selected == 1:
		setings_menu( langugestrings )



else:
   xbmc.Player().pause()
   skin = (str(xbmc.getSkinDir()))
   if ( skin.find( "ransparency" ) > -1 ):
	skin = "PM3.HD"
   if ( skin.find( "roject" ) > -1 ):
	skin = "PM3.HD"
   if ( skin.find( "Mod" ) > -1 ):
	skin = "MediaStream_Redux"
   if ( skin.find( "Aeon" ) > -1 ):
	skin = "Aeon"



###-------------------Extract Media files -----------------------------------################
   un = unzip.unzip()
   mediafolder = os.path.join("special://home/scripts/", __scriptname__ ,"resources","skins" , skin , "media" )
   mediaflags = os.path.join("special://home/scripts/", __scriptname__ ,"resources","skins" , skin , "media","flags")
   
   zip_file = os.path.join("special://home/scripts/", __scriptname__ ,"resources","lib" , "media.zip" )

   if not os.path.exists(mediafolder):	
		un.extract_med( zip_file, mediafolder )

   if ( __name__ == "__main__" ):


###-------------------------- Set Search String and Path string -------------################
	temp = False
	search_string = ""
	path_string = ""
	if len( sys.argv ) > 1:
		tmp_string = sys.argv[1]
		tmp_string.strip()
		path_string = tmp_string[tmp_string.find( "[PATH]" ) + len( "[PATH]" ):tmp_string.find( "[/PATH]" )]
		if ( tmp_string.find( "[MOVIE]" ) > 0 ):
			search_string1 = tmp_string[tmp_string.find( "[MOVIE]" ) + len( "[MOVIE]" ):tmp_string.find( "[/MOVIE]" )]
			search_string = getMovieTitleAndYear( search_string1 )
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
	movieFullPath = xbmc.Player().getPlayingFile()
	if (movieFullPath.find("http://") > -1 ) or (movieFullPath.find("smb://") > -1 ):
		temp = True

#### ------------------------------ Get User Languages,Path and Service ---------------------------#####

	lang1,lang2,lang_set,path,service = get_languages ()
	
	if lang_set == 0:
		lang1,lang2,path,service = setings_menu( langugestrings )
	
	if not path == "Default_folder":
		
		sub_folder = xbmc.translatePath(path)
	else:
		if temp:
			dialog = xbmcgui.Dialog()
			sub_folder = dialog.browse( 0, "Choose Subtitle folder", "files")
			##temp = True
		else:
			sub_folder = os.path.dirname( movieFullPath )

#### ------------------------------ Get the main window going ---------------------------#####
	ui = gui.GUI( "script-OpenSubtitles_OSD-main.xml", os.getcwd(), skin)
	ui.set_service ( service )
	ui.set_filepath( movieFullPath )
	ui.set_searchstring( search_string )
	ui.set_temp( temp )
	ui.set_sub_folder( sub_folder )
	ui.set_lang(lang1,lang2)
	ui.doModal()
	xbmc.Player().pause()
	del ui

