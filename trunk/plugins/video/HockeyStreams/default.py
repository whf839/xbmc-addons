from BeautifulSoup import BeautifulSoup
from ClientForm import ParseResponse
from mechanize import Browser
import xbmcplugin, xbmcgui, xbmc
import ClientCookie, sys, re
import urllib2, urllib

#HockeyStreams.com Video Plug-in
#by f3ar007
#
#irc.freenode.net/xbmc-scripting

def categories():
    addDir('Hockey Archives','http://hockeystreams.com',1,'')
    addDir('Live Streams','http://hockeystreams.com',8,'')

def archiveIndex(url):
    print 'Archive Index Started.'
    print 'url: ' + str(url)
    addDir('HQ Games',url,2,'')
    addDir('HD Games',url,4,'')
    addDir('HD-Plus Games',url,6,'')

def liveIndex(url):
    print 'Live Index Started.'
    print 'url: ' + str(url)
    addDir('HQ Games',url,9,'')
    addDir('HD Games',url,11,'')
    addDir('HD-Plus Games',url,13,'')

def aHQgames(url,date,usr,pwd):
    print 'url: ' + str(url)
    print 'date: ' + str(date)
    print 'usr: ' + str(usr)
    print 'pwd: ' + str(pwd)
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    archUrl = url + '/hockey_archives' + date
    print 'archUrl: ' + archUrl
    resp3 = ClientCookie.urlopen(archUrl)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/hockey_archives/0/.*[0-9]$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        archLink = url + ending
        print archLink
        gameName = re.sub('_|/',' ',ending)
        print i, gameName
        addDir(gameName[19:-5],archLink,3,'')
        i = i + 1

def aHQlinks(url,date,usr,pwd):
    print 'url: ' + url
    print 'name: ' + name
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    resp3 = ClientCookie.urlopen(url)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    print find
    for test in find:
        if 'text' in test.get('type', ''):
            directLink = str(test['value'])
            print directLink
            addLink(name,directLink,'')

def aHDgames(url,date,usr,pwd):
    print 'url: ' + str(url)
    print 'date: ' + str(date)
    print 'usr: ' + str(usr)
    print 'pwd: ' + str(pwd)
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    archUrl = url + '/hockey_archives' + date
    print 'archUrl: ' + archUrl
    resp3 = ClientCookie.urlopen(archUrl)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/hockey_archives/0/.*hi-qual$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        archLink = url + ending
        print archLink
        gameName = re.sub('_|/',' ',ending)
        print i, gameName
        addDir(gameName[19:-13],archLink,5,'')
        i = i + 1

def aHDlinks(url,date,usr,pwd):
    print 'url: ' + url
    print 'name: ' + name
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    resp3 = ClientCookie.urlopen(url)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    print find
    for test in find:
        if 'text' in test.get('type', ''):
            directLink = str(test['value'])
            print directLink
            addLink(name,directLink,'')

def aHDPgames(url,date,usr,pwd):
    print 'url: ' + str(url)
    print 'date: ' + str(date)
    print 'usr: ' + str(usr)
    print 'pwd: ' + str(pwd)
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    archUrl = url + '/hockey_archives' + date
    print 'archUrl: ' + archUrl
    resp3 = ClientCookie.urlopen(archUrl)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/hockey_archives/0/.*-plus$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        archLink = url + ending
        print archLink
        gameName = re.sub('_|/',' ',ending)
        print i, gameName
        addDir(gameName[19:-18] + ' HD-Plus',archLink,7,'')
        i = i + 1

def aHDPlinks(url,date,usr,pwd):
    print 'url: ' + url
    print 'name: ' + name
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    resp3 = ClientCookie.urlopen(url)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    print find
    for test in find:
        if 'text' in test.get('type', ''):
            directLink = str(test['value'])
            print directLink
            addLink(name,directLink,'')

def lHQgames(url,usr,pwd):
    print 'url: ' + url
    print 'usr: ' + usr
    print 'pwd: ' + pwd
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)
    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd
    resp1 = ClientCookie.urlopen(form.click())
    liveUrl = url
    print 'liveUrl: ' + liveUrl
    resp2 = ClientCookie.urlopen(liveUrl)
    html = resp2.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/live_streams/.*[0-9]$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gameUrl = url + ending
        gameName = re.sub('_|/',' ',ending)
		# gameName = os.path.dirname(gameName)
        addDir(gameName,gameUrl,10,'')
        i = i + 1
        
def lHQlinks(url,usr,pwd):
    print 'url: ' + url
    print 'usr: ' + usr
    print 'pwd: ' + pwd
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    resp3 = ClientCookie.urlopen(url)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    print find
    for test in find:
        if 'direct_link' in test.get('id', ''):
            directLink = str(test['value'])
            print directLink
            addLink(name,directLink,'')

def lHDgames(url,usr,pwd):
    print 'url: ' + url
    print 'usr: ' + usr
    print 'pwd: ' + pwd
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)
    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd
    resp1 = ClientCookie.urlopen(form.click())
    liveUrl = url
    print 'liveUrl: ' + liveUrl
    resp2 = ClientCookie.urlopen(liveUrl)
    html = resp2.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/live_streams/.*hi-qual$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gameUrl = url + ending
        gameName = re.sub('_|/',' ',ending)
        addDir(gameName[14:-13],gameUrl,12,'')
        i = i + 1

