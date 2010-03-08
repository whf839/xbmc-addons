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
			("Moda",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Moda%29&rss=1'),
			("Gwiazdy",'hhttp://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Gwiazdy%29&rss=1'),
			("Uroda",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=(Uroda)&rss=1'),
			("Fitness",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Fitness%29&rss=1'),
			("Gotowanie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Gotowanie%29&rss=1'),
			("Dziecko",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Dziecko%29&rss=1'),
			("Magia",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=%28Magia%29&rss=1'),
			("Inne",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&tags=(Inne)&rss=1'),
			("Wszystkie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=4&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
