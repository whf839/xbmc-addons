import urllib,urllib2,re,sys,xbmcplugin,xbmcgui


def alphabetList(url):
	res=[]
	alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	res.append((url, "0-9"))
	for a in alphabet:
		res.append((url,a))
	return res

#[(url,show)]
def getShows(url,name):
        res=[]
        alph=[]
        req = urllib2.Request("http://www.crunchyroll.com/"+ url +"/?tab=index")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile(r'<a href="http://www\.crunchyroll\.com/series-(.+?)/(.*)\.html" class="channel-index-item" title="(.+?)">')
        match=p.findall(link)
        for i in range(0,len(match)):
        	if match[i][1][:1].isdigit() == True and name == "0-9":
        		alph.append(match[i])
        	elif match[i][1][:1] == name:
        		alph.append(match[i])
        for url,title,name in alph:
                res.append((url,name))
        return res

#[(url,name)]
def getShowSeason(url):
        res=[]
        req = urllib2.Request("http://www.crunchyroll.com/showseriesmedia?id=" + url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        inpage=re.compile(r'<a href="http://www\.crunchyroll\.com/showseriesmedia\?id=' + url + '&amp;pg=(.?)" class="paginator" title="Last">')
        match=inpage.findall(link)
        if (len(match) > 0):
	        lastpage=int(match[0])+1
	else:
		lastpage=1
        for page in range(0, lastpage):
        	f=urllib.urlopen("http://www.crunchyroll.com/showseriesmedia?id=" + url + "&pg=" + str(page))
        	a=f.read()
        	f.close()
        	p=re.compile(r'<div class="thumb-media-mug mediathumb-mug mediathumb-mug-thumb"><a href="http://www.crunchyroll.com/media-(.+?)" title="(.+?)">')
        	match=p.findall(a)
        	for a in match:
                	res.append(a)
        return res

def getVideo(link):
	p=re.compile(r"flashvars:'premium=true&autoStart=true&delay=3&file=(.+?)&hash=")
	match=p.findall(link)
	for vidurl in match:
		url=urllib.unquote(vidurl)
		return url
	# deal with a different format
	p=re.compile(r"var btdna_file = encodeURIComponent\(btdna\({url:'(.+?)',")
	match=p.findall(link)
	for vidurl in match:
		return vidurl

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


def getVidLinks(url):
	res = []
	# get hi-res
        req = urllib2.Request("http://www.crunchyroll.com/media-" + url + "?hires=1")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        vidlink=getVideo(link)
	if vidlink: res.append(vidlink)
	# get low-res
        req = urllib2.Request("http://www.crunchyroll.com/media-" + url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        vidlink=getVideo(link)
	if vidlink: res.append(vidlink)
	# get h.264
	req = urllib2.Request("http://www.crunchyroll.com/media-" + url + "?h264=1")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        vidlink=getVideo(link)
	if vidlink: res.append(vidlink)
	return res
	
def addLink(name,url,thumbnail):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,thumbnail):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def showCats():
	cat=[("anime", "Anime"), ("drama", "Drama"), ("mv", "Music")]
	for url,name in cat:
		addDir(name,url,1,"")

def showAlphabet(url):
        alphabet=alphabetList(url)
        for url,name in alphabet:
                addDir(name,url,2,"")

def showShows(url,name):
        shows=getShows(url,name)
        for url,name in shows:
                addDir(name,url,3,"")

def showEpisodes(url):
        episodes=getShowSeason(url)
        for url,name in episodes:
                addDir(name,url,4,"")

def showVidLinks(url):
        vidLinks=getVidLinks(url)
        if len(vidLinks) == 1:
		addLink("Watch Episode",vidLinks[0],"")
	elif len(vidLinks) == 2:
        	addLink("Watch Episode - High Quality",vidLinks[0],"")
        	addLink("Watch Episode - Low Quality",vidLinks[1],"")
        elif len(vidLinks) == 3:
        	addLink("Watch Episode - High Quality",vidLinks[0],"")
        	addLink("Watch Episode - Low Quality",vidLinks[1],"")
        	if not vidLinks[2] == vidLinks[1]:
        		addLink("Watch Episode - Hi-Def", vidLinks[2],"")
        else:
        	addLink("Unable to find video","","")



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
	print "categories"
	showCats()
elif mode==1:
	print "alphabet of " + name
	showAlphabet(url)
elif mode==2:
        print "show Shows: "+url
        showShows(url,name)
elif mode==3:
        print "show eps: "+url+" - "+name
        showEpisodes(url)
elif mode==4:
        print "show vidlinks: "+url
        showVidLinks(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
