from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import xbmcplugin, xbmcgui, xbmc, time, os, re, urllib

username        = xbmcplugin.getSetting('username')
password        = xbmcplugin.getSetting('password')
hockeystreams   = 'http://hockeystreams.com'
archivestreams  = 'http://hockeystreams.com/hockey_archives'
empty           = None
directLinks     = {}
games           = {}
hqStreams       = re.compile('/live_streams/.*[0-9]$')
hdStreams       = re.compile('/live_streams/.*hi-qual$')
hdpStreams      = re.compile('/live_streams/.*hi-qual-plus$')
hqArchives      = re.compile('/hockey_archives/0/.*[0-9]$')
hdArchives      = re.compile('/hockey_archives/0/.*hi-qual$')
hdpArchives     = re.compile('/hockey_archives/0/.*hi-qual-plus$')

def createDate():                                               ##core module
    archiveMonth    = xbmcplugin.getSetting('archiveMonth')
    archiveDay      = xbmcplugin.getSetting('archiveDay')
    archiveYear     = xbmcplugin.getSetting('archiveYear')

    archiveMonth    = str(int(archiveMonth)+1)
    archiveDay      = str(int(archiveDay)+1)

    if len(archiveMonth) == 1:
        archiveMonth = '0' + str(archiveMonth)
    elif len(archiveMonth) == 2:
        archiveMonth = archiveMonth

    if len(archiveDay) == 1:
        archiveDay = '0' + str(archiveDay)
    elif len(archiveMonth) == 2:
        archiveDay = str(archiveDay)

    if archiveYear == int('0') or '0':
        archiveYear = '2009'
    elif archiveYear == int('1') or '1':
        archiveYear = '2010'

    archiveDate = '/' + archiveMonth + '-' + archiveDay + '-' + archiveYear + '/'
    return archiveDate

def categories():
    addDir('Live Streams',hockeystreams,1,'')
    addDir('Archived Streams',hockeystreams,2,'')
    addDir('RSS Streams',hockeystreams,3,'')

def indexes(url,startNum):
    addDir('High Quality Games',url,startNum,'')
    addDir('High Definition Games',url,startNum+1,'')
    addDir('High Definition Plus Games',url,startNum+2,'')

def login(usr,pwd,url,selector):
    br = Browser()
    br.open(hockeystreams)                                      ##default login page, not passed url
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    if selector == 'login':                                     ##remove useless if and replace with first elif
        pass
    elif selector == 'browser':
        br.open(url)                                            ##open passed url
        return br
    elif selector == 'function':
        data = br.open(url)
        return (data,br)

def getGameNameGamePage(gameType):
    if gameType in (hqStreams,hdStreams,hdpStreams):
        foundGames = soupIt(username,password,hockeystreams,'attrs',gameType)
    elif gameType in (hqArchives,hdArchives,hdpArchives):
        archiveDate = createDate()
        foundGames = soupIt(username,password,archivestreams+archiveDate,'attrs',gameType)
    for test in foundGames:
        ending      = str(test['href'])
        gamePage    = hockeystreams + ending
        gameName    = os.path.dirname(gamePage)
        gameName    = re.sub('_|/',' ',gameName)
        if gameType in (hqStreams,hdStreams,hdpStreams):
            gameName = gameName[38:]
        elif gameType in (hqArchives,hdArchives,hdpArchives):
            gameName = gameName[43:]
        games[gameName] = gamePage
    del foundGames
    return games                                                ##return a dict with game name and page containing direct link

def getGameNameDirectLink(selector):
    games = getGameNameGamePage(selector)                       ##hqStreams,hdStreams,hdpStreams,etc
    for k,v in games.iteritems():
        foundGames = soupIt(username,password,v,'input',empty)  ##foundGames is BeautifulSoup.resultSet
        for test in foundGames:                                 ##get rid of this 'busy loop' in the next minor revision
            if 'direct_link' in test.get('id',''):
                directLink = test['value']
                directLinks[k] = directLink
    del selector
    return directLinks

def soupIt(usr,pwd,currentUrl,selector,gameType):
    (data,br)   = login(username,password,currentUrl,'function')
    html        = data.read()
    soup        = BeautifulSoup(''.join(html))
    if selector == 'attrs':
        found = soup.findAll(attrs={'href':gameType})
    elif selector == 'input':
        found = soup.findAll('input')
    del selector
    return found

def populateGames(selector):
    populated = getGameNameDirectLink(selector)
    for k,v in populated.iteritems():
        addLink(k,v,'')

##voinages' stuff I still don't understand, entirely.
##---------------------------------------------------

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

##---------------------------------------------------
##end of voinages' stuff.

params  = get_params()
url     = None
name    = None
mode    = None

try:
    url     = urllib.unquote_plus(params['url'])
except:
    pass
try:
    name    = urllib.unquote_plus(params['name'])
except:
    pass
try:
    mode    = int(params['mode'])
except:
    pass

if mode == None or url == None or len(url)<1:
    categories()
elif mode == 1:
    indexes(hockeystreams,4)
elif mode == 2:
    indexes(hockeystreams,7)
elif mode == 3:
    indexes(hockeystreams,10)
elif mode == 4:
    populateGames(hqStreams)
elif mode == 5:
    populateGames(hdStreams)
elif mode == 6:
    populateGames(hdpStreams)
elif mode == 7:
    populateGames(hqArchives)
elif mode == 8:
    populateGames(hdArchives)
elif mode == 9:
    populateGames(hdpArchives)
##rss stuff
##---------------------------------------------------

##elif mode >= 10:
##    import rssArchives
##    if mode == 10:
##        rssArchives.populateRSS('hq')
##    elif mode == 11:
##        rssArchives.populateRSS('hd')
##    elif mode == 12:
##        rssArchives.populateRSS('hdp')

##---------------------------------------------------
##end of rss stuff

xbmcplugin.endOfDirectory(int(sys.argv[1]))
