import urllib2, urllib, time, os, re
import xbmcplugin, xbmcgui, xbmc
from BeautifulSoup import BeautifulSoup
from mechanize import Browser

# hockeystreams xbmc video plugin v1.2.0b
# stream live and archived games directly to your television!
# http://code.google.com/p/hockeystreams
# http://f3ar.bravehost.com/xbmc/hockeystreams/
# f3ar007 -at- gmail.com

def ipException(url,username,password):
    path = os.getcwd()
    path = os.path.join(path, 'resources')
    date = open(path + '\\date.txt','r')
    date = date.read()
    if date == time.strftime('%A %B %d, %Y'):
        print 'Exception Already Added!'
    elif date != time.strftime('%A %B %d, %Y'):
        br = Browser()
        br.open(url)
        br.select_form(nr=0)
        br['username'] = username
        br['password'] = password
        br.submit()
        br.open(url+'/include/exception.inc.php')
        br.select_form(nr=0)
        br.submit()
        print 'Exception Added!'
        date = open(path + '\\date.txt','w')
        today = time.strftime('%A %B %d, %Y')
        date.write(today)
        date.close()

def categories():
    addDir('Live Streams','http://hockeystreams.com',1,'')
    addDir('Hockey Archives','http://hockeystreams.com',8,'')

def liveIndex(url):
    addDir('HQ Games',url,2,'')
    addDir('HD Games',url,3,'')
    addDir('HD-Plus Games',url,4,'')

def liveHqGames(url,usr,pwd):
    # find game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    resp = br.submit()
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/live_streams/.*[0-9]$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gamePage = url + ending
        gameName = os.path.dirname(gamePage)
        gameName = re.sub('_|/',' ',gameName)
        gameName = gameName[38:]
        addDir(gameName,gamePage,5,'')
        i = i + 1
    
def liveHqLinks(url,usr,pwd):
    # find direct link on game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'direct_link' in test.get('id',''):
            direct = test['value']
            addLink(name,direct,'')

def liveHdGames(url,usr,pwd):
    # find game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    resp = br.submit()
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/live_streams/.*hi-qual$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gamePage = url + ending
        gameName = os.path.dirname(gamePage)
        gameName = os.path.dirname(gameName)
        gameName = re.sub('_|/',' ',gameName)
        gameName = gameName[38:]
        addDir(gameName,gamePage,6,'')
        i = i + 1

def liveHdLinks(url,usr,pwd):
    # find direct link on game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'direct_link' in test.get('id',''):
            direct = test['value']
            addLink(name,direct,'')

def liveHdpGames(url,usr,pwd):
    # find game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    resp = br.submit()
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/live_streams/.*hi-qual-plus$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gamePage = url + ending
        gameName = os.path.dirname(gamePage)
        gameName = os.path.dirname(gameName)
        gameName = re.sub('_|/',' ',gameName)
        gameName = gameName[38:]
        addDir(gameName,gamePage,7,'')
        i = i + 1

def liveHdpLinks(url,usr,pwd):
    # find direct link on game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'direct_link' in test.get('id',''):
            direct = test['value']
            addLink(name,direct,'')

def archiveIndex(url):
    addDir('HQ Games','http://hockeystreams.com',9,'')
    addDir('HD Games','http://hockeystreams.com',10,'')
    addDir('HD-Plus Games','http://hockeystreams.com',11,'')

def archiveHqGames(url,usr,pwd,archiveDate):
    # find game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    url0 = url + '/hockey_archives/' + archiveDate
    resp = br.open(url0)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/hockey_archives/0/.*[0-9]$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gamePage = url + ending
        gameName = os.path.dirname(gamePage)
        gameName = re.sub('_|/',' ',gameName)
        gameName = gameName[43:]
        addDir(gameName,gamePage,12,'')
        i = i + 1

def archiveHqLinks(url,usr,pwd):
    # find direct link on game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'text' in test.get('type',''):
            direct = str(test['value'])
            addLink(name,direct,'')

def archiveHdGames(url,usr,pwd,archiveDate):
    # find game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    url0 = url + '/hockey_archives/' + archiveDate
    resp = br.open(url0)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/hockey_archives/0/.*hi-qual$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gamePage = url + ending
        gameName = os.path.dirname(gamePage)
        gameName = os.path.dirname(gameName)
        gameName = re.sub('_|/',' ',gameName)
        gameName = gameName[43:]
        addDir(gameName,gamePage,13,'')
        i = i + 1

def archiveHdLinks(url,usr,pwd):
    # find direct link on game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'text' in test.get('type',''):
            direct = str(test['value'])
            addLink(name,direct,'')
            
def archiveHdpGames(url,usr,pwd,archiveDate):
    # find game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    url0 = url + '/hockey_archives/' + archiveDate
    resp = br.open(url0)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/hockey_archives/0/.*hi-qual-plus$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gamePage = url + ending
        gameName = os.path.dirname(gamePage)
        gameName = os.path.dirname(gameName)
        gameName = re.sub('_|/',' ',gameName)
        gameName = gameName[43:]
        addDir(gameName,gamePage,14,'')
        i = i + 1
    
def archiveHdpLinks(url,usr,pwd):
    # find direct link on game page
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'text' in test.get('type',''):
            direct = str(test['value'])
            addLink(name,direct,'')
            
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

def addDir(name,url,mode,iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok = True
    point = xbmcgui.ListItem(name,iconImage='',thumbnailImage='')
    point.setInfo( type='Video',infoLabels={ 'Title' : name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=point,isFolder=True)

def addLink(name,url,iconimage):
    ok = True
    point = xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
    point.setInfo( type='Video', infoLabels={ 'Title': name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=point)

params = get_params()
url = None
name = None
mode = None
username = xbmcplugin.getSetting('username')
password = xbmcplugin.getSetting('password')
archiveDate = xbmcplugin.getSetting('archiveDate')
hs = 'http://hockeystreams.com'

try:
    url = urllib.unquote_plus(params['url'])
except:
    pass
try:
    name = urllib.unquote_plus(params['name'])
except:
    pass
try:
    mode=int(params['mode'])
except:
    pass   

if mode == None or url == None or len(url)<1:
    ipException(hs,username,password)
    categories()
elif mode == 1:
    liveIndex(url)
elif mode == 2:
    liveHqGames(url,username,password)
elif mode == 3:
    liveHdGames(url,username,password)
elif mode == 4:
    liveHdpGames(url,username,password)
elif mode == 5:
    liveHqLinks(url,username,password)
elif mode == 6:
    liveHdLinks(url,username,password)
elif mode == 7:
    liveHdpLinks(url,username,password)
elif mode == 8:
    archiveIndex(url)
elif mode == 9:
    archiveHqGames(url,username,password,archiveDate)
elif mode == 10:
    archiveHdGames(url,username,password,archiveDate)
elif mode == 11:
    archiveHdpGames(url,username,password,archiveDate)
elif mode == 12:
    archiveHqLinks(url,username,password)
elif mode == 13:
    archiveHdLinks(url,username,password)
elif mode == 14:
    archiveHdpLinks(url,username,password)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
