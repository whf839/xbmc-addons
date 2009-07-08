import urllib,urllib2,re,xbmcplugin,xbmcgui,urlparse

#KeezMovies - by pajretX 2009.

#.nF0
__plugin__  = "KeezMovies"
__author__  = "pajretX"
__date__    = "06 July 2009"
__version__ = "1.5"


#0
def CATEGORIES():
	addDir('Latest/Show All','http://www.keezmovies.com/videos?page=1',2,'')
	addDir('Categories','cat2',1,'')
	addDir('Pornstars','http://www.keezmovies.com/pornstar-list?&page=1',3,'')
	addDir('Search','sss',7,'')
#1
def CATEGORIES2():
	addDir('Amateur','http://www.keezmovies.com/videos?c=3',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/amateur.jpg')
	addDir('Anal','http://www.keezmovies.com/videos?c=35',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/anal.jpg')
	addDir('Ass','http://www.keezmovies.com/videos?c=4',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/ass.jpg')
	addDir('Asian','http://www.keezmovies.com/videos?c=1',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/asian.jpg')
	addDir('Babe','http://www.keezmovies.com/videos?c=5',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/babe.jpg')
	addDir('Big Dicks','http://www.keezmovies.com/videos?c=7',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/big-dick.jpg')
	addDir('Big Tits','http://www.keezmovies.com/videos?c=8',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/big-tits.jpg')
	addDir('Blonde','http://www.keezmovies.com/videos?c=9',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/blonde.jpg')
	addDir('Blowjob','http://www.keezmovies.com/videos?c=13',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/blowjob.jpg')
	addDir('Bondage','http://www.keezmovies.com/videos?c=10',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/bondage.jpg')
	addDir('Brunette','http://www.keezmovies.com/videos?c=11',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/brunette.jpg')
	addDir('Bukkake','http://www.keezmovies.com/videos?c=14',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/bukkake.jpg')
	addDir('Celebrity','http://www.keezmovies.com/videos?c=12',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/celebrity.jpg')
	addDir('Creampie','http://www.keezmovies.com/videos?c=15',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/creampie.jpg')
	addDir('Cumshot','http://www.keezmovies.com/videos?c=16',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/cumshot.jpg')
	addDir('Dancing','http://www.keezmovies.com/videos?c=34',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/dancing.jpg')
	addDir('Ebony','http://www.keezmovies.com/videos?c=17',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/ebony.jpg')
	addDir('Fetish','http://www.keezmovies.com/videos?c=18',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/fetish.jpg')
	addDir('Fisting','http://www.keezmovies.com/videos?c=19',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/fisting.jpg')
	addDir('Funny','http://www.keezmovies.com/videos?c=32',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/funny.jpg')
	addDir('Group','http://www.keezmovies.com/videos?c=2',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/group.jpg')
	addDir('Handjob','http://www.keezmovies.com/videos?c=20',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/handjob.jpg')
	addDir('Hardcore','http://www.keezmovies.com/videos?c=21',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/hardcore.jpg')
	addDir('Hentai','http://www.keezmovies.com/videos?c=36',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/hentai.jpg')
	addDir('Interracial','http://www.keezmovies.com/videos?c=25',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/interracial.jpg')
	addDir('Large Ladies','http://www.keezmovies.com/videos?c=6',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/large-ladies.jpg')
	addDir('Latina','http://www.keezmovies.com/videos?c=26',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/latina.jpg')
	addDir('Lesbian','http://www.keezmovies.com/videos?c=27',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/lesbian.jpg')
	addDir('Masturbation','http://www.keezmovies.com/videos?c=22',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/masturbation.jpg')
	addDir('Mature','http://www.keezmovies.com/videos?c=28',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/mature.jpg')
	addDir('MILF','http://www.keezmovies.com/videos?c=29',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/milf.jpg')
	addDir('Pornstar','http://www.keezmovies.com/videos?c=30',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/pornstar.jpg')
	addDir('POV','http://www.keezmovies.com/videos?c=41',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/pov.jpg')
	addDir('Public','http://www.keezmovies.com/videos?c=24',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/public.jpg')
	addDir('Reality','http://www.keezmovies.com/videos?c=31',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/reality.jpg')
	addDir('RedHead','http://www.keezmovies.com/videos?c=40',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/redhead.jpg')
	addDir('Striptease','http://www.keezmovies.com/videos?c=33',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/striptease.jpg')
	addDir('Teen','http://www.keezmovies.com/videos?c=37',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/teen.jpg')
	addDir('Toys','http://www.keezmovies.com/videos?c=23',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/toys.jpg')
	addDir('Vintage','http://www.keezmovies.com/videos?c=42',2,'http://cdn-www.keezmovies.com/images/cat-thumbs/big/vintage.jpg')

                                           
     
# 2
def INDEX(url): 
	url_split=urlparse.urlsplit(url)
	query_params=dict(part.split('=') for part in url_split[3].split('&'))
	curr_page=int ( query_params.get("page", 1) )
	next_page=curr_page + 1
	query_params[ "page" ] = next_page
	url_unsplit = tuple( [ url_split[0], url_split[1], url_split[2], urllib.urlencode(query_params), url_split[4] ] )
	url_next_page = urlparse.urlunsplit(url_unsplit)
	print url_next_page
	addDir('-= [ N E X T     P A G E ] =-', url_next_page, 2, 'http://www.viewista.com/right_arrow.jpg')
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<div class="video-box">\r\n\t\t\t\t\r\n\t\t\t\t\t<a href="/(.+?)" class="small">\r\n\t\t\t\t\t<img src="(.+?)?cache_control=.+?" width="160" height="120" alt=".+?" title="(.+?)"').findall(link)
	for url2,thumbnail,name in match:
                thumbnail = thumbnail.replace("?","")
                addDir(name,'http://www.keezmovies.com/watch_player.php?id='+url2,5,thumbnail)

#5
def COSTAM(name,url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<flv_url>(.+?)</flv_url>').findall(link)
	for video in match:
		addLink(name,video,'')
	if xbmcplugin.getSetting("dvdplayer") == "true":
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(video)
	else:
		xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(video)		

# 3
def PS(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()	
	npb=re.compile('.+?page=(\d)').findall(url)[0]
	np=str (int (npb) + 1)
	addDir('-= [ N E X T     P A G E ] =-','http://www.keezmovies.com/pornstar-list?&page=%s' %np,3,'http://www.viewista.com/right_arrow.jpg')
	match=re.compile('<li><a href="http://www.keezmovies.com/(.+?)">(.+?)</a></li>').findall(link)
	for url_s,name_s in match:
		url_s = url_s.replace(" ", "%20")	
		addDir(name_s,'http://www.keezmovies.com/'+url_s,4,'')
# 4
def PSURL(url): 
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<div class="video-box">\r\n\t\t\t\t\r\n\t\t\t\t\t<a href="/(.+?)" class="small">\r\n\t\t\t\t\t<img src="(.+?)?cache_control=.+?" width="160" height="120" alt=".+?" title="(.+?)"').findall(link)
	for psurl,PSthumbnail,psname in match:
		PSthumbnail = PSthumbnail.replace("?","")
		addDir(psname,'http://www.keezmovies.com/embed_player.php?id=' +psurl,6,PSthumbnail)

# 6
def COSTAM2(name,url):
        req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<flv_url>(.+?)</flv_url>').findall(link)
	for video in match:
		addLink(name,video,'')
	if xbmcplugin.getSetting("dvdplayer") == "true":
		xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(video)
	else:
		xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(video)		

# 7
def search():
	bla = ''
	kb = xbmc.Keyboard(bla, "Search")
	kb.doModal()
	if (kb.isConfirmed()):
		searchstring = kb.getText()
	searched = searchstring.replace(' ','+')
	url = 'http://www.keezmovies.com/videos?search='+searched+'&x=0&y=0'
	INDEX(url)

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
                                
	return param


def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(" " + name + " ", iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok


params=get_params()
url=None
name=None
mode=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
	print ""
	CATEGORIES()
     
elif mode==1 or url=='cat2':
	print ""
	CATEGORIES2()

elif mode==2:
	print ""+url
	INDEX(url)

elif mode==3:
	print ""+url
	PS(url)

elif mode==4:
	print ""+url
	PSURL(url)

elif mode==5:
        print ""+url
        COSTAM(name,url)

elif mode==6:
        print ""+url
        COSTAM2(name,url)

elif mode==7:
	print ""+url
	search()

xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
