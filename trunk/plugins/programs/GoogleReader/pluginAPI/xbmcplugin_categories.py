"""
	Category module: list of categories to use as folders
"""

# main imports
import os, sys
import time
#from pprint import pprint
from string import find
import xbmc, xbmcgui, xbmcplugin
from urllib import unquote_plus

from pluginAPI.xbmcplugin_const import *
from pluginAPI.bbbLib import *
import pluginAPI.GoogleReaderClient as grc

__plugin__ = sys.modules[ "__main__" ].__plugin__
__lang__ = xbmc.Language( HOME_DIR ).getLocalizedString

#################################################################################################################
class _Info:
	def __init__(self, *args, **kwargs ):
		self.__dict__.update( kwargs )
		log( "Info() self.__dict__=%s" % self.__dict__ )
	def has_key(self, key):
		return self.__dict__.has_key(key)


#################################################################################################################
#################################################################################################################
class Main:
	# base paths
	BASE_PLUGIN_THUMBNAIL_PATH = os.path.join( HOME_DIR, "thumbnails" )
	DEFAULT_THUMB_IMAGE = os.path.join(HOME_DIR,"default.tbn")
	NEXT_IMG =  os.path.join( BASE_PLUGIN_THUMBNAIL_PATH, "next.png" )
	TAGS_FILENAME = "/".join( [TEMP_DIR, __plugin__+"_tags.dat"] )
	SUBS_FILENAME = "/".join( [TEMP_DIR, __plugin__+"_subs.dat"] )

	def __init__( self ):
		self._parse_argv()                      # parse sys.argv

		if not self.loadSettings():
			return

		if ( not sys.argv[ 2 ] ):
			# cleanup for new start
			deleteFile(self.TAGS_FILENAME)
			deleteFile(self.SUBS_FILENAME)
			files = os.listdir(TEMP_DIR)
			for f in files:
				if f.startswith(__plugin__+"_items_"):
					deleteFile(os.path.join(TEMP_DIR, f))

			self.client =  grc.GoogleReaderClient()
			if not self.authenticate():     	# authenticate user
				return
			ok = self.get_categories( )
		else:
			# not first run
			# load saved google authkey
			SID = xbmcplugin.getSetting( "authkey" )
			log("loaded SID=%s" % SID)
			# create client with known key
			self.client =  grc.GoogleReaderClient(SID, \
									pagesize=xbmcplugin.getSetting( "pagesize" ), \
									show_read=bool(xbmcplugin.getSetting( "show_read" ) == "true"))
			exec "ok = self.%s()" % ( self.args.category, )

		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok)

	########################################################################################################################
	def _parse_argv(self):
		if ( not sys.argv[ 2 ] ):
			self.args = _Info( title="" )
		else:
			# call Info() with our formatted argv to create the self.args object
			# replace & with , first as they're the args split char.  Then decode.
			try:
				exec "self.args = _Info(%s)" % ( unquote_plus( sys.argv[ 2 ][ 1 : ].replace( "&", ", " ) ), )
			except Exception, e:
				print str(e)

	########################################################################################################################
	def authenticate( self ):
		log( " > authenticate()")
		ok = False
		# make the authentication call
		try:
			authkey = self.client.authenticate( self.email, self.password )
			if authkey and authkey.startswith("ERROR"): raise "neterror", authkey
			if not authkey:
				messageOK(__plugin__, __lang__(30904))
			else:
				try:
					xbmcplugin.setSetting( "authkey", authkey )
					ok = True
				except: pass
		except "neterror", e:
			messageOK(__plugin__, e)

		log( "< authenticate() ok=%s" % ok)
		return ok

	########################################################################################################################
	def loadSettings(self):
		log( " > loadSettings()")

		def _checkSettings():
			# check mandatory settings are set
			self.email = xbmcplugin.getSetting( "user_email" )
			self.password = xbmcplugin.getSetting( "user_password" )
			ok = bool( self.email and self.password )
			log(" _checkSettings() ok=%s" % ok)
			return ok

		ok = _checkSettings()
		if not ok:
			# call settings menu - if xbmc builds has feature
			try:
				if ( os.environ.get( "OS", "n/a" ) == "xbox" ):
					xbmc.sleep( 2000 )
				xbmcplugin.openSettings(sys.argv[0])
				ok = _checkSettings()
			except:
				# builtin missing from build - inform user to use ContextMenu for settings
				messageOK(__plugin__, __lang__(30901), __lang__(30902), __lang__(30903))

		log( "< loadSettings() ok=%s" % ok)
		return ok

	########################################################################################################################
	def get_categories( self ):
		log( " > get_categories()")
		try:
			ok = True
			categories = (
					( __lang__( 30950 ), "get_subs", None, ),
					( __lang__( 30951 ), "select_subs_tag",  None,),
					( __lang__( 30952 ), "get_items_by_type",  "reading",),                 # all item
					( __lang__( 30953 ), "select_items_tag",  None,),                       # items by label
					( __lang__( 30954 ), "get_items_by_type", "starred", ),
					( __lang__( 30955 ), "get_items_by_type", "shared", ),
					( __lang__( 30956 ), "get_items_by_type", "notes", ),
					( __lang__( 30957 ), "select_search_tag", None, )
				)

			sz = len( categories )
			for ( ltitle, method, method_arg ) in categories:
				# set the callback url
				url = '%s?title=%s&category=%s' % ( sys.argv[ 0 ], encodeText( ltitle ), repr( method ), )
				if method_arg:
					url += "&method_arg=%s" % repr (method_arg )

				# only need to add label, icon and thumbnail, setInfo() and addSortMethod() takes care of label2
				li=xbmcgui.ListItem( ltitle )
				# add the item to the media list
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=url, listitem=li, isFolder=True, totalItems=sz )

			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
			xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files")
			xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
		except:
			handleException(self.__class__.__name__)
			ok = False

		log( "< get_categories() ok=%s" % ok)
		return ok

	########################################################################################################################
	def _get_tags_file(self):
		""" Download or Load from file, list of tags """
		log("> _get_tags_file()")
		tags = []
		try:
			if os.path.isfile(self.TAGS_FILENAME):
				tags = loadFileObj(self.TAGS_FILENAME, [])
			else:
				xmlObject = self.client.get_tag_list()
				if xmlObject and xmlObject.startswith("ERROR"): raise "neterror", xmlObject
				if xmlObject:
					result = grc.GoogleObject(xmlObject).parse()
