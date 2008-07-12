import urllib,urllib2,re,xbmcplugin,xbmcgui#v/a.j

def ExtractMediaUrl(url, data):
        
        if url.find("megavideo.com") > 0:
                codeRegex = '<ROW url="(.+?)" runtime=".+?" runtimehms=".+?" size=".+?" waitingtime=".+?" k=".+?"></ROW>'
                codeResults = re.findall(codeRegex, data, re.DOTALL + re.IGNORECASE)
                if len(codeResults) > 0:
                        code = codeResults[-1]
                        dictionary = {"0":":","%24": ".", "%25": "/", "%3A": "0", "%3B": "1", "8": "2", "9": "3", "%3E": "4", "%3F": "5", "%3C": "6", "%3D": "7", "2": "8", "3": "9", "a": "k", "b": "h", "c": "i", "d": "n", "e": "o", "f": "l", "g": "m", "h": "b", "i": "c", "k": "a", "l": "f", "m": "g", "n": "d", "o": "e", "p": "z", "s": "y", "%7E": "t", "y": "s","%7C": "v", "%7D": "w", "z": "p"}
                        return RegexReplaceDictionary(code, dictionary) 
                else:
                        return ""
        
def RegexReplaceDictionary(string, dictionary):
      
        rc = re.compile('|'.join(map(re.escape, dictionary)))
        def Translate(match):
                return dictionary[match.group(0)]
        return rc.sub(Translate, string)

def INDEXCATS():
        res=[]
        req = urllib2.Request('http://anijunkie.com/')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&amp;','&',link)
        code2=re.sub('~','',code)
        response.close()
        p=re.compile('<li class=".+?"><a href="http://anijunkie.com/index.+?option=com_seyret&catid=(.+?)&Itemid=(.+?)">(.+?)</a></li>')
        match=p.findall(code2)
        del match[0:6]
        for catid,itemid,name in match:
                url="http://anijunkie.com/index2.php?option=com_seyret&Itemid="+itemid+"&task=rss2feed&no_html=1&cid="+catid
                addDir(name,url,1,"")
                
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&amp;','&',link)
        response.close()
        p=re.compile('<title>(.+?)</title>\n\t\t\t\t\n\t\t\t\t<link>(.+?)</link>\n\t\t\t\t\t\t\t\t\n\t\t\t\t<description>&lt;p&gt;&lt;img width=&quot;160&quot; src=&quot;(.+?)&')
        match=p.findall(code)
        for name,url,thumb in match:
                addDir(name,url,2,thumb)
                
def VID(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<embed src="http://www.veoh.com/videodetails.+?permalinkId=(.+?)&id=.+?&player=.+?&videoAutoPlay=.+?"')
        match=p.findall(link)
        try:
                del match[0]
        except IndexError:
                pass
        for perma in match:
                f=urllib2.urlopen("http://www.veoh.com/rest/video/"+perma+"/details")
                veo=f.read()
                comp=re.compile('fullPreviewHashPath="(.+?)"')
                for url in comp.findall(veo):
                        addLink("VEOH LOW QUALITY",url+"?.avi","")
                        veoh="http://127.0.0.1:64653/"+perma+"?.avi"
                        addLink(name+"-VEOH PROXY",veoh,"")
                        
        #GOFISH
        p=re.compile('gfid=(.+?)&')
        match=p.findall(link)
        try:
                del match[0]
        except IndexError:
                pass
        for gfid in match:
                req = urllib2.Request("http://www.gofish.com/channel.gfp?&videoGfid="+gfid)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('\npage.commentListGfid = \'(.+?)\'')
                match=p.findall(link)
                for item in match:
                        url2="http://www.gofish.com/channel.gfp?gfid="+item+"%26videoGfid="+gfid
                        link = 'http://clipnabber.com/gethint.php'
                        data = "mode=1&url="+url2
                        req = urllib2.Request(link,data)
                        response = urllib2.urlopen(req)
                        results = response.read()
                        p=re.compile(r'<a href=\'(.+?)\' >')
                        flv=p.findall(results)
                        for url in flv:
                                addLink("GOFISH VIDEO",url,"")
                                pass
        #MEGAVIDEO                     
        p=re.compile('<embed src="(.+?)"')
        match=p.findall(link)
        try:
                del match[0]
        except IndexError:
                pass
        for a in match:
                if len(a)<79 and a.find('megavideo')>0:
                        a=a[:-43]
                        code=re.sub('http://www.megavideo.com/v/','v=',a)
                        url="http://www.megavideo.com/xml/videolink.php?"+code
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        new=ExtractMediaUrl(url,link)
                        flvappend="voinage.flv"
                        flvlink=new+flvappend
                        addLink("MEGAVIDEO LINK",flvlink,"")
                     
                
                elif len(a)<80 and a.find('megavideo')>0:
                                a=a[:-44]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("MEGAVIDEO LINK",flvlink,"")
               
                else:
                        if len(a)==80 and a.find('megavideo')>0:
                                a=a[:-45]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("MEGAVIDEO LINK",flvlink,"")

                        elif len(a)>90 and a.find('megavideo')>0:
                                a=a[:-35]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink(flvlink,flvlink,"")
        
        
        
                
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
        print "CATEGORY INDEX : "
        INDEXCATS()
elif mode==1:
        print "GET INDEX OF PAGE : "+url
        INDEX(url)
elif mode==2:
        print "GET INDEX OF PAGE : "+url
        VID(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
