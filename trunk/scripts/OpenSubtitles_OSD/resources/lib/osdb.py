import sys
import os
import xmlrpclib
import urllib, urllib2
import unzip
#import globals
from xml.dom import minidom  
from utilities import *
import socket
_ = sys.modules[ "__main__" ].__language__
__settings__ = xbmc.Settings( path=os.getcwd() )


BASE_URL_XMLRPC_DEV = u"http://dev.opensubtitles.org/xml-rpc"
BASE_URL_XMLRPC = u"http://www.opensubtitles.org/xml-rpc"
BASE_URL_SEARCH = u"http://www.opensubtitles.com/%s/search/moviename-%s/simplexml"
BASE_URL_SEARCH_ALL = u"http://www.opensubtitles.com/en/search/sublanguageid-%s/moviename-%s/simplexml"
BASE_URL_SEARCH_OFFSET = u"http://www.opensubtitles.com/en/search/sublanguageid-%s/moviename-%s/offset-40/simplexml"
BASE_URL_DOWNLOAD = u"http://dev.opensubtitles.org/%s"
BASE_URL_SEARCH_HASH = u"http://www.opensubtitles.com/en/search/sublanguageid-%s/moviebytesize-%s/moviehash-%s/simplexml"
def compare_columns(b,a):
        return cmp( b["language_name"], a["language_name"] )  or cmp( a["sync"], b["sync"] ) 

class OSDBServer:
    def Create(self):
	self.subtitles_alt_list = []
	self.subtitles_list = []
	self.subtitles_hash_list = []
	self.subtitles_name_list = []
	self.subtitles_hashalt_list = []

	self.osdb_token = ""
	self.pod_session = ""
	self.connected = False




###-------------------------- Merge Subtitles All -------------################

		
    def mergesubtitles( self ):
        self.subtitles_list = []
        if( len ( self.subtitles_hash_list ) > 0 ):
            for item in self.subtitles_hash_list:
			    if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
			        self.subtitles_list.append( item )

        if( len ( self.subtitles_name_list ) > 0 ):
            for item in self.subtitles_name_list:
			    if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
			        if item["no_files"] < 2:
			        	self.subtitles_list.append( item )

	
        if ( len ( self.subtitles_alt_list ) > 0 ):
             for item in self.subtitles_alt_list:
			    if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
			        if item["no_files"] < 2:
			        	self.subtitles_list.append( item )
			        	
        if ( len ( self.subtitles_hashalt_list ) > 0 ):
             for item in self.subtitles_hashalt_list:
			    if item["format"].find( "srt" ) == 0 or item["format"].find( "sub" ) == 0:
			        self.subtitles_list.append( item )			        	

        if( len ( self.subtitles_list ) > 0 ):
            self.subtitles_list = sorted(self.subtitles_list, compare_columns)



###-------------------------- Opensubtitles Hash -------------################
        

    def searchsubtitles( self, srcstring ,hash, size, lang1,lang2,year ):
	self.subtitles_hash_list = []
	self.allow_exception = False
	self.server = xmlrpclib.Server( "http://www.opensubtitles.org/xml-rpc", verbose=0 )
	LOG( LOG_INFO, "Logging in anonymously to xml-rpc Server" )
	login = self.server.LogIn("", "", "en", "OpenSubtitles_OSD")
	self.osdb_token  = login[ "token" ]
	LOG( LOG_INFO, "Token:[%s]", str(self.osdb_token) )
	self.connected = True
	if lang1 == lang2:
		language = lang1
	else:
		language = lang1 + "," + lang2
	
	try:
		if ( self.osdb_token ) and ( self.connected ):
			
			


			videofilesize = size
			linkhtml_index =  "search/moviebytesize-"+str( videofilesize )+"/moviehash-"+hash
			videohash = hash
			hashresult = {"hash":hash, "filesize":str( videofilesize ), "linkhtml_index":linkhtml_index}
			searchlist = []
			searchlist.append({'sublanguageid':language,'moviehash':hashresult["hash"],'moviebytesize':str( hashresult["filesize"] ) })
			searchstring = {"query":srcstring}
			searchlist1 = []
			searchlist1.append({ 'sublanguageid':language, 'query':srcstring })


			search = self.server.SearchSubtitles( self.osdb_token, searchlist )
			search2 = self.server.SearchSubtitles( self.osdb_token ,searchlist1 )

			if search["data"]:
				for item in search["data"]:
					if item["ISO639"]:
						flag_image = "flags/" + item["ISO639"] + ".gif"
					else:								
						flag_image = "-.gif"

					self.subtitles_hash_list.append({'filename':item["SubFileName"],'link':item["ZipDownloadLink"],"language_name":item["LanguageName"],"language_flag":flag_image,"language_id":item["SubLanguageID"],"ID":item["IDSubtitle"],"rating":str( int( item["SubRating"][0] ) ),"format":item["SubFormat"],"sync":True})
					
					
			if search2["data"]:
				for item in search2["data"]:
					if item["ISO639"]:
						flag_image = "flags/" + item["ISO639"] + ".gif"
					else:								
						flag_image = "-.gif"

					if year == "" : year = 0
					if int(year) > 1930:
						if int(item["MovieYear"]) == int(year):
							self.subtitles_hash_list.append({'filename':item["SubFileName"],'link':item["ZipDownloadLink"],"language_name":item["LanguageName"],"language_flag":flag_image,"language_id":item["SubLanguageID"],"ID":item["IDSubtitle"],"rating":str( int( item["SubRating"][0] ) ),"format":item["SubFormat"],"sync":False})
										


				message =  str( len ( self.subtitles_hash_list )  ) + " subtitles found"
				LOG( LOG_INFO, message )
				return True, message
				