#					pprint (result)
					for item in result['tags']:
						tags.append(item['id'].split('/')[-1])		# get tag at end of id url

					# save to file
					if tags:
						saveFileObj(self.TAGS_FILENAME, tags)
		except "neterror", e:
			messageOK(__plugin__, e)
		except:
			handleException(self.__class__.__name__)
		sz = len(tags)
		log("< _get_tags_file() tags count=%d" % sz)
		return tags, sz

	########################################################################################################################
	def select_subs_tag( self ):
		return self.select_tag('get_subs')

	########################################################################################################################
	def select_items_tag( self ):
		return self.select_tag('get_items_by_type')

	########################################################################################################################
	def select_search_tag(self):
		return self.select_tag('search')

	########################################################################################################################
	def select_tag( self, method):
		""" Select a tag and setup next listitem url call using given method """
		log("> select_tag() method=" + method)
		ok = False

		try:
			tags, sz = self._get_tags_file()
			if not tags: raise "empty"
			title = self.args.title + ": "
			# add SEARCH ALL if method is search
			if method == 'search':
				tags.insert(0,'0 - Search All')

			for tag in tags:
				# set the callback url
				li_url = '%s?title=%s&category=%s&tag=%s' % \
						( sys.argv[ 0 ], encodeText( title+tag ), repr( method ), encodeText( tag ), )
				li=xbmcgui.ListItem( tag )
				# add the item to the media list
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=li_url, listitem=li, isFolder=True, totalItems=sz )

			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
			xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files")
			xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
		except "empty":
			messageOK(self.args.title, __lang__(90307))
		except:
			handleException(self.__class__.__name__)
			ok = False

		log( "< select_tag() ok=%s" % ok)
		return ok

	########################################################################################################################
	def get_subs(self):
		log("> get_subs()")
		ok = False

		try:
			subs, sz = self._get_subs_file()
#			pprint (subs)
			if not subs: raise "empty"

			# get args tag
			li_details = []
			try:
				# if have tag - find all subs by tag
				tag = self.args.tag
				log( "tag=" + tag )
				for sub in subs:
