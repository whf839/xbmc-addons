import urllib2,urllib,re,sys,xbmcplugin,xbmcgui


def alphabetList(url):
	res=[]
	alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	res.append((url, "0-9"))
	for a in alphabet:
		res.append((url,a))
	return res

def getShows(url,name):
        res=[]
        alph=[]
        f=urllib2.urlopen(url)
        a=f.read()
        f.close()
        p=re.compile('<a href="(.+?)">(.+?)</a> <small style="color:#E1E1E1">.+?</small><br/>')
        match=p.findall(a)
        for i in range(0,len(match)):
        	if match[i][1][:1].isdigit() == True and name == "0-9":
        		alph.append(match[i])
        	elif match[i][1][:1] == name:
        		alph.append(match[i])
        for url,name in alph:
                res.append((url,name))
        return res



def getVideo(url):
        res=[]
        f=urllib2.urlopen("http://www.moviealien.com/"+url)
        a=f.read()
        f.close()
        p=re.compile(r'<embed src="http://www.veoh.com\/.+?.swf\?permalinkId=(.+?)\&id=.+?player=videodetailsembedded&videoAutoPlay=0"')
        match=p.findall(a)
        for a in match:
                f=urllib2.urlopen("http://www.veoh.com/rest/video/"+str(a)+"/details")
                veo=f.read()
                comp=re.compile('fullPreviewHashPath="(.+?)"')
                for url in comp.findall(veo):
                        return url
                        
       
        # Megavideo
        
        p=re.compile(r'<param name="movie" value="(.+?)">')
        match=p.findall(a)
        for a in match:
                if len(a)<79:
                        a=a[:-43]
                        code=re.sub('v/','?v=',a)
                        link='http://clipnabber.com/gethint.php'
                        data="mode=1&url="+code
                        req=urllib2.Request(link,data)
                        response=urllib2.urlopen(req)
                        results=response.read()
                        p=re.compile(r'<a href=\'(.+?)\' >')
                        flv=p.findall(results)
                        for vidlink in flv:
                                vidlink=vidlink+"voin.flv"
                        return vidlink
                        
                
                elif len(a)<80:
                        a=a[:-44]
                        code=re.sub('v/','?v=',a)
                        link = 'http://clipnabber.com/gethint.php'
                        data = "mode=1&url="+code
                        req = urllib2.Request(link,data)
                        response = urllib2.urlopen(req)
                        results = response.read()
                        p=re.compile(r'<a href=\'(.+?)\' >')
                        flv=p.findall(results)
                        for vidlink in flv:
                                vidlink=vidlink+"voin.flv"
                        return vidlink
                                
                elif len(a)<81:
                        a=a[:-45]
                        code=re.sub('v/','?v=',a)
                        link = 'http://clipnabber.com/gethint.php'
                        data = "mode=1&url="+code
                        req = urllib2.Request(link,data)
                        response = urllib2.urlopen(req)
                        results = response.read()
                        p=re.compile(r'<a href=\'(.+?)\' >')
                        flv=p.findall(results)
                        for vidlink in flv:
                                vidlink=vidlink+"voin.flv"
                        return vidlink

        #GOOGLEY-WOOGLEY
        p=re.compile('src="http://video.google.com/.+?docId=(.+?)&amp.+?"')
        match=p.findall(a)
        for a in match:
                code="http://video.google.com/videoplay?docid="+str(a)
                link = 'http://clipnabber.com/gethint.php'
                data = "mode=1&url="+code
                req = urllib2.Request(link,data)
                response = urllib2.urlopen(req)
                results = response.read()
                p=re.compile(r'<a href=\'(.+?)\' >')
                google=p.findall(results)
                for vidlink in google:
                        return vidlink
                                
           
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

      
def addLink(name,url):
        #print name
        #print url
        #print "--"
        ok=True
        thumbnail_url = url.split( "thumbnailUrl=" )[ -1 ]
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail_url)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def showCats():
        cat=[("http://www.moviealien.com/channels.php?channel=anime","ANIME"),("http://www.moviealien.com/channels.php?channel=tvshows", "TV SHOWS"),("http://www.moviealien.com/channels.php?channel=movies","MOVIES"),("http://www.moviealien.com/channels.php?channel=docus","DOCUMENTARIES")]
        for url,name in cat:
                addDir(name,url,1)

def showAlphabet(url,name):
        alphabet=alphabetList(url)
        for url,name in alphabet:
                addDir(name,url,2)                          

def showShows(url,name):
        shows=getShows(url,name)
        for url,name in shows:
                addDir(name,url,3)
                            
def showGetUrl(url):
        check=getVideo(url)
        addLink("Watch Video",check)
       


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
        print "A-Z of : "+url
        showAlphabet(url,name)
elif mode==2:
        print "show Page: "+url
        showShows(url,name)
elif mode==3:
        print "show vidlinks: "+url
        showGetUrl(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