###-------------------------- Opensubtitles Alternative Hash -------------################				
		else: 
			#LOG( LOG_INFO, "Searching subtitles by AltHash for ")

			search_url = BASE_URL_SEARCH_HASH % ( language, size, hash )
			search_url.replace( " ", "+" )
			LOG( LOG_INFO, "AltHash " + search_url )

			socket = urllib.urlopen( search_url )
			result = socket.read()
			socket.close()
			xmldoc = minidom.parseString(result)

			subtitles_althash = xmldoc.getElementsByTagName("subtitle")

			if subtitles_althash:
				url_base = xmldoc.childNodes[0].childNodes[1].firstChild.data
				for subtitle in subtitles_althash:
					filename = ""
					movie = ""
					lang_name = ""
					subtitle_id = ""
					lang_id = ""
					flag_image = ""
					link = ""
					if subtitle.getElementsByTagName("releasename")[0].firstChild:
						filename = subtitle.getElementsByTagName("releasename")[0].firstChild.data
					if subtitle.getElementsByTagName("format")[0].firstChild:
						format = subtitle.getElementsByTagName("format")[0].firstChild.data
						filename = filename + "." +  format
					if subtitle.getElementsByTagName("movie")[0].firstChild:
						movie = subtitle.getElementsByTagName("movie")[0].firstChild.data
					if subtitle.getElementsByTagName("language")[0].firstChild:
						lang_name = subtitle.getElementsByTagName("language")[0].firstChild.data
					if subtitle.getElementsByTagName("idsubtitle")[0].firstChild:
						subtitle_id = subtitle.getElementsByTagName("idsubtitle")[0].firstChild.data
					if subtitle.getElementsByTagName("iso639")[0].firstChild:
						lang_id = subtitle.getElementsByTagName("iso639")[0].firstChild.data
						flag_image = "flags/" + lang_id + ".gif"
					if subtitle.getElementsByTagName("download")[0].firstChild:
						link = subtitle.getElementsByTagName("download")[0].firstChild.data
						link = url_base + link
					if subtitle.getElementsByTagName("subrating")[0].firstChild:
						rating = subtitle.getElementsByTagName("subrating")[0].firstChild.data
				
					if subtitle.getElementsByTagName("files")[0].firstChild:
						no_files = int(subtitle.getElementsByTagName("files")[0].firstChild.data)
				
					self.subtitles_hashalt_list.append({'filename':filename,'link':link,'language_name':lang_name,'language_id':lang_id,'language_flag':flag_image,'movie':movie,"ID":subtitle_id,"rating":str( int( rating[0] ) ),"format":format,"sync":True, "no_files":no_files})

				message =  str( len ( self.subtitles_hashalt_list )  ) + " subtitles found"
				LOG( LOG_INFO, message )
				return True, message
			else: 
				message = "No subtitles found"
				LOG( LOG_INFO, message )
				return True, message
			
	except Exception, e:
		error = _( 731 ) % ( _( 736 ), str ( e ) ) 
		LOG( LOG_ERROR, error )
		return False, "Greska"



