"""
 Get services from Google Reader
"""
import urllib  
import urllib2  
import re
import sys
import time
from xml.dom import minidom
#from pprint import pprint
import traceback

def log(msg):
	if True:
		print msg

GOOGLE_SCHEME = 'http://www.google.com'
ATOM_PREFIXE_USER = 'user/-/'
ATOM_PREFIXE_USER_NUMBER = 'user/'+'0'*20+'/'

# search All Items
# URL=http://www.google.com/reader/api/0/search/items/ids?q=yamaha&num=1000&output=json&ck=1239194610062&client=scroll

# search Read items
# URL=http://www.google.com/reader/api/0/search/items/ids?q=yamaha&num=1000&s=user%2F13198985849186505357%2Fstate%2Fcom.google%2Fread&output=json&ck=1239194664734&client=scroll

# search notes
# URL=http://www.google.com/reader/api/0/search/items/ids?q=yamaha&num=1000&s=user%2F13198985849186505357%2Fstate%2Fcom.google%2Fcreated&output=json&ck=1239194444748&client=scroll

# search label
# URL=http://www.google.com/reader/api/0/search/items/ids?q=yamaha&num=1000&s=user%2F13198985849186505357%2Flabel%2Faudiovideo&output=json&ck=1239193799534&client=scroll

# search feed
# URL=http://www.google.com/reader/api/0/search/items/ids?q=yamaha&num=1000&s=feed%2Fhttp%3A%2F%2Fwww.avreview.co.uk%2Fnews%2Frss.asp&output=json&ck=1239194372139&client=scroll

# search contents for each id
# URL=http://www.google.com/reader/api/0/stream/items/contents?ck=1239232302557&client=scroll
# POST=i=<item id>

class GoogleReaderClient:

	reader_url = GOOGLE_SCHEME + '/reader'  
	login_url = 'https://www.google.com/accounts/ClientLogin'
	list_url = reader_url + '/atom/user/-/state/com.google/'
	api_url = reader_url + '/api/0/'
	exclude_read_url = 'user/-/state/com.google/read'

	reading_tag_url = reader_url + '/atom/user/-/label/%s'  
	get_feed_url = reader_url + '/atom/feed/'
	reading_url = list_url + 'reading-list'  
	read_items_url = list_url + 'read'  
	starred_url = list_url + 'starred'  
	shared_url = list_url + 'broadcast'  
	notes_url = list_url + 'created'  
	token_url = api_url + 'token'  
	subscription_list_url = api_url + 'subscription/list'  
	subscription_url = api_url + 'subscription/edit'
	tag_list_url = api_url + 'tag/list'
	search_url = api_url + 'search/items/ids'
	search_contents_url = api_url + 'stream/items/contents'

	def __init__( self, SID='', email='', password='', source='XBMC GoogleReader', pagesize=20, show_read=True ):

		self.source = source
		if not SID and email and password:
			self.authenticate(email, password)
		else:
			self.SID = SID
		self.pagesize = pagesize
		self.show_read = show_read

	def setSID(self, SID):
		self.SID = SID

	def setPageSize(self, pagesize):
		self.pagesize = pagesize

	def setShowRead(self, show_read):
		self.show_read = show_read

	def retrieve(self, url, header={}, post_data=None):
		if post_data:
			post_data = urllib.urlencode(post_data)

		print "retrieve() url=%s" % url
#		print "retrieve() header=%s" % header.items()
#		print "retrieve() post_data=%s" % post_data

		try :
			request = urllib2.Request(url, post_data, header)
			f = urllib2.urlopen( request )
			result = f.read()
			f.close()
		except:
			result = 'ERROR: %s' % sys.exc_info()[ 1 ]
#		print result
		return result

	#login / get SID
	def authenticate(self, email, password):
		self.SID = ''
		header = {'User-agent' : self.source}
		post_data = { 'Email': email, 'Passwd': password, 'service': 'reader', 'source': self.source, 'continue': GOOGLE_SCHEME, }
		result = self.retrieve(self.login_url, header, post_data)
		if result and not result.startswith('ERROR'):
			try:
				self.SID = re.search('SID=(\S*)', result).group(1) 
			except: pass
