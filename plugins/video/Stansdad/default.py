import urllib,re,sys,socket
import xbmcplugin,xbmcgui
import htmllib



#[(url,show)]
def getSouthparkepisodes(url):
        res=[]
        f=urllib.urlopen("http://www.stansdad.com/season"+url)
        a=f.read()
        f.close()
        p=re.compile(r'<IFRAME src="(.+?)" width="520" height="406"')
        match=p.findall(a)
        for url in match:
                res.append(url)
        return res

#[(url,show)]
def getSouthparkvidlinks(url):
        res=[]
        f=urllib.urlopen("http://www.stansdad.com"+url)
        a=f.read()
        f.close()
        p=re.compile(r'file=(.+?)&image')
        match=p.findall(a)
        for url in match:
                res.append(url)
                return res


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

        res=[]
        f=urllib.urlopen("http://www.stansdad.com")
        a=f.read()
        f.close()
        p=re.compile(r'<option class="option" value="season(.+?)">.+?-(.+?)</option>')
        match=p.findall(a)
        for url,name in match:
                addDir(name,url,1)

def showShows(url,name):
        shows=getSouthparkepisodes(url)
        for url in shows:
                addDir(name,url,2)
                
def showVidlinks(url):
        res=[]
        vidlink=getSouthparkvidlinks(url)
        for url in vidlink:
                addLink(name,"http://www.surfthechannel.com/player/flvplayer_elite.swf?VGFzd2FQUmVYZWZlUGh1d3ViYWJydXN3ZVdydUNoZWRSZXByYVRIZU51eWV5VXR1dGVqQXRIZXBBamV0ZXJBY3d1c3BVUGh1amFmYWt1dGVGdWZ1dmFXcnVnZXNwYVphc3B1UHJhY3JlcXVzcGFtYXJhc3d1ZnV2ZXZ1cHJ1d2VhSFIwY0RvdkwyZGxkR3hwYm1zdWMzVnlablJvWldOb1lXNXVaV3d1WTI5dEwyWnNkaTlQUkdzMFRrUlpNVTVFV1RGT1JFVjZUVlJqTlU5RVVUSk9WRkY0VG1wVk1FNXFWVEJQVkdjelQxUm5NRTVxVlRCTlZGazBUa1JyTkU1NlVUVlBSR00xY0h1amVzd0FyZXZ1enVicmV6VWRFc3dlUGFQaGV4ZWZBd3JVY2VEdXRyVWZydXNhdGhhdHJhbnV3ckVIZXdyZVRucHJNazVFV1RGT1JFVXlUbFJSZUU1cVZUQlBWR2N6V1ZWb1UwMUhUa1ZpTTFwTlRUSlJlbHBJYXpGa1JuQllXa2RvYTJKWGVISlhiR041VG1wVk1rNUVXVEZPUkVVeFRWUlpNVTVFV1RGT1JGRXlUbFJGTWs1VVJUSlBSR013VDBSUk1rNVVUYXN3YVBSZVhlZmVQaHV3dWJhYnJ1c3dlV3J1Q2hlZFJlcHJhVEhlTnV5ZXlVdHV0ZWpBdEhlcEFqZXRlckFjUlhoT2FsVXdUMVJuTUU1NmF6Uk9SRTE1VFZSTk5HUldhM2xQV0ZKTlpXcHJlVlZHVW10VmJFbzJXa1pzVW1Fd1dsWldWRUpYVlZSbk1FMVVTWHBQVkVFeVRrUlpNVTVFV1RGT1JGVXlUa1JyTkU1NmF6Uk9hbEY0VGtSRk5FNTZVVFZQUkZFeXd1c3BVUGh1amFmYWt1dGVGdWZ1dmFXcnVnZXNwYVphc3B1UHJhY3JlcXVzcGFtYXJhc3d1ZnV2ZXZ1cHJ1d2VUbFJGTWsxVVVUSk9SR2MwVFVSck5FMUVhelJOUkd0NVRYcG9hRk5HU1hkWk1GSjJaR3QzZWxwRVRtdGxWRll3VjJ4a2EyRkhVblJpUjNSaFZucG9NVmRVU1RWa1JYZzJUMVJLVVZaSFVsTlZibkJyVjFaR2NsSnNWbFpOUmxwU0xtWnNkZz09&config=/skin2/dynamic.php?xmlnum=15&themes=/player/themes.xml&allowSciptAccess=true&allowFullScreen=true&uidpass=579365678&uidpass2=751447256")


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
        print "index of : "+url
        showShows(url,name)
elif mode==2:
        print "Next: "+url
        showVidlinks(url)
elif mode==3:
        print "show eps: "+url+" - "+name
        showEpisodes(url)
elif mode==4:
        print "show vidlinks: "+url
        showVidLinks(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
