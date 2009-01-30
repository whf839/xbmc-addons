import urllib2,urllib,re,xbmcplugin,xbmcgui,os,base64

# Veoh 2008.



def CATS():
        if xbmcplugin.getSetting("Clear Previous Searches") == "true":
                os.remove(os.getcwd().replace(";","")+'/search.veoh')
        else:
                user=xbmcplugin.getSetting("Set User name: ")
                addDir('USER SUBSCRIPTIONS','http://www.veoh.com/rest/v2/execute.xml?method=veoh.people.getSubscriptions&username='+user+'&maxResults=100&apiKey=5697781E-1C60-663B-FFD8-9B49D2B56D36',3,'')
                addDir('USER FAVOURITES','http://www.veoh.com/rest/v2/execute.xml?method=veoh.people.getFavorites&username='+user+'&maxResults=100&safe=false&apiKey=5697781E-1C60-663B-FFD8-9B49D2B56D36',3,'')
                addDir("SEARCH VEOH","http://Voinage.com",1,"");addDir("PREVIOUS SEARCHES","http://Voinage.com",2,"")

def SEARCHPARAMS():
        
        if xbmcplugin.getSetting("Search Duration : All") == "true":
                dur="&minLength=0"
                SEARCH(dur)
        elif xbmcplugin.getSetting("Search Duration : 10 / 20 mins") == "true":
                dur="&minLength=600&maxLength=1200"
                SEARCH(dur)
        elif xbmcplugin.getSetting("Search Duration : 20 / 40 mins") == "true":
                dur="&minLength=1200&maxLength=2400"
                SEARCH(dur)
        elif xbmcplugin.getSetting("Search Duration : 40 / 60 mins") == "true":
                dur="&minLength=2400&maxLength=3600"
                SEARCH(dur)
        elif xbmcplugin.getSetting("Search Duration : 1hr / 3hrs") == "true":
                dur="&minLength=3600&maxLength=10800"
                SEARCH(dur)
        elif xbmcplugin.getSetting("Search Duration : 3hrs+") == "true":
                dur="&minLength=10800"
                SEARCH(dur)
        else:
                dur="&minLength=0"
                SEARCH(dur)

def PREVSEARCH():
        main=open(os.getcwd().replace(";","")+'/search.veoh','r').read()
        bits=re.compile('<URL>(.+?)</URL><NAME>(.+?)</NAME>').findall(main)
        for url,name in bits:
                addDir(name,url,3,"")
        
def SEARCH(dur):
        keyb = xbmc.Keyboard('', 'Search Veoh')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote_plus(search)
                if xbmcplugin.getSetting("Open Veoh Search") == "true":
                        url='http://www.veoh.com/rest/v2/execute.xml?method=veoh.search.video&userQuery='+encode+'&contentSource=veoh'+dur+'&safe=false&maxResults=100&apiKey=08344E97-13CE-E0BE-28AA-B8F7D686DD07'
                        f = open(os.getcwd().replace(";","")+'/search.veoh', 'a');f.write('<URL>'+url+'</URL><NAME>'+search+'</NAME>');f.close()
                elif xbmcplugin.getSetting("Specific Veoh Search") == "true":
                        url='http://www.veoh.com/rest/v2/execute.xml?method=veoh.search.video&userQuery="'+encode+'"&contentSource=veoh'+dur+'&safe=false&maxResults=100&apiKey=08344E97-13CE-E0BE-28AA-B8F7D686DD07'
                        f = open(os.getcwd().replace(";","")+'/search.veoh', 'a');f.write('<URL>'+url+'</URL><NAME>'+search+'</NAME>');f.close()
                else:
                        url='http://www.veoh.com/rest/v2/execute.xml?method=veoh.search.video&userQuery="'+encode+'"&contentSource=veoh'+dur+'&safe=false&maxResults=100&apiKey=08344E97-13CE-E0BE-28AA-B8F7D686DD07'
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                lastresult=re.compile('items="(.+?)"').findall(link);last=int(lastresult[0])
                perma=re.compile('permalinkId="(.+?)"').findall(link)
                length=re.compile('length="(.+?)"').findall(link)
                purl=re.compile('fullPreviewHashPath="(.+?)"').findall(link)
                thumbnail=re.compile('fullHighResImagePath="(.+?)"').findall(link)
                name=re.compile('\r\n\ttitle="(.+?)"\r\n\tdateAdded=".+?"').findall(link)
                ipod=re.compile('ipodUrl="(.+?)"').findall(link)
                for i in range(0,len(perma)):
                        addLink(name[i]+' Dur: '+length[i],purl[i],thumbnail[i])
                        addLink2(name[i]+'-full mp4'+' Dur: '+length[i],ipod[i])
                if last>100: addDir(" NEXT PAGE",'http://www.veoh.com/rest/v2/execute.xml?method=veoh.search.video&userQuery="'+encode+'"&contentSource=veoh'+dur+'&offset=100&safe=false&maxResults=100&apiKey=08344E97-13CE-E0BE-28AA-B8F7D686DD07',3,"")
                else: pass
                

                        
