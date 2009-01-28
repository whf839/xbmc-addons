import urllib,urllib2,re,sys,xbmcplugin,xbmcgui

       
def INDEX():
    req = urllib2.Request('http://oneclickmoviez.com/a-z-index/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    page = urllib2.urlopen(req);new=page.read();page.close()
    MAIN=re.compile('<a href="(.+?)"><br />').findall(new)
    NAME=re.compile('http://oneclickmoviez.com/.+?/.+?/(.+?)/').findall(str(MAIN))
    for i in range(0,len(MAIN)):
        addDir(NAME[i].replace('-',' ').upper(),MAIN[i],2,'')
        
def VIDEO(name,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    page = urllib2.urlopen(req);new=page.read();page.close()
    FB=re.compile('<a href="(.+?)" onclick=".+?">Watch it Online!!!</a></p>').findall(new)
    LINKS=re.compile('<p style="text-align: center;">(.+?) <a href="(.+?)" onclick=".+?">HERE</a></p>').findall(new)
    thumb=re.compile('<img style=".+?" src="(.+?)" alt="" border="0" />').findall(new)
    if not thumb: thumb=['']
    if not LINKS:
        LINKS=re.compile('>(.+?) <a href="(.+?)" onclick=".+?">').findall(new)
    if FB:
        try:
            req = urllib2.Request(FB[0])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urllib2.urlopen(req).read()
            match=re.compile("var LinkURL = \'(.+?)\'").findall(page)
            req = urllib2.Request(match[0])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urllib2.urlopen(req).read()
            link=re.compile('<embed type="video/divx" src="(.+?)"').findall(page)
            addLink(name,link[0],thumb[0])
        except:
            req = urllib2.Request('http://www.freemediatv.com/filebase.php?url=http://filebase.to/files/158069/The.Contender.S04E03.REAL.HDTV.XviD-FQM.WRESTLiNGBAY.COM.avi')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req);page2=response.read();response.close()
            URL=re.compile('<form action="(.+?)#"').findall(page2)
            CID=re.compile('name="cid" value="(.+?)">').findall(page2)
            UID=re.compile('name="uid" value="(.+?)"').findall(page2)
            DATA='cid='+urllib.quote_plus(CID[0])+'&uid='+UID[0]+'&go=click+to+watch+Video%21'
            req = urllib2.Request(URL[0])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req,DATA);response.close()
            req = urllib2.Request(FB[0])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urllib2.urlopen(req).read()
            match=re.compile("var LinkURL = \'(.+?)\'").findall(page)
            req = urllib2.Request(match[0])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urllib2.urlopen(req).read()
            link=re.compile('<embed type="video/divx" src="(.+?)"').findall(page)
            addLink(name,link[0],thumb[0])
            
            
    for host,linkage in LINKS:
        if host.find('GHOST')>0:
            req = urllib2.Request(linkage)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
            page = urllib2.urlopen(req).read()
            match=re.compile("var LinkURL = \'(.+?)\'").findall(page)
            req = urllib2.Request(match[0])
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req);page3=response.read();response.close()
            link=re.compile('<a href="(.+?)" class="download_link"').findall(page3)
            addLink(name+'-RGHOST',link[0],thumb[0])   

             
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
                dp.create("Tv-shack Download","Downloading File",url)
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
    INDEX()
elif mode==2:
    print "PAGE"
    VIDEO(name,url)

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