###-------------------------- Opensubtitles Second Language -------------################

    def searchsubtitlesbyname_alt( self, name, lang2, lang1 ):
	self.subtitles_alt_list = []
        self.allow_exception = False
        search_url = ""
	try:
		LOG( LOG_INFO, "Searching subtitles by name for " + name )
		if lang1 == lang2 :
			search_url = "http://www.opensubtitles.com/en/search/sublanguageid-" + lang2 +"/moviename-" + name+"/offset-40/simplexml"
		else:
			search_url = "http://www.opensubtitles.com/en/search/sublanguageid-" + lang2 +"/moviename-" + name+"/simplexml"
		#LOG( LOG_INFO, search_url )

		socket = urllib.urlopen( search_url )
		result = socket.read()
		socket.close()
		xmldoc = minidom.parseString(result)

		subtitles_alt = xmldoc.getElementsByTagName("subtitle")

		if subtitles_alt:
			url_base = xmldoc.childNodes[0].childNodes[1].firstChild.data
			for subtitle in subtitles_alt:
				filename = ""
				movie = ""
				lang_name = ""
				subtitle_id = ""
				lang_id = ""
				flag_image = ""
				link = ""
				if subtitle.getElementsByTagName("releasename")[0].firstChild:
					filename = subtitle.getElementsByTagName("releasename")[0].firstChild.data
				if subtitle.getElementsByTagName("format")[0].firstChild:
					format = subtitle.getElementsByTagName("format")[0].firstChild.data
					filename = filename + "." +  format
				if subtitle.getElementsByTagName("movie")[0].firstChild:
					movie = subtitle.getElementsByTagName("movie")[0].firstChild.data
				if subtitle.getElementsByTagName("language")[0].firstChild:
					lang_name = subtitle.getElementsByTagName("language")[0].firstChild.data
				if subtitle.getElementsByTagName("idsubtitle")[0].firstChild:
					subtitle_id = subtitle.getElementsByTagName("idsubtitle")[0].firstChild.data
				if subtitle.getElementsByTagName("iso639")[0].firstChild:
					lang_id = subtitle.getElementsByTagName("iso639")[0].firstChild.data
					flag_image = "flags/" + lang_id + ".gif"
				if subtitle.getElementsByTagName("download")[0].firstChild:
					link = subtitle.getElementsByTagName("download")[0].firstChild.data
					link = url_base + link
				if subtitle.getElementsByTagName("subrating")[0].firstChild:
					rating = subtitle.getElementsByTagName("subrating")[0].firstChild.data
					
				if subtitle.getElementsByTagName("files")[0].firstChild:
					no_files = int(subtitle.getElementsByTagName("files")[0].firstChild.data)
				

				self.subtitles_alt_list.append({'filename':filename,'link':link,'language_name':lang_name,'language_id':lang_id,'language_flag':flag_image,'movie':movie,"ID":subtitle_id,"rating":str( int( rating[0] ) ),"format":format,"sync":False, "no_files":no_files})
			#self.subtitles_list.append ( self.subtitles_alt_list )

			message =  str( len ( self.subtitles_hash_list )  ) + " subtitles found"
			LOG( LOG_INFO, message )
			return True, message
		else: 
			message = "No subtitles found"
			LOG( LOG_INFO, message )
			return True, message

	except Exception, e:
		error = _( 743 ) % ( search_url, str ( e ) ) 
		LOG( LOG_ERROR, error )
		return False, error