#			print "authenticate() SID=%s" % self.SID
			return self.SID
		else:
			return result

	#get results from url
	def get_results(self, url, post_data=None):
		if self.SID:
			header = {'User-agent' : self.source}
			header['Cookie']='Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % self.SID
			return self.retrieve(url, header, post_data)
		else:
			print "get_results() Error: SID missing!"
			return None

	#get a token, this is needed for modifying to reader
	def get_token(self):
		return self.get_results(self.token_url)

	#get a specific feed.  It works for any feed, subscribed or not
	def get_feed(self, url, continuation=None, **kwargs):
		# url that have come from subscriptions list may be prefixed with 'feed/' remove it
		url = self.get_feed_url + url.replace('feed/http','http')
		url = self._add_api_get_params(url, continuation, self.show_read)
		if kwargs:
			url += urllib.urlencode(urlargs)
		return self.get_results(url.encode('utf-8'))

	#get a list of the users subscribed feeds
	def get_subscription_list(self):
		return self.get_results(self.subscription_list_url)

	#get a list of the label tags
	def get_tag_list(self):
		return self.get_results(self.tag_list_url)

	#get a feed of the users unread items    
	def get_reading_list(self, continuation=None):
		url = self._add_api_get_params(self.reading_url, continuation, self.show_read)
		return self.get_results(url)

	#get a feed of the users read items    
	def get_read_items(self, continuation=None):
		url = self._add_api_get_params(self.read_items_url, continuation, showRead=True)
		return self.get_results(url)
		
	#get a feed of the users unread items of a given tag    
	def get_reading_tag_list(self, tag, continuation=None):
		url = self.reading_tag_url % tag.replace(" ","%20")
		url = self._add_api_get_params(url, continuation, self.show_read)
		return self.get_results(url.encode('utf-8'))

	#get a feed of a users starred items/feeds
	def get_starred(self, continuation=None):
		url = self._add_api_get_params(self.starred_url, continuation, self.show_read)
		return self.get_results(url)

	#get a feed of a users shared items/feeds
	def get_shared(self, continuation=None):
		url = self._add_api_get_params(self.shared_url, continuation, self.show_read)
		return self.get_results(url)

	#get a feed of a users shared items/feeds
	def get_notes(self, continuation=None):
		url = self._add_api_get_params(self.notes_url, continuation, self.show_read)
		return self.get_results(url)

	#subscribe of unsubscribe to a feed    
	def modify_subscription(self, what, do):
	#    url = subscription_url + '?client=client:%s&ac=%s&s=%s&token=%s' % \
	#                  ( login, do.encode('utf-8'), 'feed%2F' + what.encode('utf-8'), get_token() )
		url = self.subscription_url + '?client=%s' % self.source
		post_data = { 'ac' : do, 's' : "feed/"+what, 'T' : self.get_token() }
		return self.get_results(url, post_data)
		
	#subscribe to a feed
	def subscribe_to(self, url):
		return modify_subscription(url, 'subscribe')

	#unsubscribe to a feed
	def unsubscribe_from(self, url):
		return modify_subscription(url, 'unsubscribe')

	# search All Items
	def search_all_items(self, text):
		return self.search(text)

	# search by label
	def search_label(self, text, what):
		return self.search(text, 'user/-/label/' + what)

	# search by feed
	def search_feed(self, text, what):
		return self.search(text, 'user/-/feed/' + what)

	# search Notes
	def search_notes(self, text):
		return self.search(text, 'user/-/state/com.google/created/')

	# search Read
	def search_read(self, text):
		return self.search(text, 'user/-/state/com.google/read/')

	# search
	def search(self, text, what=''):
		url = "%s?q=%s" % (self.search_url, urllib.quote_plus(text.replace("'", "\\u0027")))
		if what:
			url += "&s=%s" % urllib.quote_plus(what.replace("'", "\\u0027"))
		url += "&num=250&output=xml"
		url = self._add_api_get_params(url, None, True)		# no continuation, incl read
		results = self.get_results(url.encode('utf-8'))
		if results and not results.startswith("ERROR"):
			# parse ids from result
			reObj = re.compile('"id">(.*?)<',re.IGNORECASE)
			idList = reObj.findall(results)
			if idList:
				return self.get_search_contents(idList)	# returns json string
			else:
				return None

		return results

	def get_search_contents(self, idList):
		post = []
		for id in idList:
			post.append( ('i', id) )
		post.append( ('T', self.get_token() ) )	# mandatory
		url = self._add_api_get_params(self.search_contents_url)
		return self.get_results(url, post)

	# append additional GET params
	def _add_api_get_params(self, url, continuation='', showRead=True):
		if url.find("?") == -1:
			url += "?"
		else:
			url += "&"
		url += "n=%s&ck=%d" % (self.pagesize, int(time.time()))
		if continuation:
			url += "&c=%s" % continuation
		if not showRead:
			url += "&xt=%s" % self.exclude_read_url
		return url

