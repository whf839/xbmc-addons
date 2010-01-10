import urllib,urllib2,re,xbmcplugin,xbmcgui,urlparse,os
from BeautifulSoup import BeautifulSoup, SoupStrainer

#Vibux - by pajretX 2010.

#.nF0
__plugin__  = "Vibux"
__author__  = "pajretX"
__date__    = "10 January 2010"
__version__ = "1.01"



#0
def Main():
	addDir('Most Recent','http://vibux.com/recent/1',2,'')
	addDir('Most Viewed','http://vibux.com/viewed/1',2,'')
	addDir('Random','http://vibux.com/random/1',2 ,'')
	addDir('Categories','http://vibux.com/channels/',1,'')
	addDir('Search','sss',7,'')
#1
def CATEGORIES(url):
	getData = urllib2.Request(url)
	response = urllib2.urlopen(getData)
	link=response.read()
	response.close
	soupStrainer  = SoupStrainer ( "ul", { "id" : "channels" } )
	b = BeautifulSoup( link, soupStrainer )
#video_names_1
	v1 = b.findAll( "li", { None : None } )
	v1=str(v1).replace(" ","")
	cats=re.compile('/div>\n<ahref="(.+?)">\n(.+?)\n</a>\n<divclass').findall(str(v1))
	for WURL,NAME in cats:
		addDir(NAME,WURL + 'recent/1',2,'')	


# 2 
def LISTA(url):
	warunek=re.compile('/channel/').findall(url)
	if warunek != []:
		adres=re.compile('(.+?)recent/\\d+').findall(url)[0]
		numerek=re.compile('.+?recent/(\d+)').findall(url)[0]
		nastepna=str(int(numerek) + 1)
		adress=adres + 'recent/' + str(nastepna)
	else:
		adres=re.compile('(.+?)/\\d+').findall(url)[0]
		numerek=re.compile('.+?/(\d+)').findall(url)[0]
		nastepna=str(int(numerek) + 1)
		adress=adres + '/' + str(nastepna)
	addDir('Next Page',adress,2,'')
	getData = urllib2.Request(url)
	response = urllib2.urlopen(getData)
	link=response.read()
	response.close
	soupStrainer  = SoupStrainer ( "div", { "class" : "video" } )
	b = BeautifulSoup( link, soupStrainer )
	cats=re.compile('</div><a href="(.+?)"><img src="(.+?)" /></a><div class="video-title"><b><a href=".+?" title="(.+?)">.+?</a></b></div>').findall(str(b))
	for WURL,SCURL,WNAME in cats:
		WNAME=WNAME.replace('&amp;','&').replace('!','')
		addDir1(WNAME,WURL,3,SCURL)
# 3
def cedzak(url,name):
	getData = urllib2.Request(url)
	response = urllib2.urlopen(getData)
	link=response.read()
	response.close
	url=re.compile('<param name="src" value="(.+?)" />').findall(link)[0]
	pliki(url,name)	
	
	
# 3a
def pliki(url,name):
	stream = httppobierz(url,name)
	if stream == 'false':
		return
	if xbmcplugin.getSetting("dvdplayer") == "true":
		player_type = xbmc.PLAYER_CORE_DVDPLAYER
	else:
		player_type = xbmc.PLAYER_CORE_MPLAYER
	ok=xbmc.Player(player_type).play(url)

# 7
def search():
	bla = ''
	kb = xbmc.Keyboard(bla, "Search")
	kb.doModal()
	if (kb.isConfirmed()):
		searchstring = kb.getText()
	searched = searchstring.replace(' ','%20')
	url = 'not finished'
	LISTA(url)

def httppobierz(koncowy,name):
	name = name + '.avi'
	def pobierz(url,dest):
                    dp = xbmcgui.DialogProgress()
                    dp.create('Pobieranie','',name)
                    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
                    try:
                                    percent = min((numblocks*blocksize*100)/filesize, 100)
                                    dp.update(percent)
                    except:
                                    percent = 100
                                    dp.update(percent)
                    if dp.iscanceled():
                                    dp.close()
        plik = None
        stream = 'false'
        if (xbmcplugin.getSetting('pobierz') == '0'):
                dia = xbmcgui.Dialog()
                ret = dia.select(xbmc.getLocalizedString( 30011 ),[xbmc.getLocalizedString( 30006 ),xbmc.getLocalizedString( 30007 ),xbmc.getLocalizedString( 30008 ),xbmc.getLocalizedString( 30012 )])
                if (ret == 0):
                        stream = 'true'
                elif (ret == 1):
                        plik = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('pobierz_do'), name))
                        pobierz(koncowy,plik)
                elif (ret == 2):
                        plik = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('pobierz_do'), name))
                        pobierz(koncowy,plik)
                        stream = 'true'
                else:
                        return stream
        #odtwarzaj
        elif (xbmcplugin.getSetting('pobierz') == '1'):
                stream = 'true'
        #pobierz
        elif (xbmcplugin.getSetting('pobierz') == '2'):
                plik = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('pobierz_do'), name))
                pobierz(koncowy,plik)
        #pobierz i odtwarzaj
        elif (xbmcplugin.getSetting('pobierz') == '3'):
                plik = xbmc.translatePath(os.path.join(xbmcplugin.getSetting('pobierz_do'), name))
                pobierz(koncowy,plik)
                stream = 'true'            
        if (plik != None and os.path.isfile(plik)):
                koncowy =str(plik)
        return stream


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



def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(" " + name + " ", iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addDir1(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
	Main()
     
elif mode==1:
	print ""
	CATEGORIES(url)

elif mode==2:
	print ""+url
	LISTA(url)

elif mode==3:
	print ""
	cedzak(url,name)

elif mode==7:
	print ""+url
	search()

xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
