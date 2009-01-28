import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,cookielib
#fastpasstv - V2008

def CATS():
        addDir('TV SHOWS','http://www.fastpasstv.com/tv-shows-a-z/',1,'')
        addDir('CARTOONS','http://www.fastpasstv.com/cartoons-a-z/',1,'')
        addDir('MOVIES','http://www.fastpasstv.com/movies-a-z/',1,'')
            
def INDEX(url):
        req=urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req);link=response.read();response.close()
        lexus=re.compile('<li><a href="(.+?)"><span class="head">(.+?)</span></a></li>').findall(link)
        if len(lexus)<1:
                lexus=re.compile('h2><a href="(.+?)" rel=".+?" title=".+?">(.+?)</a><span class="description">.+?<a href=".+?" title=".+?" rel=".+?">.+?</a></span></h2>\n\n\t<p><img class="aligncenter" src="(.+?)" alt="" />').findall(link)    
                nextpage=re.compile('<span class="alignleft"><a href="(.+?)">').findall(link)
                try: addDir('0. NEXT PAGE',nextpage[0],1,'')
                except: pass
        try:
                for url,name in lexus:
                        addDir(name,url,2,'')
        except:
                for url,name,thumb in lexus:
                        addDir(name,url,2,thumb)
                        

def VIDS(data,name):
        req = urllib2.Request(data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        page = urllib2.urlopen(req);new=page.read();page.close()
        swap=re.compile('<p><a href="(.+?)" target="_blank" onclick=".+?">(.+?)</a>').findall(new)
        if len(swap)<1:
                swap=re.compile('mce_href="(.+?)" onclick=".+?">(.+?)</a>').findall(new)
        info=re.compile('<p><img class="aligncenter" src="(.+?)" alt=.+? /></p>\n<p>(.+?)</p>\n<p>').findall(new)
        for url,name in swap:
                if url.find('divx')>0:
                        try:
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                page = urllib2.urlopen(req);new=page.read();page.close()
                                swap=re.compile('<a href="(.+?)" target="_blank">Click Here to continue to divx video</a>').findall(new)
                                req = urllib2.Request(swap[0])
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                page = urllib2.urlopen(req);new2=page.read();page.close()
                                donogo=re.compile('<embed type="video/divx" src="(.+?)"').findall(new2)
                                addLink(name,donogo[0],'')
                        except : addLink('Video not found on donogo.com','','')
                if url.find('zshare')>0:
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        page = urllib2.urlopen(req);new=page.read();page.close()
                        try:
                                zshare=re.compile("'streamer=lighttpd&autostart=true&file=(.+?)'").findall(new)
                                if not zshare:
                                        zshare=re.compile('param name="URL" value="(.+?)">\n').findall(new)
                                addLink(name,zshare[0],'',)
                        except: addLink('File Deleted from Zshare','http://gone.com','http://www.kalilily.net/weblog/gone%20fishin.jpg')
                if url.find('supernovatube')>0:
                        req = urllib2.Request(url.replace('view_video','human'))
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        page = urllib2.urlopen(req);response=page.read();page.close()
                        cookie=page.info()['Set-Cookie']
                        nova=re.compile(r'<input type="hidden" name="(.+?)" id=".+?" value="(.+?)">').findall(response)
                        submit=re.compile('<input type="submit" name="(.+?)" id=".+?" value="(.+?)">').findall(response)
                        data=nova[0][0]+'='+nova[0][1]+'&'+nova[1][0]+'='+nova[1][1]+'&'+submit[0][0]+'='+submit[0][1].replace(' ','+')
                        req = urllib2.Request(url.replace('view_video','play'),data)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        req.add_header('Cookie',cookie)
                        page = urllib2.urlopen(req)
                        response=page.read();page.close()
                        flv=re.compile('"file","(.+?)"').findall(response)
                        try:
                                addLink(name,flv[0],'')
                        except : addLink('Video not found on Supernovatube.com','','')
                        
                if url.find('veoh')>0:
                        veoh=re.sub('http://www.veoh.com/videos/','',url)
                        addLink(name,'http://127.0.0.1:64653/'+veoh,'')
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

        

def addDir(name,url,mode,thumbnail):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( "video", { "Title":name})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


      
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
        print "PAGE"
        INDEX(url)
elif mode==2:
        print "PAGE"
        VIDS(url,name)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
