import sys
import os
import xbmc
import xbmcgui
import osdb
from osdb import OSDBServer
from utilities import *
import urllib
import unzip
import sublight_utils as SublightUtils
import xmlrpclib
import time
import base64
import zipfile
import re
import globals
from urllib2 import Request, urlopen, URLError, HTTPError


_ = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__ = sys.modules[ "__main__" ].__version__
__settings__ = xbmc.Settings( path=os.getcwd() )

STATUS_LABEL = 100
LOADING_IMAGE = 110
SUBTITLES_LIST = 120
OSDB_SERVER = "http://www.opensubtitles.org/xml-rpc"


class GUI( xbmcgui.WindowXMLDialog ):
    ##socket.setdefaulttimeout(10.0) #seconds
	
    def __init__( self, *args, **kwargs ):
	
          
	  pass
	  


    def set_session(self,session_id):
	  self.session_id = session_id

    def set_allparam(self, path,search,temp,sub_folder, year):
	  self.year = year
	  LOG( LOG_INFO, "Year: [%s]" ,  self.year )
	  	  
	  lang1 = toScriptLang(__settings__.getSetting( "Language1" ))
	  lang2 = toScriptLang(__settings__.getSetting( "Language2" ))	  
	  
	  self.lang1 = toOpenSubtitlesId( lang1 )
	  self.lang_two1 = toOpenSubtitles_two(lang1)
	  LOG( LOG_INFO, "Language 1: [%s]" ,  self.lang1  )
	  
	  self.lang2 = toOpenSubtitlesId( lang2 )
	  self.lang_two2 = toOpenSubtitles_two(lang2)
	  LOG( LOG_INFO, "Language 2: [%s]" ,  self.lang2  )
	  	  
	  self.sub_folder = sub_folder
	  LOG( LOG_INFO, "Subtitle Folder: [%s]" ,  self.sub_folder )
	  
	  self.file_original_path = path
	  if not (path.find("special://") > -1 ):
		self.file_path = path[path.find(os.sep):len(path)]
	  else:
		self.file_path = path
	  LOG( LOG_INFO, "File Path: [%s]" ,  self.file_path )
	  
	  self.set_temp = temp
	  LOG( LOG_INFO, "Temp?: [%s]" ,  self.set_temp )
	          
	  self.search_string = latin1_to_ascii(search)
	  LOG( LOG_INFO, "Search String: [%s]" , self.search_string )
	  
	  self.OS =  __settings__.getSetting( "OS" ) == "true"
	  if self.OS : self.service = "OpenSubtitles"
	  LOG( LOG_INFO, "OS Service : [%s]" , self.OS )

	  self.PN =  __settings__.getSetting( "PN" ) == "true"
	  self.username = __settings__.getSetting( "PNuser" )
	  self.password = __settings__.getSetting( "PNpass" )
	  if self.PN and len(self.username) > 1 and len(self.password) >1 :
	  	self.service = "Podnapisi"
	  else:	
	  	self.PN = False
	  	
	  LOG( LOG_INFO, "PN Service : [%s]" , self.PN )

	  self.SL =  __settings__.getSetting( "SL" ) == "true"
	  if self.SL : self.service = "Sublight"
	  LOG( LOG_INFO, "SL Service : [%s]" , self.SL )
	  
	  if not self.SL and not self.OS and not self.PN:
		import xbmcgui
		dialog = xbmcgui.Dialog()
		possibleChoices = ["Sublight", "OpenSubtitles","Podnapisi"]  
		choice = dialog.select( _( 505 ) , possibleChoices)
		self.service = ""
		if choice == 0:
			self.service = "Sublight"
			self.SL = True
		if choice == 1:
			self.service = "OpenSubtitles"
			self.OS = True
		if choice == 2:
			if len(self.username) > 1 and len(self.password) >1 :
				self.service = "Podnapisi"
				self.PN = True
			else:	
				#import xbmcgui
				dialog = xbmcgui.Dialog()
				selected = dialog.ok("OpenSubtitles_OSD", "Podnapisi service requires username and password", "Register at www.podnapisi.net and enter it", "in script settings menu" )
				#self.exit_script()
		LOG( LOG_INFO, "Service : [%s]" , self.service )
	  
	  self.mansearch =  __settings__.getSetting( "searchstr" ) == "true"
	  LOG( LOG_INFO, "Manual Search : [%s]" , self.mansearch )
	  
	  self.pos = -1
	  	  
	  if self.SL : self.pos = self.pos +1
	  if self.OS : self.pos = self.pos +1
	  if self.PN : self.pos = self.pos +1
	  service_num = self.pos
	  if self.mansearch : self.pos = self.pos +1
	  LOG( LOG_INFO, "Self Pos : [%s]" , self.pos )
	  
	  self.pause = True
	  return service_num

    def set_filehash( self, hash ):
        LOG( LOG_INFO, "File Hash: [%s]" , ( hash ) )
        self.file_hash = hash

    def set_filesize( self, size ):
        LOG( LOG_INFO, "File Size: [%s]" , ( size ) )
        self.file_size = size


    def set_subtitles( self, subtitles ):
        self.subtitles = subtitles

    def onInit( self ):


	LOG( LOG_INFO, "onInit" )
        self.setup_all()

	    
    def extract(self, file, dir):
    

        zf = zipfile.ZipFile(file, "r")

        for i, name in enumerate(zf.namelist()):
            LOG( LOG_INFO, "Zip test: [%s]", name )	
            if not name.endswith('/'):
                outfile = open(os.path.join(dir, name), 'wb')
                outfile.write(zf.read(name))
                outfile.flush()
                outfile.close()    
    
    
    
    def setup_all( self ):

    
        self.getControl( 300 ).setLabel( _( 601 ) )
        self.getControl( 301 ).setLabel( _( 602 ) )
        self.setup_variables()
        self.connect()

        
    def setup_variables( self ):
    
        try: xbox = xbmc.getInfoLabel( "system.xboxversion")
        except:xbox = ""
        if xbox == "":
        	self.set_xbox = False
        else:
        	self.set_xbox = True
        LOG( LOG_INFO, "XBOX System: [%s]" ,  xbox )	
        self.controlId = -1
        self.allow_exception = False
        self.osdb_server = OSDBServer()
        self.osdb_server.Create()
        self.manuall = False
    
    
    def connect( self ):
		self.getControl( SUBTITLES_LIST ).reset()
		self.osdb_server.Create()

		if self.service == "OpenSubtitles":
			self.getControl( 111 ).setVisible( False )
			self.getControl( 110 ).setVisible( True )
			self.connected = True
			self.getControl( STATUS_LABEL ).setLabel( _( 635 ) )
			self.search_subtitles()

		if self.service == "Sublight":
			self.getControl( 110 ).setVisible( False )
			self.getControl( 111 ).setVisible( True )
			self.getControl( STATUS_LABEL ).setLabel( _( 646 ) )
			self.search_subtitles_sub()

		if self.service == "Podnapisi":
			self.getControl( 110 ).setVisible( False )
			self.getControl( 111 ).setVisible( False )
			self.getControl( STATUS_LABEL ).setLabel( _( 646 ) )
			self.search_subtitles_pod()
		



    def search_subtitles( self ):
        ok = False
	ok2 = False
	ok3 = False
	msg = ""

	self.getControl( STATUS_LABEL ).setLabel( xbmc.getLocalizedString( 646 ) )	

	try:
            if not self.file_original_path.find("http") > -1 and not self.set_xbox :
                LOG( LOG_INFO, "Search by hash " +  os.path.basename( self.file_original_path ) )
                self.getControl( STATUS_LABEL ).setLabel( _( 642 ) % ( "...", ) )
                self.set_filehash ( hashFile( self.file_original_path ) )
                self.set_filesize ( os.path.getsize( self.file_original_path ) )    
                try : ok,msg = self.osdb_server.searchsubtitles( self.search_string, self.file_hash,self.file_size,self.lang1,self.lang2,self.year )
                except: self.connected = False
                if not ok:
                	self.connected = False
                LOG( LOG_INFO, "Hash Search: " + msg )
                        
            if not self.connected or (len ( self.osdb_server.subtitles_hash_list )) < 2:
                LOG( LOG_INFO,"Search by name " +  self.search_string )
                self.getControl( STATUS_LABEL ).setLabel( _( 642 ) % ( "......", ) )
                
                ok2,msg2 = self.osdb_server.searchsubtitlesbyname( self.search_string, self.lang1 )
                LOG( LOG_INFO, "Name Search: " + msg2 )
                
                ok3,msg3 = self.osdb_server.searchsubtitlesbyname_alt( self.search_string, self.lang2 , self.lang1 )
                LOG( LOG_INFO, "Name 2 Search: " + msg3 )
                
            self.osdb_server.mergesubtitles()
            if not ok and not ok2 and not ok3:
                self.getControl( STATUS_LABEL ).setLabel( _( 634 ) % ( msg, ) )
                
            if self.osdb_server.subtitles_list:
                label = ""
                label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "Sublight.si" )
                listitem = xbmcgui.ListItem( label,label2 )
                if self.SL : self.getControl( SUBTITLES_LIST ).addItem( listitem )
                label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "Podnapisi.net" )
                listitem = xbmcgui.ListItem( label,label2 )
                if self.PN : self.getControl( SUBTITLES_LIST ).addItem( listitem )
                label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
                listitem = xbmcgui.ListItem( label,label2 )
                if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
                for item in self.osdb_server.subtitles_list:
		    
                    listitem = xbmcgui.ListItem( label=item["language_name"], label2=item["filename"], iconImage=item["rating"], thumbnailImage=item["language_flag"] )
                    

                    if item["sync"]:
                        listitem.setProperty( "sync", "true" )
                    else:
                        listitem.setProperty( "sync", "false" )
                    self.getControl( SUBTITLES_LIST ).addItem( listitem )
            else:
		    
					label = ""
					label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "Sublight.si" )
					listitem = xbmcgui.ListItem( label,label2 )
					if self.SL : self.getControl( SUBTITLES_LIST ).addItem( listitem )
					label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "Podnapisi.net" )
					listitem = xbmcgui.ListItem( label,label2 )
					if self.PN : self.getControl( SUBTITLES_LIST ).addItem( listitem )
					label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
					listitem = xbmcgui.ListItem( label,label2 )
					if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
		    



            movie_title1 = self.search_string.replace("+"," ")
            self.getControl( STATUS_LABEL ).setLabel(( str( len ( self.osdb_server.subtitles_list ) )) + _( 744 ) + '"' + movie_title1 + '"' )
	    
            self.setFocus( self.getControl( SUBTITLES_LIST ) )
            self.getControl( SUBTITLES_LIST ).selectItem( 0 )
	    
        except Exception, e:
            error = _( 634 ) % ( "search_subtitles:" + str ( e ) ) 
            LOG( LOG_ERROR, error )
            return False, error
        
    def search_subtitles_pod( self ):
        ok = False
	ok2 = False
	ok3 = False
	msg = ""
	test = 0
	self.getControl( STATUS_LABEL ).setLabel( _( 646 ) )	

	try:
            if test == 0 and not self.file_original_path.find("http") > -1 and not self.set_xbox :
                LOG( LOG_INFO, "Search by hash_pod " +  os.path.basename( self.file_original_path ) )
                self.getControl( STATUS_LABEL ).setLabel( _( 642 ) % ( "...", ) )
                self.set_filehash( hashFile( self.file_original_path ) )

                ok,msg = self.osdb_server.searchsubtitles_pod( self.search_string, self.file_hash,self.lang_two1,self.lang_two2 )
                if not ok:
                	self.connected = False
                LOG( LOG_INFO, "Hash Search_pod: " + msg )
                        
            if (len ( self.osdb_server.subtitles_hash_list )) < 2:
                LOG( LOG_INFO,"Search by name_pod" +  self.search_string )
                self.getControl( STATUS_LABEL ).setLabel( _( 642 ) % ( "......", ) )
                
                ok2,msg2 = self.osdb_server.searchsubtitlesbyname_pod( self.search_string, self.lang_two1,self.lang_two2, self.year )
                LOG( LOG_INFO, "Name Search_pod: " + msg2 )
                
                
            self.osdb_server.mergesubtitles()
            if not ok and not ok2 and not ok3:
                self.getControl( STATUS_LABEL ).setLabel( _( 634 ) % ( msg, ) )
                
            if self.osdb_server.subtitles_list:
                label = ""
                label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "Sublight.si" )
                listitem = xbmcgui.ListItem( label,label2 )
                if self.SL : self.getControl( SUBTITLES_LIST ).addItem( listitem )
                label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "OpenSubtitles.org" )
                listitem = xbmcgui.ListItem( label,label2 )
                if self.OS : self.getControl( SUBTITLES_LIST ).addItem( listitem )
                label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
                listitem = xbmcgui.ListItem( label,label2 )
                if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
                for item in self.osdb_server.subtitles_list:
		    
                    listitem = xbmcgui.ListItem( label=item["language_name"], label2=item["filename"], iconImage=item["rating"], thumbnailImage=item["language_flag"] )
                    

                    if item["sync"]:
                        listitem.setProperty( "sync", "true" )
                    else:
                        listitem.setProperty( "sync", "false" )
                    self.getControl( SUBTITLES_LIST ).addItem( listitem )
            else:
		    
					label = ""
					label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "Sublight.si" )
					listitem = xbmcgui.ListItem( label,label2 )
					if self.SL : self.getControl( SUBTITLES_LIST ).addItem( listitem )
					label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + "OpenSubtitles.org" )
					listitem = xbmcgui.ListItem( label,label2 )
					if self.OS : self.getControl( SUBTITLES_LIST ).addItem( listitem )
					label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
					listitem = xbmcgui.ListItem( label,label2 )
					if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
		    



            movie_title1 = self.search_string.replace("+"," ")
            self.getControl( STATUS_LABEL ).setLabel(   str( len ( self.osdb_server.subtitles_list ) ) + _( 744 ) + '"' + movie_title1 + '"' )
	    
            self.setFocus( self.getControl( SUBTITLES_LIST ) )
            self.getControl( SUBTITLES_LIST ).selectItem( 0 )
	    
        except Exception, e:
            error = _( 634 ) % ( "search_subtitles:" + str ( e ) ) 
            LOG( LOG_ERROR, error )
            return False, error    
    
    
    
    
    
    def search_subtitles_sub( self ):
		self.getControl( 111 ).setVisible( True )
		self.getControl( 110 ).setVisible( False )
		self.getControl( STATUS_LABEL ).setLabel( _( 642 ) % ( "...", ) )
		sublightWebService = SublightUtils.SublightWebService()
		session_id = sublightWebService.LogInAnonymous()
		self.set_session(session_id)
	
		videoInfoTag = xbmc.Player().getVideoInfoTag()
		movie_year  = ( videoInfoTag.getYear(), "" ) [ videoInfoTag.getYear() == 0 ]
		movie_title = self.search_string.replace ("+"," ")
	
		video_hash = ""

		if not self.set_xbox and not self.file_original_path.find("http") > -1 :
			md5_video_hash = SublightUtils.calculateMD5VideoHash( self.file_original_path )
			video_hash     = sublightWebService.GetFullVideoHash( session_id, md5_video_hash )
		
		if video_hash == "":
			video_hash = "0000000000000000000000000000000000000000000000000000"
	
		subtitles = []
        	language1 = SublightUtils.toSublightLanguage( self.lang1 )
        	language2 = SublightUtils.toSublightLanguage(  self.lang2 )
        	language3 = SublightUtils.toSublightLanguage( "0" )
	
		season = xbmc.getInfoLabel("VideoPlayer.Season")
		episode = xbmc.getInfoLabel("VideoPlayer.Episode")
		title = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")

	
		if (len(episode) > -1):
			movie_year = ""
	
		if not (len(title) > 0) or self.manuall:	
			movie_title = self.search_string.replace ("+"," ")
			episode = ""
			season = ""
			movie_year = ""
		else:
			movie_title = title	

		LOG( LOG_INFO, "Sublight Hash [%s]" , str(video_hash) )
		LOG( LOG_INFO, "Sublight Language 1: [%s], Language 2: [%s]" , language1 ,language2 )
		LOG( LOG_INFO, "Sublight Search Title:[%s] , Season:[%s] , Episode:[%s]" , movie_title,season,episode )
		self.getControl( STATUS_LABEL ).setLabel( _( 642 ) % ( "......", ) )
		subtitles = sublightWebService.SearchSubtitles(session_id, video_hash, movie_title, movie_year,season, episode, language2, language1, language3 )
	
		self.set_subtitles(subtitles)
	
		if len(subtitles) == 0 :
        	        label = ""
        	        label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + " OpenSubtitles.org")
              
        	        listitem = xbmcgui.ListItem( label,label2 )
        	        if self.OS : self.getControl( SUBTITLES_LIST ).addItem( listitem )
        	        label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + " Podnapisi.net")
        	        listitem = xbmcgui.ListItem( label,label2 )
        	        if self.PN : self.getControl( SUBTITLES_LIST ).addItem( listitem )
        	        label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
        	        listitem = xbmcgui.ListItem( label,label2 )
        	        if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
						


		else:
                
            	    label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + " OpenSubtitles.org")
            	    label = ""
            	    listitem = xbmcgui.ListItem( label,label2 )
                
            	    if self.OS : self.getControl( SUBTITLES_LIST ).addItem( listitem )
            	    label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + " Podnapisi.net")
            	    listitem = xbmcgui.ListItem( label,label2 )
            	    if self.PN : self.getControl( SUBTITLES_LIST ).addItem( listitem )
            	    label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
            	    listitem = xbmcgui.ListItem( label,label2 )
            	    if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
            	    
            	    for subtitle in subtitles:
                
						release       =                          subtitle[ "release" ]
						language      =                          subtitle[ "language" ]
						isLinked      =                          subtitle[ "isLinked" ]
						rate          =                          subtitle[ "rate" ]
						icon_flag     = "flags/" + toOpenSubtitles_two(language) + ".gif"
						
						listitem = xbmcgui.ListItem( label=language, label2=release, thumbnailImage=icon_flag, iconImage=str(int(round(rate*2))) )

						if isLinked == "true" :
							listitem.setProperty( "sync", "true" )
						else:
							listitem.setProperty( "sync", "false" )
						self.getControl( SUBTITLES_LIST ).addItem( listitem )
		
		
		movie_title1 = self.search_string.replace("+"," ")
		self.getControl( STATUS_LABEL ).setLabel( str( len ( self.subtitles ) ) +  _( 744 ) + '"' + movie_title1 + '"' )
		self.setFocus( self.getControl( SUBTITLES_LIST ) )
		self.getControl( SUBTITLES_LIST ).selectItem( 0 )
		LOG( LOG_INFO,"Service "+self.service)
    
    
    
    
    def show_control( self, controlId ):
        self.getControl( STATUS_LABEL ).setVisible( controlId == STATUS_LABEL )
        self.getControl( SUBTITLES_LIST ).setVisible( controlId == SUBTITLES_LIST )
        page_control = ( controlId == STATUS_LABEL )
        try: self.setFocus( self.getControl( controlId + page_control ) )
        except: self.setFocus( self.getControl( controlId ) )


    def file_download(self, url, dest):
		LOG( LOG_INFO, "Link down" + url )
		req = Request(url)
		f = urlopen(req)
		local_file = open(dest, "w" + "b")

		local_file.write(f.read())
		local_file.close()
            

    def download_subtitles(self, pos):
        LOG( LOG_INFO, "download_subtitles" )
        self.getControl( STATUS_LABEL ).setLabel(  _( 649 ) )
        if self.osdb_server.subtitles_list:
            

            filename = self.osdb_server.subtitles_list[pos]["filename"]
            subtitle_format = self.osdb_server.subtitles_list[pos]["format"]
            url = self.osdb_server.subtitles_list[pos]["link"]
            local_path = self.sub_folder
            zip_filename = xbmc.translatePath( os.path.join( local_path, "zipsubs.zip" ) )
            
            sub_filename = os.path.basename( self.file_path )
            form = self.osdb_server.subtitles_list[pos]["format"]
            lang = toOpenSubtitles_two(self.osdb_server.subtitles_list[pos]["language_name"])
            subName1 = sub_filename[0:sub_filename.rfind(".")] 
            if subName1 == "":
				subName1 = self.search_string.replace("+", " ")
            if self.set_temp:
				subName1 = self.search_string.replace("+", " ")
            
            self.file_download( url, zip_filename )
	    self.extract_subtitles( filename, form, lang,subName1, subtitle_format, zip_filename, local_path )
	    
	    
    
	    



    def download_subtitles_sub(self, pos):
        subtitle_id   =                          self.subtitles[pos][ "subtitleID" ]
        language      =                          self.subtitles[pos][ "language" ]
        numberOfDiscs = SublightUtils.toInteger( self.subtitles[pos][ "numberOfDiscs" ] )
 
	self.getControl( STATUS_LABEL ).setLabel(  _( 649 ) )
	sublightWebService = SublightUtils.SublightWebService()
        ticket_id, download_wait = sublightWebService.GetDownloadTicket(self.session_id, subtitle_id)
	if ticket_id != "" :
	    if download_wait > 0 :
		time.sleep(float(download_wait))
			
            xbmc.Player().setSubtitles(xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib','dummy.srt' ) ) )
            #subs = False
            #xbmc.Player().setSubtitles("")
            subtitle_b64_data = sublightWebService.DownloadByID(self.session_id, subtitle_id, ticket_id)
            base64_file_path = os.path.join(  self.sub_folder, "subtitle.b64" )
            base64_file      = open(base64_file_path, "wb")
            base64_file.write( subtitle_b64_data )
            base64_file.close()
            
            base64_file = open(base64_file_path, "r")
             
            zip_file_path = os.path.join( self.sub_folder , "subtitle.zip" )
            zip_file      = open(zip_file_path, "wb")
                     
            base64.decode(base64_file, zip_file)

            base64_file.close()
            zip_file.close()

            filename = ""
            subtitle_format = "srt"
            local_path = self.sub_folder
            zip_filename = zip_file_path
            sub_filename = os.path.basename( self.file_path )
            form = "srt"
            lang = str(toOpenSubtitles_two(language))
            subtitle_lang = lang
            subName1 = sub_filename[0:sub_filename.rfind(".")] 
            if subName1 == "":
				subName1 = self.search_string.replace("+", " ")

            movie_files     = []
            number_of_discs = int(numberOfDiscs)
            if number_of_discs == 1 :
                movie_files.append(sub_filename)
            elif number_of_discs > 1 and not self.set_temp:

                regexp = movie_file
                regexp = regexp.replace( "\\", "\\\\" )
                regexp = regexp.replace( "^", "\^" )
                regexp = regexp.replace( "$", "\$" )
                regexp = regexp.replace( "+", "\+" )
                regexp = regexp.replace( "*", "\*" )
                regexp = regexp.replace( "?", "\?" )
                regexp = regexp.replace( ".", "\." )
                regexp = regexp.replace( "|", "\|" )
                regexp = regexp.replace( "(", "\(" )
                regexp = regexp.replace( ")", "\)" )
                regexp = regexp.replace( "{", "\{" )
                regexp = regexp.replace( "}", "\}" )
                regexp = regexp.replace( "[", "\[" )
                regexp = regexp.replace( "]", "\]" )
                regexp = re.sub( "\d+", "\\d+", regexp )
                regex  = re.compile( regexp, re.IGNORECASE )
                
                
                movie_dir  = os.path.dirname  (self.file_path)
                movie_file = os.path.basename (self.file_path)
                
                files = os.listdir( movie_dir )
                for file in files :
                    if regex.match( self.file_path ) != None:
                        movie_files.append(self.file_path)
                

                movie_files.sort()
                

            if not zipfile.is_zipfile( zip_file_path ) :

        	    label = ""
        	    label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + " OpenSubtitles.org")
              
        	    listitem = xbmcgui.ListItem( label,label2 )
        	    if self.OS : self.getControl( SUBTITLES_LIST ).addItem( listitem )
        	    label2 = "[COLOR=FFFF0000]%s[/COLOR]" % (  _( 610 ) + " Podnapisi.net")
        	    listitem = xbmcgui.ListItem( label,label2 )
        	    if self.PN : self.getControl( SUBTITLES_LIST ).addItem( listitem )
        	    label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
        	    listitem = xbmcgui.ListItem( label,label2 )
        	    if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
            else :

                self.getControl( STATUS_LABEL ).setLabel(  _( 652 ) )
                zip = zipfile.ZipFile (zip_file_path, "r")
                i   = 0
                for zip_entry in zip.namelist():

                    file_name = zip_entry
                    i         = i + 1
                    if i <= len( movie_files ) :
                    
						sub_ext  = os.path.splitext( file_name )[1]
						sub_name = os.path.splitext( movie_files[i - 1] )[0]
						if self.set_temp:
							sub_name = self.search_string.replace("+", " ")
							
						file_name = "%s.%s%s" % ( sub_name, subtitle_lang, sub_ext )   
                    
                    file_path = os.path.join(self.sub_folder, file_name)
                    outfile   = open(file_path, "wb")
                    outfile.write( zip.read(zip_entry) )
                    outfile.close()
                zip.close()
                xbmc.Player().pause()
                xbmc.Player().setSubtitles(file_path)

            os.remove(base64_file_path)
            os.remove(zip_file_path)
            self.exit_script()            
            


	     
    def extract_subtitles(self, filename, form, lang, subName1, subtitle_format, zip_filename, local_path ):
        LOG( LOG_INFO, "extract_subtitles" )
        self.getControl( STATUS_LABEL ).setLabel(  _( 652 ) )
        xbmc.Player().setSubtitles(xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib','dummy.srt' ) ) )
        
        try:
            un = unzip.unzip()
            files = un.get_file_list( zip_filename )
            ztest = os.path.join( self.sub_folder , "zip1.zip" )
            if not zipfile.is_zipfile( zip_filename ) :
            	self.getControl( STATUS_LABEL ).setLabel( _( 654 ) )
            	subtitle_set = False
            	label = ""
            	label2 = "[COLOR=FFFF0000]%s[/COLOR]" % ( _( 610 ) +" Sublight.si" )
            	listitem = xbmcgui.ListItem( label,label2 )
            	if self.SL : self.getControl( SUBTITLES_LIST ).addItem( listitem )
            	label2 = "[COLOR=FFFF0000]%s[/COLOR]" % ( _( 610 ) +" Podnapisi.net" )
            	listitem = xbmcgui.ListItem( label,label2 )
            	if self.PN : self.getControl( SUBTITLES_LIST ).addItem( listitem )

            	label2 = "[COLOR=FF00FF00]%s[/COLOR]" % ( _( 612 ) )
            	listitem = xbmcgui.ListItem( label,label2 )
            	if self.mansearch : self.getControl( SUBTITLES_LIST ).addItem( listitem )
			
	    else:
	    	self.getControl( STATUS_LABEL ).setLabel( _( 650 ) )
            LOG( LOG_INFO, _( 631 ) % ( zip_filename, local_path ) )
            un.extract( zip_filename, local_path )
            LOG( LOG_INFO, _( 644 ) % ( local_path ) )
            self.getControl( STATUS_LABEL ).setLabel( _( 651 ) )
            LOG( LOG_INFO, "Number of subs in zip:[%s]" ,str(len(files)) )
            
            movie_files     = []
            number_of_discs = 1
            sub_filename = os.path.basename( self.file_path )
            
            if number_of_discs == 1 :
                movie_files.append(sub_filename)
            elif number_of_discs > 1 and not self.set_temp:

                regexp = movie_file
                regexp = regexp.replace( "\\", "\\\\" )
                regexp = regexp.replace( "^", "\^" )
                regexp = regexp.replace( "$", "\$" )
                regexp = regexp.replace( "+", "\+" )
                regexp = regexp.replace( "*", "\*" )
                regexp = regexp.replace( "?", "\?" )
                regexp = regexp.replace( ".", "\." )
                regexp = regexp.replace( "|", "\|" )
                regexp = regexp.replace( "(", "\(" )
                regexp = regexp.replace( ")", "\)" )
                regexp = regexp.replace( "{", "\{" )
                regexp = regexp.replace( "}", "\}" )
                regexp = regexp.replace( "[", "\[" )
                regexp = regexp.replace( "]", "\]" )
                regexp = re.sub( "\d+", "\\d+", regexp )
                regex  = re.compile( regexp, re.IGNORECASE )
                
                
                movie_dir  = os.path.dirname  (self.file_path)
                movie_file = os.path.basename (self.file_path)
                
                files = os.listdir( movie_dir )
                for file in files :
                    if regex.match( self.file_path ) != None:
                        movie_files.append(self.file_path)
                

                movie_files.sort()
                
            if not zipfile.is_zipfile( zip_filename ) :

				self.getControl( STATUS_LABEL ).setLabel( _( 654 ) )
				label2 = "[COLOR=FF00FF00]%s[/COLOR]" % (  _( 612 ) )
				listitem = xbmcgui.ListItem( label,label2 )
				self.getControl( SUBTITLES_LIST ).addItem( listitem )
            else :
                self.getControl( STATUS_LABEL ).setLabel(  _( 652 ) )
                zip = zipfile.ZipFile (zip_filename, "r")
                i   = 0
                for zip_entry in zip.namelist():
                    LOG( LOG_INFO, "Zip [%s]" , self.sub_folder )
                    if (zip_entry.find( "srt" ) < 0)  and (zip_entry.find( "sub" ) < 0)  and (zip_entry.find( "txt" )< 0) :
                		LOG( LOG_INFO, "Brisi " + os.path.join( self.sub_folder, zip_entry ) )
                		os.remove ( os.path.join( self.sub_folder, zip_entry ) )

                    
                    
                    if ( zip_entry.find( "srt" )  > 0 ) or ( zip_entry.find( "sub" )  > 0 ) or ( zip_entry.find( "txt" )  > 0 ):
                    
						if i == 0 :
						
							i         = i + 1
							file_name = zip_entry
							sub_ext  = os.path.splitext( file_name )[1]
							sub_name = os.path.splitext( movie_files[i - 1] )[0]
							if self.set_temp:
								sub_name = self.search_string.replace("+", " ")
									
							file_name = "%s.%s%s" % ( sub_name, str(lang), ".srt" )
							file_path = os.path.join(self.sub_folder, file_name)
							outfile   = open(file_path, "wb")
							outfile.write( zip.read(zip_entry) )
							outfile.close()
							os.remove ( os.path.join( self.sub_folder, zip_entry ) )
                zip.close()
                xbmc.Player().pause()
                xbmc.Player().setSubtitles(file_path)


            os.remove(zip_filename)
            self.exit_script()            



	except Exception, e:
            error = _( 634 ) % ( str ( e ) )
            LOG( LOG_ERROR, error )
            


    def keyboard(self):
		sep = xbmc.translatePath(os.path.dirname(self.file_original_path))
		default = sep.split(os.sep)
		dir = default.pop()
		if str(dir) == "":
			default = sep.split("/")
			dir = default.pop()
		kb = xbmc.Keyboard(dir, 'Enter The Search String', False)
		
		LOG( LOG_INFO, "Directory: [%s] " , dir + str(default) )
		text = self.search_string
		kb.doModal()
		if (kb.isConfirmed()):
			text = kb.getText()
    		
    		self.search_string = text.replace(" ","+")
    		LOG( LOG_INFO, "Keyboard Entry: [%s]" ,  self.search_string )
    		self.manuall = True
		self.connect()
    		
    def exit_script( self, restart=False ):

        self.close()

    def onClick( self, controlId ):

           	
		if self.pos == 1:
			if not self.mansearch:
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 0):
    		
					if (self.service == "OpenSubtitles"):
						if self.PN:
							service = "Podnapisi"
						if self.SL:
							service = "Sublight"

					if (self.service == "Podnapisi"):
						if self.OS:
							service = "OpenSubtitles"
						if self.SL:
							service = "Sublight"

					if (self.service == "Sublight"):
						if self.PN:
							service = "Podnapisi"
						if self.OS:
							service = "OpenSubtitles"	
					self.service = service
					self.connect()
					
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() >= 1):
            	
					if self.service == "OpenSubtitles":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) -1 )

					if self.service == "Sublight":
						self.download_subtitles_sub( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 1 )
            	
					if self.service == "Podnapisi":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 1 ) 	
			else:
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 0):    
					self.keyboard()
					
    			if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() >= 1):
            	
					if self.service == "OpenSubtitles":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) -1 )

					if self.service == "Sublight":
						self.download_subtitles_sub( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 1 )
            	
					if self.service == "Podnapisi":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 1 )					 
					
		if self.pos == 2:
			if not self.mansearch:
			
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 0):
    		
					if (self.service == "OpenSubtitles"):
						if self.PN:
							service = "Podnapisi"
						if self.SL:
							service = "Sublight"

					if (self.service == "Podnapisi"):
						if self.OS:
							service = "OpenSubtitles"
						if self.SL:
							service = "Sublight"

					if (self.service == "Sublight"):
						if self.PN:
							service = "Podnapisi"
						if self.OS:
							service = "OpenSubtitles"	
					self.service = service
					self.connect()
    							
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 1):
    	
					if (self.service == "OpenSubtitles"):
						if self.SL:
							service = "Sublight"
						if self.PN:
							service = "Podnapisi"


					
					if (self.service == "Podnapisi"):
						if self.SL:
							service = "Sublight"
						if self.OS:
							service = "OpenSubtitles"


					if (self.service == "Sublight"):
						if self.OS:
							service = "OpenSubtitles"	
						if self.PN:
							service = "Podnapisi"

					self.service = service
					self.connect()
    				
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() >= 2):
            	
					if self.service == "OpenSubtitles":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) -2 )

					if self.service == "Sublight":
						self.download_subtitles_sub( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 2 )
            	
					if self.service == "Podnapisi":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 2 ) 
						
						    				
			else:
    		
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 0):
    		
					if (self.service == "OpenSubtitles"):
						if self.PN:
							service = "Podnapisi"
						if self.SL:
							service = "Sublight"

					
					if (self.service == "Podnapisi"):
						if self.OS:
							service = "OpenSubtitles"
						if self.SL:
							service = "Sublight"

					if (self.service == "Sublight"):
						if self.PN:
							service = "Podnapisi"
						if self.OS:
							service = "OpenSubtitles"	
					self.service = service
					self.connect()
    				    		
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 1):    
					self.keyboard()
					
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() >= 2):
            	
					if self.service == "OpenSubtitles":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) -2 )

					if self.service == "Sublight":
						self.download_subtitles_sub( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 2 )
           	
					if self.service == "Podnapisi":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 2 ) 					

		if self.pos == 3:
			
			
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 0):
    		
					if (self.service == "OpenSubtitles"):
						service = "Sublight"
					if (self.service == "Podnapisi"):
						service = "Sublight"
					if (self.service == "Sublight"):
						service = "OpenSubtitles"
					self.service = service
					self.connect()
    							
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 1):
    		
					if (self.service == "OpenSubtitles"):
						service = "Podnapisi"
					if (self.service == "Podnapisi"):
						service = "OpenSubtitles"
					if (self.service == "Sublight"):
						service = "Podnapisi"
					self.service = service
					self.connect()
    				
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() == 2):    
					self.keyboard()
    			
				if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() >= 3):
            	
					if self.service == "OpenSubtitles":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) -3 )

					if self.service == "Sublight":
						self.download_subtitles_sub( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 3 )
            	
					if self.service == "Podnapisi":
						self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) - 3 ) 
						
						    				


					
		if self.pos == 0:
			if ( self.controlId == SUBTITLES_LIST ) and (self.getControl( SUBTITLES_LIST ).getSelectedPosition() >= 0):
            	
				if self.service == "OpenSubtitles":
					self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) )

				if self.service == "Sublight":
					self.download_subtitles_sub( (self.getControl( SUBTITLES_LIST ).getSelectedPosition()) )
            	
				if self.service == "Podnapisi":
					self.download_subtitles( (self.getControl( SUBTITLES_LIST ).getSelectedPosition())  ) 										   					
	
 
    
    def onFocus( self, controlId ):
    	self.controlId = controlId
	
def onAction( self, action ):
	if ( action.getButtonCode() in CANCEL_DIALOG ):

		self.exit_script()