def INDEX(url):
        
        if xbmcplugin.getSetting("Search Duration : All") == "true":
                dur="&minLength=0"
        elif xbmcplugin.getSetting("Search Duration : 10 / 20 mins") == "true":
                dur="&minLength=600&maxLength=1200"
                
        elif xbmcplugin.getSetting("Search Duration : 20 / 40 mins") == "true":
                dur="&minLength=1200&maxLength=2400"
                
        elif xbmcplugin.getSetting("Search Duration : 40 / 60 mins") == "true":
                dur="&minLength=2400&maxLength=3600"
                
        elif xbmcplugin.getSetting("Search Duration : 1hr / 3hrs") == "true":
                dur="&minLength=3600&maxLength=10800"
                
        elif xbmcplugin.getSetting("Search Duration : 3hrs+") == "true":
                dur="&minLength=10800"
                
        else:
                dur="&minLength=0"
                
        flash=[]      
        query=re.compile('userQuery=(.+?)&').findall(url)
        numb=re.compile('<videoList offset="(.+?)"').findall(url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        numb=re.compile('<videoList offset="(.+?)"').findall(link)
        lastresult=re.compile('items="(.+?)"').findall(link);last=int(lastresult[0])
        perma=re.compile('permalinkId="(.+?)"').findall(link)
        length=re.compile('length="(.+?)"').findall(link)
        purl=re.compile('fullPreviewHashPath="(.+?)"').findall(link)
        thumbnail=re.compile('fullHighResImagePath="(.+?)"').findall(link)
        name=re.compile('\r\n\ttitle="(.+?)"\r\n\tdateAdded=".+?"').findall(link)
        collection=re.compile('channel collectionId="(.+?)"').findall(link)
        ipod=re.compile('ipodUrl="(.+?)"').findall(link)
        if len(collection)>0 and url.find('getSubscriptions')>0:
                for i in range(0,len(perma)):
                        addDir(perma[i],'http://www.veoh.com/rest/v2/execute.xml?method=veoh.collection.getVideos&collectionId='+collection[i]+'&maxResults=100&apiKey=5697781E-1C60-663B-FFD8-9B49D2B56D36',3,'')
        else:
                for i in range(0,len(perma)):
                        if url.find('collection')>0:
                                addLink2(name[i]+'-Full mp4',ipod[i])
                        else:
                                addLink(name[i]+' Dur: '+length[i],purl[i],thumbnail[i])
                                addLink2(name[i]+'-Full mp4'+' Dur: '+length[i],ipod[i])
                if last>100: addDir(" NEXT PAGE",'http://www.veoh.com/rest/v2/execute.xml?method=veoh.search.video&userQuery="'+query[0]+'"&contentSource=veoh'+dur+'&offset=100&safe=false&maxResults=100&apiKey=08344E97-13CE-E0BE-28AA-B8F7D686DD07',3,"")
                else: pass

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

      
def addLink(name,url,thumbnail):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink2(name,url):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
        SEARCHPARAMS()
elif mode==2:
        PREVSEARCH()
elif mode==3:
        INDEX(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))





       