#					print "sub['categories']=", sub['categories']
					for category in sub['categories']:
						if tag == category['label']:
							li_details.append( (sub['title'], sub['id'] ) )
							break
			except:
				# no tag - get all subs
				for sub in subs:
					li_details.append( (sub['title'], sub['id'] ) )

			if not li_details: raise "empty"

			# loop throu all entries making listitems
			for title, id in li_details:
				li_url = '%s?title=%s&category=%s&feed=%s' % \
							( sys.argv[ 0 ], encodeText( title ), repr( 'get_items_by_type' ), encodeText( id ), )
				li=xbmcgui.ListItem( decodeText(title) )
				# add the item to the media list
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=li_url, listitem=li, isFolder=True, totalItems=sz )

			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
			xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="files")
			xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
		except "empty":
			messageOK(self.args.title, __lang__(30905))
		except:
			handleException(self.__class__.__name__)
			ok = False

		log( "< get_subs() ok=%s" % ok)
		return ok

	########################################################################################################################
	def _get_subs_file(self):
		""" Download or Load from file, subscriptions list """
		log("> _get_subs_file()")
		data = []
		try:
			if os.path.isfile(self.SUBS_FILENAME):
				data = loadFileObj(self.SUBS_FILENAME, [])
			else:
				xmlObject = self.client.get_subscription_list()
				if xmlObject and xmlObject.startswith("ERROR"): raise "neterror", xmlObject
				if xmlObject:
					result = grc.GoogleObject(xmlObject).parse()
					# extract subs
					data = result.get('subscriptions', [])
					if data:
						# save to file
						saveFileObj(self.SUBS_FILENAME, data)
		except "neterror", e:
			messageOK(__plugin__, e)
		except:
			handleException(self.__class__.__name__)

		sz = len(data)
		log("< _get_subs_file() tags count=%d" % sz)
		return data, sz

	########################################################################################################################
	def get_items_by_type( self ):
		""" Make a list of all items, selected by type. Uses continuation pages. """
		log("> get_items_by_type()")
		ok = False

		try:
			# use 'next page' continuation if supplied with args
			try:
				continuation = self.args.continuation
			except:
				continuation = ''

			atomfeed = None
			arg_key = ''
			arg_value = ''
			# fetch items according to addition args 'method_arg' or 'tag'
			if self.args.has_key('method_arg'):
				arg_key = 'method_arg'
				arg_value = self.args.method_arg
				log("method_arg=%s" % arg_value)
				if arg_value == 'starred':
					atomfeed = self.client.get_starred(continuation)
				elif arg_value == 'shared':
					atomfeed = self.client.get_shared(continuation)
				elif arg_value == 'notes':
					atomfeed = self.client.get_notes(continuation)
				elif arg_value == 'reading':
					atomfeed = self.client.get_reading_list(continuation)
				else:
					log("unknown method_arg!")

			elif self.args.has_key('tag'):
				arg_key = 'tag'
				arg_value = self.args.tag
				log("tag=%s" % arg_value)
				atomfeed = self.client.get_reading_tag_list(arg_value, continuation)

			elif self.args.has_key('feed'):
				arg_key = 'feed'
				arg_value = self.args.feed
				log("feed=%s" % arg_value)
				atomfeed = self.client.get_feed(arg_value, continuation=continuation)

			if atomfeed and atomfeed.startswith("ERROR"): raise "neterror", atomfeed

			xmlfeed = grc.GoogleFeed(atomfeed)
			sz = xmlfeed.get_size()
			log("xmlfeed sz=%d" % sz)
			if not sz: raise "empty"

			# process entires
			self.args.title = xmlfeed.get_title()
			# another page ?
			continuation = xmlfeed.get_continuation()
			if continuation:
				# callback to this, using new continuation
				# NB title already url encoded at this point
				li_url = '%s?title=%s&category=%s&continuation=%s' % \
						( sys.argv[ 0 ], repr( self.args.title), repr( 'get_items_by_type' ), repr( continuation ))
				# add additional args as per orig call
				if arg_key:
					li_url += '&%s=%s' % (arg_key, encodeText( arg_value ))

				li=xbmcgui.ListItem( __lang__(30921), "", self.NEXT_IMG, self.NEXT_IMG )	# next page
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=li_url, listitem=li, isFolder=True, totalItems=sz)

			ok = self._fill_item_list(xmlfeed, continuation)
		except "empty":
			messageOK(decodeText(self.args.title), __lang__(30906))
		except "neterror", e:
			messageOK(__plugin__, e)
		except:
			handleException(self.__class__.__name__)
			ok = False

		log( "< get_items_by_type() ok=%s" % ok)
		return ok

	########################################################################################################################
	def search(self):
		log("> search()")
		ok = False

		try:
			if self.args.has_key('searchText'):
				text = self.args.searchText
			else:
				text = ''
			text = self._get_keyboard(text)
			if text:
				self.args.searchText = text

				if 'Search All' in self.args.tag:
					jsonString = self.client.search_all_items(text)
				else:
					jsonString = self.client.search_label(text, self.args.tag)
				if jsonString and jsonString.startswith("ERROR"): raise "neterror", jsonString

				grso = grc.GoogleReaderSearchObject(jsonString)
				sz = grso.get_size()
				log("search results sz=%d" % sz)
				if not sz: raise "empty"

				ok = self._fill_item_list(grso)
		except "empty":
			messageOK(decodeText(self.args.title), __lang__(30906))
		except "neterror", e:
			messageOK(__plugin__, e)
		except:
			handleException(self.__class__.__name__)
			ok = False

		log("< search()")
		return ok

	########################################################################################################################
	def _fill_item_list(self, xmlfeed, continuation=''):
		log("> _fill_item_list() continuation=%s" % continuation)
		ok = False

		try:        
			sz = xmlfeed.get_size()
			log("_fill_item_list() items sz=%d" % sz)
			if not sz: raise "empty"

			# loop throu all entries making listitems
			download_images = bool(xbmcplugin.getSetting( "list_images" ) == "true")
			saveEntries = {}
			for entry in xmlfeed.get_entries():
