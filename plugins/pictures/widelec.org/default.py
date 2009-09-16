import urllib,urllib2,re,xbmcplugin,xbmcgui,os

#widelec.org - by pajretX 2009.

#.nF0
__plugin__  = "widelec.org"
__author__  = "pajretX"
__date__    = "16 September 2009"
__version__ = "1.37.1"

HOME_DIR = os.getcwd()
base = "http://www.widelec.org/"

# STRINGS
names = xbmc.Language( HOME_DIR ).getLocalizedString
naj = (names (30000))
kom = (names (30001))
ogl = (names (30002))
kat = (names (30003))

gen = (names (30004))
kob = (names (30005))
lud = (names (30006))
wid = (names (30007))
mot = (names (30008))
odj = (names (30009))
spo = (names (30010))
sta = (names (30011))
wyn = (names (30012))
zwi = (names (30013))
res = (names (30014))

#0
def CATEGORIES():
	addDir(naj,'http://www.widelec.org/index.php?page=1&order_by=0&category=&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(kom,'http://www.widelec.org/index.php?page=1&order_by=1&category=&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(ogl,'http://www.widelec.org/index.php?page=1&order_by=2&category=&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(kat,'cat2',1,'')


#1
def CATEGORIES2():
	addDir(gen,'http://www.widelec.org/index.php?page=1&order_by=0&category=fotografia&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(kob,'http://www.widelec.org/index.php?page=1&order_by=0&category=kobiety&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(lud,'http://www.widelec.org/index.php?page=1&order_by=0&category=ludzie&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(wid,'http://www.widelec.org/index.php?page=1&order_by=0&category=miejscowki&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(mot,'http://www.widelec.org/index.php?page=1&order_by=0&category=motoryzacja&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(odj,'http://www.widelec.org/index.php?page=1&order_by=0&category=odjechane&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(spo,'http://www.widelec.org/index.php?page=1&order_by=0&category=sport&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(sta,'http://www.widelec.org/index.php?page=1&order_by=0&category=wiekowe&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(wyn,'http://www.widelec.org/index.php?page=1&order_by=0&category=wynalazki&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(zwi,'http://www.widelec.org/index.php?page=1&order_by=0&category=zwierzeta&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
	addDir(res,'http://www.widelec.org/index.php?page=1&order_by=0&category=reszta&category_id=0&site=blog&section=1&text=&pokrewne=',2,'')
                                           
     
# 2
def INDEX(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response=urllib2.urlopen(req)
	link = response.read()
	response.close()
	pagee=re.compile('.+?page=(\d+).+?').findall(url)[0]
	wwww=re.compile('&order.+?pokrewne=').findall(url)[0]
	page_n0 = str (int(pagee) + 1 )
	asasa=('http://www.widelec.org/index.php?page=%s' %page_n0 +wwww)
	addDir('--== [ N E X T     P A G E ] ==--', asasa, 2, 'http://www.widelec.org/images/pl/nav_end.gif')
	matches=re.compile('<a href="(.+?)" class="bigTitle" title=".+?"><strong>(.+?)</strong></a>').findall(link)
	del link
	for match in matches :
	#
		link = base + match[0]
		name = match[1]
		addDir(name,link,3,'')
#3
def FOTKI(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response=urllib2.urlopen(req)
	llink = response.read()
	response.close()
        foto_count=re.compile('class="next">Nast\xc4\x99pna</a><a HREF="(.+?)">Koniec</a>').findall(llink)
	del llink
        try:
                if len(foto_count)>1:        
                        dzzz=str(foto_count[0])
                        foto_c_no=re.compile('.+?page2=(\d+).+?').findall(dzzz)[0]
                        page_id_no = re.compile('(\d+).html').findall(url)[0]
                        for photos in range(1,int(foto_c_no) + 1):
                                srerl = ('http://www.widelec.org/index.php?page2=%s' %photos)
                                req = urllib2.Request(srerl +'site=blog&action=detail&blog_id=' + page_id_no +'&site=blog&section=1&text=&pages=10')
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response=urllib2.urlopen(req)
                                html = response.read()
                                response.close()
                                matches=re.compile('<img src="stuff(.+?)".+?class.+?>').findall(html)
                                del html
                                for foto in matches:
                                        addLink("fotka",base +'stuff/' +foto,'')
                elif len(foto_count)<1:
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response=urllib2.urlopen(req)
                        link = response.read()
                        response.close()
                        foto_count=re.compile('<a HREF="(.+?)" class="next">Nast\xc4\x99pna</a>').findall(link)[0]
                        dzzz2=re.compile('>(\d)<').findall(foto_count)[-1]
                        for photos2 in range(1,int(dzzz2) + 1):
                                page_id_no = re.compile('(\d+).html').findall(url)[0]
                                srerl = ('http://www.widelec.org/index.php?page2=%s' %photos2)
                                req = urllib2.Request(srerl +'site=blog&action=detail&blog_id=' + page_id_no +'&site=blog&section=1&text=&pages=10')
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response=urllib2.urlopen(req)
                                html = response.read()
                                response.close()
                                matches=re.compile('<img src="stuff(.+?)".+?class.+?>').findall(html)
                                del html
                                for foto in matches:
                                        addLink("fotka",base +'stuff/' +foto,'')

	except:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response=urllib2.urlopen(req)
                link = response.read()
                response.close()
                matches=re.compile('<img src="stuff(.+?)".+?class.+?>').findall(link)
                del link
                for foto in matches:
                        addLink("fotka",base +'stuff/' +foto,'')
			
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
	name = os.path.split(url)[1]
	print "name = " + name
	print "url  = " + url
	print "iconimage = " + iconimage
	print "--------------------------"
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
	print ""
	FOTKI(url)


xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