###-------------------------- Opensubtitles First Language -------------################


    def searchsubtitlesbyname( self, name, lang1 ):
	self.subtitles_name_list = []
        self.allow_exception = False
	search_url = ""
	
	try:
		LOG( LOG_INFO, "Searching subtitles by name for " + name )
		search_url = "http://www.opensubtitles.com/en/search/sublanguageid-" + lang1 +"/moviename-" + name+"/simplexml"
		search_url.replace( " ", "+" )
		LOG( LOG_INFO, search_url )

		socket = urllib.urlopen( search_url )
		result = socket.read()
		socket.close()
		xmldoc = minidom.parseString(result)

		subtitles = xmldoc.getElementsByTagName("subtitle")
		

		if subtitles:
			url_base = xmldoc.childNodes[0].childNodes[1].firstChild.data
			for subtitle in subtitles:
				filename = ""
				movie = ""
				lang_name = ""
				subtitle_id = ""
				lang_id = ""
				flag_image = ""
				link = ""
				if subtitle.getElementsByTagName("releasename")[0].firstChild:
					filename = subtitle.getElementsByTagName("releasename")[0].firstChild.data
				if subtitle.getElementsByTagName("format")[0].firstChild:
					format = subtitle.getElementsByTagName("format")[0].firstChild.data
					filename = filename + "." +  format
				if subtitle.getElementsByTagName("movie")[0].firstChild:
					movie = subtitle.getElementsByTagName("movie")[0].firstChild.data
				if subtitle.getElementsByTagName("language")[0].firstChild:
					lang_name = subtitle.getElementsByTagName("language")[0].firstChild.data
				if subtitle.getElementsByTagName("idsubtitle")[0].firstChild:
					subtitle_id = subtitle.getElementsByTagName("idsubtitle")[0].firstChild.data
				if subtitle.getElementsByTagName("iso639")[0].firstChild:
					lang_id = subtitle.getElementsByTagName("iso639")[0].firstChild.data
					flag_image = "flags/" + lang_id + ".gif"
				if subtitle.getElementsByTagName("download")[0].firstChild:
					link = subtitle.getElementsByTagName("download")[0].firstChild.data
					link = url_base + link
				if subtitle.getElementsByTagName("subrating")[0].firstChild:
					rating = subtitle.getElementsByTagName("subrating")[0].firstChild.data
					
				if subtitle.getElementsByTagName("files")[0].firstChild:
					no_files = int(subtitle.getElementsByTagName("files")[0].firstChild.data)
				
					
				self.subtitles_name_list.append({'filename':filename,'link':link,'language_name':lang_name,'language_id':lang_id,'language_flag':flag_image,'movie':movie,"ID":subtitle_id,"rating":str( int( rating[0] ) ),"format":format,"sync":False, "no_files":no_files})
			#self.subtitles_list.append ( self.subtitles_name_list )

			message =  str( len ( self.subtitles_hash_list )  ) + " subtitles found"
			LOG( LOG_INFO, message )
			return True, message
		else: 
			message = "No subtitles found"
			LOG( LOG_INFO, message )
			return True, message

	except Exception, e:
		error = _( 743 ) % ( search_url, str ( e ) ) 
		LOG( LOG_ERROR, error )
		return False, error


###-------------------------- Podnapisi Hash -------------################


    def searchsubtitles_pod( self, file, movie_hash, lang1,lang2 ):
	self.subtitles_hash_list = []
        self.allow_exception = False
	podserver = xmlrpclib.Server('http://ssp.podnapisi.net:8000')

	
	lang = []
	lang11 = twotoone(lang1)
	lang22 = twotoone(lang2)
	lang.append(lang11)
	lang.append(lang22)
	hash_pod =[]
	hash_pod.append(movie_hash)

	LOG( LOG_INFO, "Languages : [%s]", str(lang)  )
	LOG( LOG_INFO, "Hash : [%s]", str(hash_pod)  )
	try:

		init = podserver.initiate("OpenSubtitles_OSD")
		try:
			from hashlib import md5 as md5
			from hashlib import sha256 as sha256
		except ImportError:
			from md5 import md5
			import sha256


		username = __settings__.getSetting( "PNuser" )
		password = __settings__.getSetting( "PNpass" )
		
		hash = md5()
		hash.update(password)
		password = hash.hexdigest()
     
		password256 = sha256.sha256(str(password) + str(init['nonce'])).hexdigest()
		if str(init['status']) == "200":
			self.pod_session = init['session']

			auth = podserver.authenticate(self.pod_session, username, password256)
			LOG( LOG_INFO, "Auth : [%s]", str(auth)  )
			
			filt = podserver.setFilters(self.pod_session, True, lang , False)
			LOG( LOG_INFO, "Filter : [%s]", str(filt)  ) 						
			
			search = podserver.search(self.pod_session , hash_pod)

			if str(search['status']) == "200" and len(search['results']) :
				item1 = search["results"]
				item2 = item1[movie_hash]
				item3 = item2["subtitles"]
				title_name = item2["movieTitle"]
				episode = item2["tvEpisode"]
				season = item2["tvSeason"]
				title_year = item2["movieYear"]
				if str(episode) == "0":
					title = str(title_name) + " (" + str(title_year) + ")" 
				else:
					title = str(title_name) + " S ("+ str(season) + ") E (" + str(episode) +")"
				

				for item in item3:

					if item["lang"]:
						flag_image = "flags/" + item["lang"] + ".gif"
					else:								
						flag_image = "-.gif"
					link = 	"http://www.podnapisi.net/ppodnapisi/download/i/" + str(item["id"])
					rating = int(item['rating'])*2
					name = item['release']
					if name == "" : name = title 
					
					if item["inexact"]:
						sync1 = False
					else:
						sync1 = True	
					LOG( LOG_INFO, str(item["inexact"]) )	
					self.subtitles_hash_list.append({'filename':name,'link':link,"language_name":toOpenSubtitles_fromtwo(item["lang"]),"language_flag":flag_image,"language_id":item["lang"],"ID":item["id"],"sync":sync1, "format":"srt", "rating": str(rating) })


				message =  str( len ( self.subtitles_hash_list )  ) + " subtitles found"
				LOG( LOG_INFO, message )
				return True, message
			else: 
				message = "No subtitles found Podnapisi_hash"
				LOG( LOG_INFO, message )
				return True, message



	except Exception, e:
		error = "Greska"
		LOG( LOG_ERROR, error )
		return False, error