#				print "entry="
#				pprint (entry)
				google_id = entry['google_id']
				if not google_id:
					continue
				updated = entry.get('updated','')
				if not updated:
					updated = entry.get('published','')
				updated = time.strftime("%d-%m-%Y %H:%M", time.localtime(updated))
				title = cleanHTML(entry['title'])
				sourceTitle = decodeText(entry['sources'].values()[0][1])		# [first source](id, title)
				author = entry.get('author','')
				content = entry.get('content','')
				if not content:
					content = entry.get('summary','')
				thumbnail = findImgSrc(content)											# find first image in content
				# only fetch image if settings permit, but image always fetched when item shown
				thumbnail = get_thumbnail(thumbnail, download_images)			# load or download
				content = cleanHTML(content)

				# store these clean values to our saved entry
				cleanEntry = {}
				cleanEntry['updated'] = updated
				cleanEntry['title'] = title
				cleanEntry['content'] = content
				cleanEntry['author'] = author
				cleanEntry['image'] = thumbnail
				saveEntries[google_id] = cleanEntry
#				pprint (cleanEntry)

				# continuation in this url is used to form a unique items filename that can be loaded when item selected
				li_url = '%s?title=%s&category=%s&google_id=%s&continuation=%s' % \
							(sys.argv[ 0 ], encodeText( entry['title'] ), repr('show_item'), repr( entry['google_id'] ), repr( continuation ))

				if thumbnail.startswith('http') and not download_images:
					thumbnail = self.DEFAULT_THUMB_IMAGE
				if thumbnail:
					li=xbmcgui.ListItem( title, sourceTitle, thumbnail, thumbnail )
				else:
					li=xbmcgui.ListItem( title, sourceTitle )
				li.setInfo( "video", { "Title": title, "Date": updated[:10], "Director": author, "Plot": content, "Genre": sourceTitle} )
				# add the item to the media list
				ok = xbmcplugin.addDirectoryItem( handle=int( sys.argv[ 1 ] ), url=li_url, listitem=li, isFolder=False, totalItems=sz )

#			pprint (saveEntries)
			# save to file so we can read it in if an item selected
			saveFileObj(ITEMS_FILENAME % continuation, saveEntries)

			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
			xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
			xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="videos")
			xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=self.args.title )
		except "empty":
			messageOK(decodeText(self.args.title), __lang__(30906))
		except:
			handleException(self.__class__.__name__)
			ok = False

		log( "< _fill_item_list() ok=%s" % ok)
		return ok


	########################################################################################################################
	def _get_keyboard(self, default="", heading="", isHidden=False):
		if not heading:
			heading = self.args.title
		kb = xbmc.Keyboard(default, heading, isHidden)
		kb.doModal()
		if kb.isConfirmed():
			text = kb.getText().strip()
			log("_get_keyboard() " + text)
			return text
		else:
			return ''
