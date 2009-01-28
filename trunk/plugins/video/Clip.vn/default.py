import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,socket,base64,os

#Clip.vn

def CATS():
        if xbmcplugin.getSetting("Clear Previous Searches") == "true":
                os.remove('Q:/plugins/video/Clip.vn/search.vn')
        else:
                addDir("SEARCH CLIP VN","http://Voinage.com",4,"");addDir("PREVIOUS SEARCHES","http://Voinage.com",3,"")

def PREVSEARCH():
        main=open('Q:/plugins/video/Clip.vn/search.vn','r').read()
        bits=re.compile('<URL>(.+?)</URL><NAME>(.+?)</NAME>').findall(main)
        for url,name in bits:
                addDir(name,url,1,"")

def INDEX():
        res=[]
        keyb = xbmc.Keyboard('', 'Search Clip Vn')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote_plus(search)                
                req = urllib2.Request('http://clip.vn/search?inputType=0&searchFor=clip&lookIn=site&keyWord='+encode+'&cPage=1')
                url='http://clip.vn/search?inputType=0&searchFor=clip&lookIn=site&keyWord='+encode+'&cPage=1'
                f = open('Q:/plugins/video/Clip.vn/search.vn', 'a');f.write('<URL>'+url+'</URL><NAME>'+search+'</NAME>');f.close()
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('\r\n\t\t\t\t\t\t\t\t<a href="http://clip.+?/watch/.+?/(.+?),vn" title=".+?" onclick=".+?" >\r\n\t\t\t\t\t\t\t\t\t<img class="clipthumb" src="(.+?)" alt="(.+?)"/>')
                match=p.findall(link)
                for url,thumbnail,name in match:
                        addDir(name,url,2,thumbnail)
                next='http://clip.vn/search?inputType=0&searchFor=clip&lookIn=site&keyWord='+encode+'&cPage=1&'
                p=re.compile('http://clip.vn/.+?inputType=0&searchFor=clip&lookIn=site&keyWord=(.+?)&cPage=(.+?)&')
                match2=p.findall(next)
                for code,page in match2:
                        url="http://clip.vn/search?inputType=0&searchFor=clip&lookIn=site&keyWord="+code+"&cPage="+str(int(page)+1)+"&"
                        addDir('   NEXT PAGE',url,1,"")
                        
def INDEX2(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('\r\n\t\t\t\t\t\t\t\t<a href="http://clip.+?/watch/.+?/(.+?),vn" title=".+?" onclick=".+?" >\r\n\t\t\t\t\t\t\t\t\t<img class="clipthumb" src="(.+?)" alt="(.+?)"/>')
        match=p.findall(link)
        for url,thumbnail,name in match:
                addDir(name,url,2,thumbnail)
        p=re.compile('http://clip.vn/.+?inputType=0&searchFor=clip&lookIn=site&keyWord=(.+?)&cPage=(.+?)&')
        match2=p.findall(url)
        for code,page in match2:
                url="http://clip.vn/search?inputType=0&searchFor=clip&lookIn=site&keyWord="+code+"&cPage="+str(int(page)+1)+"&"
                addDir('   NEXT PAGE',url,1,"")

            
def VIDEO(url,name):
        req = urllib2.Request("http://clip.vn/movies/nfo/"+url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read()
        match=re.compile(r'\r\n\t\t\t\t\t\t\t<enclosure url=\'(.+?)\' duration=\'.+?\' id=\'.+?\' type=\'video/x-flv\'/>\r\n\t\t\t\t\t</ClipInfo>').findall(response)
        addLink(name,'http://127.0.0.1:64653/streamplug/'+base64.standard_b64encode(match[0])+'?.flv',"")
        

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
        print "categories"
        CATS()
elif mode==1:
        print "index of : "+url
        INDEX2(url,name)
elif mode==2:
        print "index of : "+url
        VIDEO(url,name)
elif mode==3:
        print "index of : "+url
        PREVSEARCH()
elif mode==4:
        print "index of : "+url
        INDEX()
        

xbmcplugin.endOfDirectory(int(sys.argv[1]))