class GoogleFeed(object) :
	""" Uses a recursive Generator to parse XML """
	def __init__(self,xmlfeed) :
		# Need a lot more check !!!
		self._entries = []
		self._properties = {}
		self._continuation = None
		self._document = None
		self._isotime_pos = [(0,4),(5,7),(8,10),(11,13),(14,16),(17,19)]

		try:
			if xmlfeed:
				self._document = minidom.parseString(xmlfeed)
				for feedelements in self._document.childNodes[0].childNodes :
					if feedelements.localName == 'entry' :
						self._entries.append(feedelements)
					elif feedelements.localName == 'continuation' :
						self._continuation = feedelements.firstChild.data
					else :
						self._properties[feedelements.localName] = feedelements
		except:
			print "GoogleFeed() " + str(sys.exc_info()[ 1 ])
			
	def get_size(self):
		return len(self._entries)
	def get_title(self) :
		if 'title' in self._properties :
			return self._properties['title'].childNodes[0].data
	def get_entries(self) :
		for dom_entry in self._entries :
			entry = {}
			entry['categories'] = {}
			entry['sources'] = {}
			entry['crawled'] = int(dom_entry.getAttribute('gr:crawl-timestamp-msec'))
			for dom_entry_element in dom_entry.childNodes :
				if dom_entry_element.localName == 'id' :
					entry['google_id'] = dom_entry_element.firstChild.data
					entry['original_id'] = dom_entry_element.getAttribute('gr:original-id')
				elif dom_entry_element.localName == 'link' :
					if dom_entry_element.getAttribute('rel')=='alternate' :
						entry['link'] = dom_entry_element.getAttribute('href')
				elif dom_entry_element.localName == 'category' :
					if dom_entry_element.getAttribute('scheme')==GOOGLE_SCHEME :
						term = dom_entry_element.getAttribute('term')
						digit_table = {
							ord('0'):ord('0'),
							ord('1'):ord('0'),
							ord('2'):ord('0'),
							ord('3'):ord('0'),
							ord('4'):ord('0'),
							ord('5'):ord('0'),
							ord('6'):ord('0'),
							ord('7'):ord('0'),
							ord('8'):ord('0'),
							ord('9'):ord('0'),
							}
						if term.translate(digit_table).startswith(ATOM_PREFIXE_USER_NUMBER) :
							term = ATOM_PREFIXE_USER + term[len(ATOM_PREFIXE_USER_NUMBER):]
						entry['categories'][term] = dom_entry_element.getAttribute('label')
				elif dom_entry_element.localName == 'summary' :
					entry['summary'] = dom_entry_element.firstChild.data
				elif dom_entry_element.localName == 'content' :
					entry['content'] = dom_entry_element.firstChild.data
				elif dom_entry_element.localName == 'author' :
					entry['author'] = dom_entry_element.getElementsByTagName('name')[0].firstChild.data
				elif dom_entry_element.localName == 'title' :
					entry['title'] = dom_entry_element.firstChild.data
				elif dom_entry_element.localName == 'source' :
					stream_id = dom_entry_element.getAttribute('gr:stream-id')
					# { streamid : [ google stream id, title ], ... }
					entry['sources'][stream_id] = ( dom_entry_element.getElementsByTagName('id')[0].firstChild.data, dom_entry_element.getElementsByTagName('title')[0].firstChild.data )
				elif dom_entry_element.localName == 'published' :
					entry['published'] = self.iso2time(dom_entry_element.firstChild.data)
				elif dom_entry_element.localName == 'updated' :
					entry['updated'] = self.iso2time(dom_entry_element.firstChild.data)
			for entry_key in ('link','summary','author','title') :
				if entry_key not in entry :
					entry[entry_key] = u''
			for entry_key in ('published','updated','crawled') :
				if entry_key not in entry :
					entry[entry_key] = None
			if 'content' not in entry :
				entry['content'] = entry['summary']
			yield entry
	def get_continuation(self) :
		return self._continuation
	def iso2time(self,isodate) :
		# Ok, it's unreadable ! So, I have z == '2006-12-17T12:07:19Z',
		# I take z[0:4] and z[5:7] and etc.,
		# ('2006','12', etc.)
		# I convert them into int, And I add [0,0,0]
		# Once converted in tuple, I got (2006,12,17,12,07,19,0,0,0), which is what mktime want...
		return time.mktime(tuple(map(lambda x:int(isodate.__getslice__(*x)),self._isotime_pos)+[0,0,0]))

