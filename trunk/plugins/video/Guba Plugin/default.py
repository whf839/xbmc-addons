import urllib,urllib2,re,xbmcplugin,xbmcgui
#Guba Plugin XBMC - Voinage 2008

check=[]

def GUBAINDEX(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        clean=re.sub('&amp','&',link)
        clean1=re.sub('&quot;','',clean)
        clean2=re.sub('&quot;New&quot','',clean1)
        clean3=re.sub('&#39;','',clean2)
        p=re.compile('<img src="(.+?)" hoversrc=".+?" alt="" border="0"/>\n  </a>\n<ul class="drop drop_free"><li style="width: 150px;" ><div  class="thumbs_title_medium" ><a href="(.+?)">(.+?)</a>')
        match=p.findall(clean3)
        for thumbnail,url,name in match:
            res.append((thumbnail,url,name))
        return res

def INDEXSEARCHPAGES(url):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        clean=re.sub('&amp','&',link)
        clean1=re.sub('&quot;','',clean)
        clean2=re.sub('&quot;New&quot','',clean1)
        clean3=re.sub('&#39;','',clean2)
        p=re.compile('<img src="(.+?)" hoversrc=".+?" alt="" border="0"/>\n  </a>\n<ul class="drop drop_free"><li style="width: 150px;" ><div  class="thumbs_title_medium" ><a href="(.+?)">(.+?)</a>')
        match=p.findall(clean3)
        for thumbnail,url,name in match:
            res.append((thumbnail,url,name))
        return res

def VIDEOLINKS(url,name):
        res=[]
        req = urllib2.Request('http://www.guba.com'+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('null, null, null,\r\n.+"(.+?)" ')
        match=p.findall(link)
        for url in match:
            res.append(url)
        #GET ORIGINAL FORMAT
        p=re.compile('\r\n <option value="(.+?)">.+?</option>')
        match=p.findall(link)
        for url in match:
                res.append(url)
        return res

def PAGE(url):

        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<input type="hidden" name="referring_uri" value="(.+?)page." />')
        match=p.findall(link)
        pageform=match[0]
        p=re.compile('</b>             .+? <a href="(.+?)">Next</a>\n        </div>\n \n </div>\n')
        match2=p.findall(link)
        page=pageform+match2[0]
        res.append(page)
        return res

def SEARCHPAGES(url):

        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<span class="page_selected">.+?</span>                        <a href="(.+?)" >.+?</a>\n')
        match=p.findall(link)
        for url in match:
                a=re.sub(' ','%20',url)
                url2="http://www.guba.com"+a
                res.append(url2)
        return res


def SEARCHGUBA():
        res=[]
        keyb = xbmc.Keyboard('', 'SEARCH GUBA VIDEO')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote_plus(search)
                s='http://www.guba.com/general/search?query='+encode+'&set=5&x=0&y=0'
                req = urllib2.Request('http://www.guba.com/general/search?query='+encode+'&set=5&x=0&y=0')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                clean=re.sub('&amp','&',link)
                clean1=re.sub('&quot;','',clean)
                clean2=re.sub('&quot;New&quot','',clean1)
                p=re.compile('<img src="(.+?)" hoversrc=".+?" alt="" border="0"/>\n  </a>\n<ul class="drop drop_free"><li style="width: 150px;" ><div  class="thumbs_title_medium" ><a href="(.+?)">(.+?)</a>')
                match=p.findall(clean2)
                del match[0:3]
                for thumbnail,url,name in match:
                        a=re.sub(' ','%20',url)
                        res.append((thumbnail,a,name))
                        check.append(s)
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

#####DIRECTORY & LINK / SECTION

def addLink(name,url):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
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
     
def addLinkIcon(name,url,thumbnail):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDirIcon(name,url,mode,thumbnail):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#####DEFINE CATEGORY / SECTION

def MAIN():
        addDir("2. ACTION","http://www.guba.com",1)
        addDir("3. ANIMATION","http://www.guba.com",2)
        addDir("4. CLASSICS","http://www.guba.com",3)
        addDir("5. COMEDY","http://www.guba.com",4)
        addDir("6. DOCUMENTARY","http://www.guba.com",5)
        addDir("7. DRAMA","http://www.guba.com",6)
        addDir("8. EDUCATIONAL","http://www.guba.com",7)
        addDir("9. FAMILY","http://www.guba.com",8)
        addDir("10. FOREIGN","http://www.guba.com",9)
        addDir("11. INDEPENDENT","http://www.guba.com",10)
        addDir("12. MISCELLANEOUS","http://www.guba.com",11)
        addDir("13. MUSIC VIDEOS","http://www.guba.com",12)
        addDir("14. ROMANCE","http://www.guba.com",13)
        addDir("15. SPORTS","http://www.guba.com",14)
        addDir("16. TV SHOWS","http://www.guba.com",15)
        addDir("17. THRILLER","http://www.guba.com",16)
        addDirIcon("1. SEARCH GUBA","http://www.guba.com",17,"http://www.wiraconsultant.com/images/search.png")
def ACTIONCATS():
        addDir("ALL","http://www.guba.com/all/video/Action/page1",18)
        addDir("SCI FI / FANTASY","http://www.guba.com/all/video/Action/Scifi%20-%20Fantasy/page1",18)
        
def ANIMATIONCATS():
        addDir("ALL","http://www.guba.com/all/video/Animation/page1",18)
        addDir("ANIME","http://www.guba.com/all/video/Animation/Anime/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Animation/General/page1",18)
        addDir("VINTAGE","http://www.guba.com/all/video/Animation/Vintage/page1",18)

def CLASSICSCATS():
        addDir("ALL","http://www.guba.com/all/video/Classics/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Classics/General/page1",18)
 
def COMEDYCATS():
        addDir("ALL","http://www.guba.com/all/video/Comedy/page1",18)
        addDir("BRITISH","http://www.guba.com/all/video/Comedy/British/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Comedy/General/page1",18)
        addDir("SITCOMS","http://www.guba.com/all/video/Comedy/Sitcoms/page1",18)
        addDir("STAND UP","http://www.guba.com/all/video/Comedy/Standup/page1",18)
        addDir("HUMOUR","http://www.guba.com/all/video/Comedy/Humor/page1",18)
    
def DOCUMENTARYCATS():
        addDir("ALL","http://www.guba.com/all/video/Documentary/page1",18)
        addDir("AVIATION","http://www.guba.com/all/video/Documentary/Aviation/page1",18)
        addDir("CONSPIRACY","http://www.guba.com/all/video/Documentary/Conspiracy/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Documentary/General/page1",18)
        addDir("MILITARY","http://www.guba.com/all/video/Documentary/Military/page1",18)
   
def DRAMACATS():
        addDir("ALL","http://www.guba.com/all/video/Drama/page1",18)
        addDir("BRITISH","http://www.guba.com/all/video/Drama/British/page1",18)
        addDir("HORROR","http://www.guba.com/all/video/Drama/Horror/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Drama/General/page1",18)
        addDir("REALITY TV","http://www.guba.com/all/video/Drama/Reality%20TV/page1",18)
        addDir("SCI FI / FANTASY","http://www.guba.com/all/video/Drama/Scifi%20-%20Fantasy/page1",18)
        addDir("THEATRE","http://www.guba.com/all/video/Drama/Theatre/page1",18)
        addDir("VINTAGE","http://www.guba.com/all/video/Drama/Vintage/page1",18)

def EDUCATIONALCATS():
        addDir("ALL","http://www.guba.com/all/video/Educational/page1",18)
        addDir("HOBBIES","http://www.guba.com/all/video/Educational/Hobbies/page1",18)
        addDir("HOW TO","http://www.guba.com/all/video/Educational/How%20To/page1",18)
        addDir("HOME IMPROVEMENT","http://www.guba.com/all/video/Educational/Home%20Improvement/page1",18)
        addDir("COOKING","http://www.guba.com/all/video/Educational/Cooking/page1",18)
        addDir("HEALTH","http://www.guba.com/all/video/Educational/Health/page1",18)

def FAMILYCATS():
        addDir("ALL","http://www.guba.com/all/video/Family/page1",18)
    
def FOREIGNCATS():
        addDir("ALL","http://www.guba.com/all/video/Foreign/page1",18)
        addDir("AUSTRALIAN","http://www.guba.com/all/video/Foreign/Australian/page1",18)
        addDir("BOLLYWOOD","http://www.guba.com/all/video/Foreign/Bollywood/page1",18)
        addDir("FRENCH","http://www.guba.com/all/video/Foreign/French/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Foreign/General/page1",18)
        addDir("GERMAN","http://www.guba.com/all/video/Foreign/German/page1",18)
        addDir("KOREAN","http://www.guba.com/all/video/Foreign/Korean/page1",18)
        addDir("NORDIC","http://www.guba.com/all/video/Foreign/Nordic/page1",18)
 
def INDEPENDENTCATS():
        addDir("ALL","http://www.guba.com/all/video/Independent/page1",18)
    
def MISCELLANEOUSCATS():
        addDir("ALL","http://www.guba.com/all/video/Miscellaneous/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Miscellaneous/General/page1",18)
      
def MUSICVIDEOCATS():
        addDir("ALL","http://www.guba.com/all/video/Music%20Videos/page1",18)
        addDir("ALTERNATIVE","http://www.guba.com/all/video/Music%20Videos/Alternative/page1",18)
        addDir("COUNTRY","http://www.guba.com/all/video/Music%20Videos/Country/page1",18)
        addDir("ELECTRONICA","http://www.guba.com/all/video/Music%20Videos/Electronica/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Music%20Videos/Electronica/page1",18)
        addDir("METAL","http://www.guba.com/all/video/Music%20Videos/Metal/page1",18)
        addDir("NEW AGE","http://www.guba.com/all/video/Music%20Videos/New%20Age/page1",18)
        addDir("POP","http://www.guba.com/all/video/Music%20Videos/Pop/page1",18)
        addDir("ROCK","http://www.guba.com/all/video/Music%20Videos/Rock/page1",18)
        addDir("RAP","http://www.guba.com/all/video/Music%20Videos/Rap/page1",18)
        addDir("R & B","http://www.guba.com/all/video/Music%20Videos/R%20and%20B/page1",18)
    
def ROMANCECATS():
        addDir("ALL","http://www.guba.com/all/video/Romance/page1",18)
     
def SPORTSCATS():
        addDir("ALL","http://www.guba.com/all/video/Sports/page1",18)
        addDir("FITNESS","http://www.guba.com/all/video/Sports/Fitness/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/Sports/General/page1",18)
        addDir("MARTIAL ARTS","http://www.guba.com/all/video/Sports/Martial%20Arts/page1",18)
        addDir("PLANES / TRAINS / AUTOMOBILES","http://www.guba.com/all/video/Sports/Planes,%20trains,%20autos/page1",18)
        addDir("EXTREME","http://www.guba.com/all/video/Sports/Xtreme/page1",18)
        
def TVSHOWSCATS():
        addDir("ALL","http://www.guba.com/all/video/TV%20Shows/page1",18)
        addDir("GENERAL","http://www.guba.com/all/video/TV%20Shows/General/page1",18)
    
def THRILLERCATS():
        addDir("ALL","http://www.guba.com/all/video/Thriller/page1",18)

def SEARCH():
        SEARCHING=SEARCHGUBA()
        addDirIcon("000. NEXT PAGE",check[0],20,"http://www.nicolasart.com/images/Right%20Arrow.png")
        for thumbnail,link,name in SEARCHING:
                addDirIcon(name,link,19,thumbnail)
                                
def SHOWGUBAINDEX(url,name):
        GUBA=GUBAINDEX(url,name)
        for thumbnail,url,name in GUBA:
                addDirIcon(name,url,19,thumbnail)
                
def SHOWINDEXSEARCHPAGES(url):
        GUBAPAGES=INDEXSEARCHPAGES(url)
        for thumbnail,url,name in GUBAPAGES:
                addDirIcon(name,url,19,thumbnail)

def SHOWPAGES(url):
        PAGEFORM=PAGE(url)
        for PAGES in PAGEFORM:
                addDirIcon("000. NEXT PAGE",PAGES,18,"http://www.nicolasart.com/images/Right%20Arrow.png")

def SHOWSEARCHPAGES(url):
        PAGEFORM=SEARCHPAGES(url)
        for PAGES in PAGEFORM:
                addDirIcon("000. NEXT PAGE",PAGES,20,"http://www.nicolasart.com/images/Right%20Arrow.png")
                                           
def SHOWVIDEOLINKS(url,name):
        Vids=VIDEOLINKS(url,name)
        if len(Vids)>1:
                addLink("WATCH VIDEO - ORIGINAL FORMAT HI QUALITY",Vids[1])
        else:
                for url in Vids:
                        addLink("WATCH VIDEO - FLV",url)

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
        MAIN()
elif mode==1:
        print "ACTIONCATS: "+url
        ACTIONCATS()
elif mode==2:
        print "ANIMATIONCATS: "+url
        ANIMATIONCATS()
elif mode==3:
        print "CLASSICSCATS: "+url
        CLASSICSCATS()
elif mode==4:
        print "COMEDYCATS:"+url
        COMEDYCATS()
elif mode==5:
        print "DOCUMENTARYCATS:"+url
        DOCUMENTARYCATS()
elif mode==6:
        print "DRAMACATS:"+url
        DRAMACATS()
elif mode==7:
        print "EDUCATIONALCATS:"+url
        EDUCATIONALCATS()
elif mode==8:
        print "FAMILYCATS:"+url
        FAMILYCATS()
elif mode==9:
        print "FOREIGNCATS:"+url
        FOREIGNCATS()
elif mode==10:
        print "INDEPENDENTCATS:"+url
        INDEPENDENTCATS()
elif mode==11:
        print "MISC CATS:"+url
        MISCELLANEOUSCATS()
elif mode==12:
        print "MUSIC VIDEOSCATS"+url
        MUSICVIDEOCATS()
elif mode==13:
        print "ROMANCECATS:"+url
        ROMANCECATS()
elif mode==14:
        print "SPORTSCATS"+url
        SPORTSCATS()
elif mode==15:
        print "TV SHOWS CATS:"+url
        TVSHOWSCATS()
elif mode==16:
        print "THRILLERCATS"+url
        THRILLERCATS()
elif mode==17:
        print "SEARCH GUBA RESULTS"+url
        SEARCH()
elif mode==18:
        print "MAIN CONTENT LIST  :"+url
        SHOWPAGES(url)
        SHOWGUBAINDEX(url,name)
elif mode==19:
        print "VIDEO LINKS :"+url
        SHOWVIDEOLINKS(url,name)
elif mode==20:
        print "SHOW INDEX SEARCH PAGES:"+url
        SHOWSEARCHPAGES(url)
        SHOWINDEXSEARCHPAGES(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
