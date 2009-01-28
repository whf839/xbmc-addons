import urllib,urllib2,re,sys,socket,xbmcplugin,xbmcgui,htmllib,IMDbClient,Queue,threading,time

#Globals (start with a captial letter)
Qin  = Queue.Queue() 
Qout = Queue.Queue()
Qerr = Queue.Queue()
Pool = []   
settings = {}
settings[ "username" ] = xbmcplugin.getSetting( "username" ) 
settings[ "password" ] = xbmcplugin.getSetting( "password" )


def process_queue():
    flag='ok'
    while flag !='stop':
        try:
            flag,item=Qin.get() #will wait here!
            if flag=='ok':
                IMDbFetcher = IMDbClient.IMDbFetcher()
		newdata = IMDbFetcher.fetch_info( item, "512" )
		newdata.imdb = url
                Qout.put(newdata)
        except:
            Qerr.put(err_msg())
            
def start_threads(amount=6):
    for i in range(amount):
         thread = threading.Thread(target=process_queue)
         thread.start()
         Pool.append(thread)

def put(data,flag='ok'):
    Qin.put([flag,data]) 

def get(): return Qout.get() #will wait here!

def get_all():
    try:
        while 1:
            yield Qout.get_nowait()
    except Queue.Empty:
        pass

def stop_threads():
    for i in range(len(Pool)):
        Qin.put(('stop',None))
    while Pool:
        time.sleep(1)
        for index,the_thread in enumerate(Pool):
            if the_thread.isAlive():
                continue
            else:
                del Pool[index]
            break





#[(url,show)]
def getChannelFeed(url,name):
	IMDbFetcher = IMDbClient.IMDbFetcher()	
        res=[]
        f=urllib.urlopen(url)
        a=f.read()
        f.close()
        p=re.compile(r'us.imdb.com/Title(........)')
	prevPage=re.compile(r'<a href="(.*)">Prev Page</a>')
	match=prevPage.findall(a)
	for url in match:
		info = IMDbClient._Info()
		url= "http://www.vcdquality.com/"+url
		info.title = "~Next~"
		info.poster = None
		res.append((url,info,1))
		del info

	
	
        match=p.findall(a)
	start_threads()
        for url in match:
		url = "http://us.imdb.com/Title"+url
		if (url.strip() != ""):			 
			#STANDARD use:
			put(url)	
	stop_threads()
	for info in get_all(): 
		url = "http://members.easynews.com/global4/search.html?gps="+urllib.quote_plus(info.title)+"&sbj=&from=&ns=&fil=&fex=&vc=&ac=&fty[]=MOVIE&s1=nsubject&s1d=%2B&s2=nrfile&s2d=%2B&s3=dsize&s3d=%2B&pby=100&pno=1&sS=0&u=1&svL=&d1=&d1t=&d2=&d2t=&b1=&b1t=&b2=&b2t=&px1=&px1t=&px2=&px2t=&fps1=&fps1t=&fps2=&fps2t=&bps1=&bps1t=&bps2=&bps2t=&hz1=&hz1t=&hz2=&hz2t=&rn1=&rn1t=&rn2=&rn2t=&fly=2";	
		url = url.replace("http://", "http://"+settings[ "username" ]+":"+settings[ "password" ]+"@")
		res.append((url,info,2))
		

	
	nextPage=re.compile(r'<a href="(.*)">Next Page</a>')	
	match=nextPage.findall(a)
	for url in match:
		info = IMDbClient._Info()
		url= "http://www.vcdquality.com/"+url
		info.title = "!Previous!"
		info.poster = None
		res.append((url,info,1))
		del info
        return res