###-------------------------- Podnapisi By Name -------------################

    def searchsubtitlesbyname_pod( self, name, lang1,lang2,year ):
	from utilities import *
	self.subtitles_name_list = []
        self.allow_exception = False
	search_url = ""
	season = ""
	episode = ""
	title1 = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")
	title = title1.replace(" ","+")
	if year == 0 : year = ""
	tbsl = "1"
	lang_num1 = twotoone(lang1)
	lang_num2 = twotoone(lang2)
	LOG( LOG_INFO, "PodLang"+lang_num1+lang_num2 )
	if len(title) > 1:
		name = title
		season = xbmc.getInfoLabel("VideoPlayer.Season")
		episode = xbmc.getInfoLabel("VideoPlayer.Episode")
		
	BASE_URL_SEARCH_POD = "http://www.podnapisi.net/ppodnapisi/search?tbsl=1&sK=" + name + "&sJ=" +lang_num1+ "&sY=" + str(year)+ "&sTS=" + str(season) + "&sTE=" + str(episode) + "&sXML=1"
	BASE_URL_SEARCH_POD1 = "http://www.podnapisi.net/ppodnapisi/search?tbsl=1&sK=" + name + "&sJ=" +lang_num2+ "&sY=" + str(year)+ "&sTS=" + str(season) + "&sTE=" + str(episode) + "&sXML=1"

	try:
		LOG( LOG_INFO, "Searching subtitles by name_pod for " + name )
		search_url = BASE_URL_SEARCH_POD 
		search_url1 = BASE_URL_SEARCH_POD1
		search_url.replace( " ", "+" )
		LOG( LOG_INFO, search_url )

		socket = urllib.urlopen( search_url )
		result = socket.read()
		socket.close()
		xmldoc = minidom.parseString(result)
		
		subtitles = xmldoc.getElementsByTagName("subtitle")
		
		socket = urllib.urlopen( search_url1 )
		result = socket.read()
		socket.close()
		
		xmldoc = minidom.parseString(result)
		
		subtitles1 = xmldoc.getElementsByTagName("subtitle")
		
		subtitles = subtitles + subtitles1		
		if subtitles:
			url_base = "http://www.podnapisi.net/ppodnapisi/download/i/"

			for subtitle in subtitles:
				filename = ""
				movie = ""
				lang_name = ""
				subtitle_id = 0
				lang_id = ""
				flag_image = ""
				link = ""
				format = "srt"
				no_files = ""
				if subtitle.getElementsByTagName("title")[0].firstChild:
					movie = subtitle.getElementsByTagName("title")[0].firstChild.data

				if subtitle.getElementsByTagName("release")[0].firstChild:
					filename = subtitle.getElementsByTagName("release")[0].firstChild.data
					if len(filename) < 2 :
						filename = movie
				else:
					filename = movie

				filename = filename + "." +  format
				rating = 0
				if subtitle.getElementsByTagName("rating")[0].firstChild:
					rating = subtitle.getElementsByTagName("rating")[0].firstChild.data
					rating = int(rating)*2			
				

				if subtitle.getElementsByTagName("languageName")[0].firstChild:
					lang_name = subtitle.getElementsByTagName("languageName")[0].firstChild.data
				if subtitle.getElementsByTagName("id")[0].firstChild:
					subtitle_id = subtitle.getElementsByTagName("id")[0].firstChild.data

				flag_image = "flags/" + toOpenSubtitles_two(lang_name) + ".gif"

				link = url_base + str(subtitle_id)

				if subtitle.getElementsByTagName("cds")[0].firstChild:
					no_files = int(subtitle.getElementsByTagName("cds")[0].firstChild.data)
				
					
				self.subtitles_name_list.append({'filename':filename,'link':link,'language_name':lang_name,'language_id':lang_id,'language_flag':flag_image,'movie':movie,"ID":subtitle_id,"rating":str(rating),"format":format,"sync":False, "no_files":no_files})

			message =  str( len ( self.subtitles_name_list )  ) + " subtitles found"
			LOG( LOG_INFO, message )
			return True, message
		else: 
			message = "No subtitles found"
			LOG( LOG_INFO, message )
			return True, message

	except Exception, e:
		error = _( 743 ) % ( search_url, str ( e ) ) 
		LOG( LOG_ERROR, error )
		return False, error

