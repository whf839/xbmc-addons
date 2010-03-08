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
			("Kraje i Regiony",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&tags=(Kraje_i_regiony)&rss=1'),
			("Aktywnie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&tags=(Aktywnie)&rss=1'),
			("TV",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&tags=%28TV%29&rss=1'),
			("Ekstremalnie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&tags=%28Ekstremalnie%29&rss=1'),
			("Wasze Filmy",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&tags=%28Wasze_filmy%29&rss=1'),
			("Goście",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&tags=%28Go%C5%9Bcie%29&rss=1'),
			("Wszystkie",'http://www.onet.tv/feed/getMoviesCategoryOrTagsDate,15,1,desc,movies.xml?category=8&rss=1')
			]
		for name, url in gl:
			li=xbmcgui.ListItem(name)
			u=sys.argv[0]+"?RSS&po_co="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