class GoogleObject(object) :
	""" This class aims at reading 'object' xml structure.
		Look like it's based on something jsoinsable.
		( http://json.org/ )
		Yes I'm a moron ( in the sense defined by the asshole/moron spec
		http://www.diveintomark.org/archives/2004/08/16/specs ),
		which means everything is just supposition.

		A json can contains only string, number, object, array, true,
		false, null.

		It look like Google Reader use string for true and false.
		Never seen 'null' neither.

		A GoogleObject can only contains string, number, object, array
		"""
	def __init__(self,xmlobject) :
		""" 'xmlobject' is the string containing the answer from Google as
			an object jsonizable. """
		self._document = minidom.parseString(xmlobject)
	def parse(self) :
		""" 'parse' parse the object and return the pythonic version of
			the object. """
		return self._parse_dom_element(self._document.childNodes[0])
	def _parse_dom_element(self,dom_element) :
		value = None
		if dom_element.localName == 'object' :
			value = {}
			for childNode in dom_element.childNodes :
				if childNode.localName != None :
					name = childNode.getAttribute('name')
					value[name] = self._parse_dom_element(childNode)
		elif dom_element.localName == 'list' :
			value = []
			for childNode in dom_element.childNodes :
				if childNode.localName != None :
					value.append(self._parse_dom_element(childNode))
		elif dom_element.localName == 'number' :
			value = int(dom_element.firstChild.data)
		elif dom_element.localName == 'string' :
			value = dom_element.firstChild.data
		# let's act as a total moron : Never seen those balise, but
		# I can imagine them may exist by reading http://json.org/
		elif dom_element.localName == 'true' :
			value = True
		elif dom_element.localName == 'false' :
			value = False
		elif dom_element.localName == 'null' :
			value = None
		return value

class GoogleReaderSearchObject(object):
	""" hacky way of decoding a json object """

	def __init__(self, jsonString):
		try:
			self.jsonItems = eval(jsonString.replace(':true',':True'))['items']
		except:
			print "GoogleReaderSearchObject() " + str(sys.exc_info()[ 1 ])
			self.jsonItems = []

	def get_entries(self):
		""" Uses a recursive Generator to parse """
		for item in self.jsonItems:
#			pprint (item)
			entry = {}
			entry['sources'] = {}
			entry['crawled'] = item.get('crawlTimeMsec',u'')
			entry['google_id'] = item.get('id','')
			try:
				entry['original_id'] = item['origin']['streamId']
			except:
				entry['original_id'] = u''
			entry['title'] = item.get('title','')
			try:
				entry['link'] = item['alternate'][0]['href']	# [{'alternate': [{'href': 'http://','type': 'text/html'}]
			except:
				entry['link'] = u''
			entry['categories'] = item.get('categories','')
			try:
				entry['content'] = item['content']['content']
			except:
				entry['content'] = u''
			try:
				entry['summary'] = item['summary']['content']
			except:
				entry['summary'] = u''
			entry['author'] = item.get('author',u'')
			entry['title'] = item.get('title',u'')
			entry['published'] = item.get('published',u'')
			entry['updated'] = item.get('updated',u'')
			entry['origin'] = item.get('origin', {})
			try:
				streamid = entry['origin']['streamId']
				title =  entry['origin']['title']
				entry['sources'][streamid] = ( streamid, title )
			except:
				entry['sources'] = {}

#			pprint (entry)
			yield entry

	def get_items(self):
		return self.jsonItems

	def get_item(self, itemIdx):
		try:
			return self.jsonItems[itemIdx]
		except:
			return None

	def get_size(self):
		return len(self.jsonItems)

#if ( __name__ == "__main__" ):
#	print "GOOGLE READER started"
#	client = GoogleReaderClient()
#	if client.authenticate("username","password"):
#		xmlobject = client.get_subscription_list()
#		result = GoogleObject(xmlobject).parse()
#		pprint (result)

#		xmlobject = client.get_tag_list()
#		result = GoogleObject(xmlobject).parse()
#		pprint (result)

#		print "client.get_reading_list()"
#		print client.get_reading_list()
#		print "client.get_read_items()"
#		print client.get_read_items()
#		print "client.get_reading_tag_list()"
#		print client.get_reading_tag_list('audiovideo')
#		print "client.get_starred()"
#		print client.get_starred()
#		print "client.get_token()"
#		print client.get_token()

#		test_feed = 'http://picasaweb.google.com/data/feed/base/user/timothy.broder/albumid/5101347429735335089?kind=photo&alt=rss&hl=en_US'
#		test_feed = 'http://action.giss.ath.cx/RSSRewriter.py/freenews'
		#print subscribe_to(test_feed)
		#returns ok but I don't see the feed in reader?
#		atomfeed = client.get_feed(test_feed)
#		print "atomfeed=", atomfeed
#		if atomfeed:
#			xmlfeed = GoogleFeed(atomfeed)
#			print xmlfeed.get_title()
#
#			for entry in xmlfeed.get_entries() :
#				print "    %s %s %s\n" % (entry['google_id'],entry['published'],entry['title'])
#			print xmlfeed.get_continuation()