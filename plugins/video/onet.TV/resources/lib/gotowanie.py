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
			("Obiady",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Obiady%29&rss=1'),
			("Na szybko",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Na_szybko%29&rss=1'),
			("Mięsa i ryby",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Mi%C4%99sa_i_ryby%29&rss=1'),
			("Sałatki",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Sa%C5%82atki%29&rss=1'),
			("Desery",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Desery%29&rss=1'),
			("Na imprezę",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Na_imprez%C4%99%29&rss=1'),
			("Ze świata",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Ze_%C5%9Bwiata%29&rss=1'),
			("Inne",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&tags=%28Inne%29&rss=1'),
			("Wszystkie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=13&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