#[(url,show)]
def getEasyListing(url):
        res=[]
        f=urllib.urlopen(url)
        a=f.read()
        f.close()

	prevPage=re.compile(r'<a id="prevP" href="(.*)" rel="prev">')
	match=prevPage.findall(a)
	for url in match:
		info = IMDbClient._Info()
		url= ("http://members.easynews.com"+url).replace("http://", "http://"+settings[ "username" ]+":"+settings[ "password" ]+"@")
		info.title = "!Previous!"		
		info.poster = None
		addDir(info.title,url,1,info)
		del info

	easyParse = re.compile(r'<td class="subject" ><a href="(.*)" target="subjTarget" >(.*)</a>   <a href="/header2.html' )
	items= easyParse.findall(a)
	for target,title in items:      
                res.append((title,target.replace("http://", "http://"+settings[ "username" ]+":"+settings[ "password" ]+"@")))

	nextPage=re.compile(r'<a id="nextP" href="(.*)" rel="next">')
	match=nextPage.findall(a)
	for url in match:
		info = IMDbClient._Info()
		url = url.replace("&amp;", "&")
		url = url.replace("&gps", "gps")
		url= ("http://members.easynews.com"+url).replace("http://", "http://"+settings[ "username" ]+":"+settings[ "password" ]+"@")
		print "NEXT EASY: "+url
		info.title = "~Next~"
		info.poster = None
		addDir(info.title,url,1,info)
		del info

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

       
def addLink(name,url,info):
	ok = True
	iconimage = info.poster
	
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( "video", { "Title": info.title, "Year": info.year, "Plot": info.plot, "PlotOutline": info.tagline, "MPAA": info.mpaa, "Genre": info.genre, "Studio": info.studio, "Director": info.director, "Duration": info.duration, "Cast": info.cast } )


	try:
                # set context menu items
                action1 = "XBMC.RunPlugin(%s?Download=True)" % ( sys.argv[ 0 ], )
                liz.addContextMenuItems( [ ("Download", action1, ) ] )
        except:
                pass

	print "ADDLINKURL: "+url
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        
        return ok

def addDir(name,url,mode,info = ""):
	if (info.poster != None):
		iconimage = info.poster
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&imdb="+urllib.quote_plus(info.imdb)
	else:
		iconimage = ""
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if (info.poster != None):
	        liz.setInfo( "video", { "Title": info.title, "Year": info.year, "Plot": info.plot, "PlotOutline": info.tagline, "MPAA": info.mpaa, "Genre": info.genre, "Studio": info.studio, "Director": info.director, "Duration": info.duration, "Cast": info.cast, "Trailer": info.trailer } )
	else:
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def showCats():
	info = IMDbClient._Info()
	info.poster = None
        cat=[("http://www.vcdq.com/index.php?genre=5", "VCDQuality DVD RIPs")]
        for url,name in cat:
                addDir(name,url,1,info)

def showShows(url,name):
        shows=getChannelFeed(url,name)
        for url,info,mode in shows:
                addDir(info.title,url,mode,info)
                
def getListings(url,imdb):
	IMDbFetcher = IMDbClient.IMDbFetcher()
	info = IMDbFetcher.fetch_info( imdb, "512" )
        shows=getEasyListing(url)
        for title,link in shows:
                addLink(title,link,info)
def showVidlinks(url):
       addLink("WATCH DVD EPISODE",url)
        
        
params=get_params()
url=None
name=None
mode=None
imdb=None
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
try:
        imdb=urllib.unquote_plus(params["imdb"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IMDB: "+str(imdb)
print "Args: "+str(sys.argv[2])
if( sys.argv[ 2 ].startswith( "?Download" ) ):
	print "****************************DOWNLOAD**********************************"
        import xbmcplugin_download as download
        download.Main()
if mode==None or url==None or len(url)<1:
        print "categories"
        showCats()
elif mode==1:
        print "index of : "+url
        showShows(url,name)
elif mode==2:
        print "Easynews: "+url
	xbmc.log("Easynews: "+url)
        getListings(url, imdb)
elif mode==3:
        print "show eps: "+url+" - "+name
        showEpisodes(url)
elif mode==4:
        print "show vidlinks: "+url
        showVidLinks(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
