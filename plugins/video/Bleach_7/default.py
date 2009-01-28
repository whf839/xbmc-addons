import urllib,urllib2,re,sys,xbmcplugin,xbmcgui

def INDEX():
        req = urllib2.Request('http://www.bleach7.com/?page=member/anime')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req).read();clean=re.sub('\n','',response)
        info=re.compile('<td>(.+?)</td> <td> <a href="(.+?)">.+?</a> </td>').findall(clean)
        for name,url in info:
                addDir(name,'http://www.bleach7.com/'+url,1,"")

def VIDEO(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        addLink(name,response.url,"")

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
        def Download(url,dest):
                dp = xbmcgui.DialogProgress()
                dp.create("Fast Pass Tv Download","Downloading File",url)
                urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
                try:
                        percent = min((numblocks*blocksize*100)/filesize, 100)
                        print percent
                        dp.update(percent)
                except:
                        percent = 100
                        dp.update(percent)
                if dp.iscanceled():
                        dp.close()
        if xbmcplugin.getSetting("Download Flv") == "true":
                dialog = xbmcgui.Dialog()
                path = dialog.browse(3, 'Choose Download Directory', 'files', '', False, False, '')
                Download(url,path+name+'.flv')
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
        print "Working well"
        print xbmcgui.getCurrentWindowId()
        INDEX()
elif mode==1:
        print "index of : "+url
        print xbmcgui.getCurrentWindowId()
        VIDEO(url,name)


        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