def lHDlinks(url,usr,pwd):
    print 'url: ' + url
    print 'usr: ' + usr
    print 'pwd: ' + pwd
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    resp3 = ClientCookie.urlopen(url)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    print find
    for test in find:
        if 'direct_link' in test.get('id', ''):
            directLink = str(test['value'])
            print directLink
            addLink(name,directLink,'')
            
def lHDPgames(url,usr,pwd):
    print 'url: ' + url
    print 'usr: ' + usr
    print 'pwd: ' + pwd
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)
    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd
    resp1 = ClientCookie.urlopen(form.click())
    liveUrl = url
    print 'liveUrl: ' + liveUrl
    resp2 = ClientCookie.urlopen(liveUrl)
    html = resp2.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll(attrs={ 'href' : re.compile('/live_streams/.*-plus$') } )
    i = 0
    for test in find:
        ending = str(test['href'])
        gameUrl = url + ending
        gameName = re.sub('_|/',' ',ending)
        addDir(gameName[14:-13],gameUrl,14,'')
        i = i + 1

def lHDPlinks(url,usr,pwd):
    print 'url: ' + url
    print 'usr: ' + usr
    print 'pwd: ' + pwd
    req = ClientCookie.Request(url)
    resp = ClientCookie.urlopen(req)

    forms = ParseResponse(resp, backwards_compat=False)
    form = forms[0]
    form['username'] = usr
    form['password'] = pwd

    resp1 = ClientCookie.urlopen(form.click())
    resp2 = resp1.read()

    resp3 = ClientCookie.urlopen(url)
    html = resp3.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    print find
    for test in find:
        if 'direct_link' in test.get('id', ''):
            directLink = str(test['value'])
            print directLink
            addLink(name,directLink,'')
    
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
    ok = True
    point = xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
    point.setInfo( type='Video', infoLabels={ 'Title': name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=point)

def addDir(name,url,mode,iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok = True
    point = xbmcgui.ListItem(name, iconImage='', thumbnailImage='')
    point.setInfo( type='Video', infoLabels={ 'Title': name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=point,isFolder=True)

params = get_params()
url = None
name = None
mode = None

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

print 'url: ' + str(url)
print 'name: ' + str(name)
print 'mode: ' + str(mode)

if mode == None or url == None or len(url)<1:
    if xbmcplugin.getSetting('username') == 'enter user':
        xbmcplugin.openSettings(sys.argv[0])
    print 'Begin Categories.'
    print 'sys.argv[0]: ' + sys.argv[0]
    print 'sys.argv[1]: ' + sys.argv[1]
    print 'sys.argv[2]: ' + sys.argv[2]
    categories()
elif mode == 1:
    print 'Begin Archived Index.'
    print 'url: ' + url
    print 'sys.argv[0]: ' + sys.argv[0]
    print 'sys.argv[1]: ' + sys.argv[1]
    print 'sys.argv[2]: ' + sys.argv[2]
    archiveIndex(url)
elif mode == 2:
    print 'Begin Listing Archived HQ Games.'
    date = xbmcplugin.getSetting('archiveDate')
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    aHQgames(url,date,username,password)
elif mode == 3:
    print 'Begin Listing Archived HQ Links.'
    date = xbmcplugin.getSetting('archiveDate')
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    aHQlinks(url,date,username,password)
elif mode == 4:
    print 'Begin Listing Archived HD Games.'
    date = xbmcplugin.getSetting('archiveDate')
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    aHDgames(url,date,username,password)
elif mode == 5:
    print 'Begin Listing Archived HD Links.'
    date = xbmcplugin.getSetting('archiveDate')
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    aHDlinks(url,date,username,password)
elif mode == 6:
    print 'Begin Listing Archived HD-Plus Games.'
    date = xbmcplugin.getSetting('archiveDate')
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    aHDPgames(url,date,username,password)
elif mode == 7:
    print 'Begin Listing Archived HD-Plus Links.'
    date = xbmcplugin.getSetting('archiveDate')
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    aHDPlinks(url,date,username,password)
elif mode == 8:
    print 'Beging Listing Live Choices.'
    liveIndex(url)
elif mode == 9:
    print 'Begin Listing Live HQ Games.'
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    lHQgames(url,username,password)
elif mode == 10:
    print 'Begin Listing Live HQ Links.'
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    lHQlinks(url,username,password)
elif mode == 11:
    print 'Begin Listing Live HD Games.'
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    lHDgames(url,username,password)
elif mode == 12:
    print 'Begin Listing Live HD Links.'
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    lHDlinks(url,username,password)
elif mode == 13:
    print 'Begin Listing Live HD-Plus Games.'
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    lHDPgames(url,username,password)
elif mode == 14:
    print 'Begin Listing Live HD-Plus Links.'
    username = xbmcplugin.getSetting('username')
    password = xbmcplugin.getSetting('password')
    lHDPlinks(url,username,password)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
