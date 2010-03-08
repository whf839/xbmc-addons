import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
class Main:
	def __init__( self ) :

		self.getNames()

	def getNames(self):
		gl=[
			("Kraj",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Kraj%29&rss=1'),
			("Świat",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28%C5%9Awiat%29&rss=1'),
			("Teraz MY",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Teraz_MY%29&rss=1'),
			("CNN",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28CNN%29&rss=1'),
			("Pogoda",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Pogoda%29&rss=1'),
			("Biznes",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Biznes%29&rss=1'),
			("Nauka",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Nauka%29&rss=1'),
			("Ciekawostki",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28Ciekawostki%29&rss=1'),
			("UWAGA!",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&tags=%28UWAGA!%29&rss=1'),
			("Wszystkie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=1&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
