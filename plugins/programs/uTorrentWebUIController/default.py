import urllib2, urllib, time, sys, os, re
import xbmcplugin, xbmcgui, xbmc
from mechanize import Browser
from ClientForm import ParseResponse
import ClientForm

# uTorrent WebUI Controller v1.2.0
# f3ar007@gmail.com
# http://f3ar007.com/xbmc

class Items(object):
    def __init__(self):

        self.br = Browser()
        self.ip = xbmcplugin.getSetting('ip')
        self.port = xbmcplugin.getSetting('port')
        self.usr = xbmcplugin.getSetting('usr')
        self.pwd = xbmcplugin.getSetting('pwd')
        self.tdir = xbmcplugin.getSetting('tdir')

        self.lang = xbmc.Language(os.getcwd()).getLocalizedString

        self.dialog = xbmcgui.Dialog()

i = Items()
baseurl = 'http://'+i.ip+':'+i.port+'/gui/?token='

def getToken():
    tokenUrl = 'http://'+i.ip+':'+i.port+'/gui/token.html'

    i.br.add_password(tokenUrl,i.usr,i.pwd)

    response = i.br.open(tokenUrl)
    data = response.read()

    match = re.compile("<div id='token' style='display:none;'>(.+?)</div>").findall(data)
    token = match[0]

    return token

def getList():
    token = getToken()
    url = baseurl + token + '&list=1'
    i.br.add_password(url,i.usr,i.pwd)
    response = i.br.open(url)
    data = response.read()
    data = data.split('\n')
    torrentList = []
    for line in data:
        if len(line) > 80:
            torrentList.append(line)
            print line
    return torrentList

def updateList():
    torrentList = getList()
    tupList = []
    c = 0
    for num in torrentList:
        tor = torrentList[c]
        tor = tor.split(',')
        hashnum = tor[0]
        hashnum = hashnum[2:-1]
        status = tor[1]
        torname = tor[2]
        complete = tor[4]
        complete = int(complete)
        complete = complete / 10.0
        tup = (hashnum, status, torname, complete)
        tupList.append(tup)
        c = c + 1
    return tupList

def getNewStatus():
    c = 0
    nameStatus = []
    hashStatus = {}
    tupList = updateList()
    for iterator in tupList:
        hashnum, bw, name, complete = tupList[c]
        c = c + 1
        tup = (bw, name)
        hashStatus[hashnum] = bw
        nameStatus.append(tup)
    return nameStatus, hashStatus, tupList

def listTorrents():
    nameStatus, hashStatus, tupList = getNewStatus()
    c = 0
    mode = 1
    for iterator in nameStatus:
        (bw, name) = nameStatus[c]
        if int(bw) in (169,232,233):
            thumb = os.path.join(os.getcwd(),'pause.png')
        elif int(bw) in (130,137,200,201):
            thumb = os.path.join(os.getcwd(),'play.png')
        elif int(bw) in (128,136):
            thumb = os.path.join(os.getcwd(),'stop.png')
        elif int(bw) == 200:
            thumb = os.path.join(os.getcwd(),'queued.png')
        else:
            thumb = os.path.join(os.getcwd(),'unknown.png')
        url = baseurl
        hashnum, junk1, junk2, complete = tupList[c]
        c = c + 1
        mode = mode
        addDir(name,url,mode,thumb,hashnum)
        mode = mode + 1

def performAction(selection):
    sel = i.dialog.select(i.lang(32001),[i.lang(32002),i.lang(32003),i.lang(32004),i.lang(32005),i.lang(32006),i.lang(32007),i.lang(32008)])
    token = getToken()
    i.br.add_password(baseurl,i.usr,i.pwd)
    if sel == 0:
        token = getToken()
        i.br.open(baseurl+token+'&action=pause&hash='+selection)
        xbmc.executebuiltin('Container.Update')
    if sel == 1:
        token = getToken()
        i.br.open(baseurl+token+'&action=unpause&hash='+selection)
        xbmc.executebuiltin('Container.Update')
    if sel == 2:
        token = getToken()
        i.br.open(baseurl+token+'&action=start&hash='+selection)
        xbmc.executebuiltin('Container.Update')
    if sel == 3:
        token = getToken()
        i.br.open(baseurl+token+'&action=stop&hash='+selection)
        xbmc.executebuiltin('Container.Update')
    if sel == 4:
        token = getToken()
        i.br.open(baseurl+token+'&action=forcestart&hash='+selection)
        xbmc.executebuiltin('Container.Update')
    if sel == 5:
        token = getToken()
        i.br.open(baseurl+token+'&action=remove&hash='+selection)
        xbmc.executebuiltin('Container.Update')
    if sel == 6:
        token = getToken()
        i.br.open(baseurl+token+'&action=removedata&hash='+selection)
        xbmc.executebuiltin('Container.Update')

def pauseAll():
    tupList = updateList()
    c = 0
    for num in tupList:
        hashnum, junk0, junk1, junk2 = tupList[c]
        token = getToken()
        url = baseurl + token + '&action=pause&hash='+hashnum
        i.br.add_password(url,i.usr,i.pwd)
        i.br.open(url)
        c = c + 1

def resumeAll():
    tupList = updateList()
    c = 0
    for num in tupList:
        hashnum, junk0, junk1, junk2 = tupList[c]
        token = getToken()
        url = baseurl + token + '&action=unpause&hash='+hashnum
        i.br.add_password(url,i.usr,i.pwd)
        i.br.open(url)
        c = c + 1

def stopAll():
    tupList = updateList()
    c = 0
    for num in tupList:
        hashnum, junk0, junk1, junk2 = tupList[c]
        token = getToken()
        url = baseurl + token + '&action=stop&hash='+hashnum
        i.br.add_password(url,i.usr,i.pwd)
        i.br.open(url)
        c = c + 1

def startAll():
    tupList = updateList()
    c = 0
    for num in tupList:
        hashnum, junk0, junk1, junk2 = tupList[c]
        token = getToken()
        url = baseurl + token + '&action=start&hash='+hashnum
        i.br.add_password(url,i.usr,i.pwd)
        i.br.open(url)
        c = c + 1

def limitSpeeds():
    upLimit = i.dialog.numeric(0,i.lang(32009))
    downLimit = i.dialog.numeric(0,i.lang(32010))
    token = getToken()
    url = baseurl + token + '&action=setsetting&s=max_ul_rate&v='+upLimit+'&s=max_dl_rate&v='+downLimit

def addFiles():
    tdir = i.tdir
    print tdir
    tlist = os.listdir(tdir)
    c = 0
    for iterator in tlist:
        tfile = tdir + tlist[c]
        tfile = str(tfile)
        token = getToken()
        html = """<html>
<body>
<form enctype="multipart/form-data" method="POST" action="%s%s&action=add-file">
<input type="file" name="torrent_file">
<br>
<input type="submit" value="Send">
</body>
</html>
""" % (baseurl,token)
        f = open(os.path.join(os.getcwd(),'form.html'),'w')
        f.write(html)
        f.close()
        f = open(os.path.join(os.getcwd(),'form.html'),'r')
        forms = ClientForm.ParseFile(f, 'http://f3ar007.com/xbmc/example.html', backwards_compat=False)
        f.close()
        form = forms[0]
        form.add_file(open(tfile))
        i.br.add_password(baseurl+token+'&action=add-file&s='+tfile,i.usr,i.pwd)
        i.br.open(form.click(nr=0))
        c = c + 1
    import time
    time.sleep(1)
    xbmc.executebuiltin('Container.Update')
        
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

def addDir(name,url,mode,iconimage,hashNum):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&hashNum="+str(hashNum)
    ok = True
    point = xbmcgui.ListItem(name,thumbnailImage=iconimage)
    rp = "XBMC.RunPlugin(%s?mode=%s)"
    point.addContextMenuItems([(i.lang(32011), rp % (sys.argv[0], 1000)),(i.lang(32012), rp % (sys.argv[0], 1001)),(i.lang(32013), rp % (sys.argv[0], 1002)),(i.lang(32014), rp % (sys.argv[0], 1003)),(i.lang(32015), rp % (sys.argv[0], 1004)),(i.lang(32016), rp % (sys.argv[0], 1005))],replaceItems=True)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=point,isFolder=False)

params = get_params()
url = None
name = None
mode = 0
hashNum = None

try:
    url = urllib.unquote_plus(params['url'])
except:
    pass
try:
    name = urllib.unquote_plus(params['name'])
except:
    pass
try:
    mode = int(params['mode'])
except:
    pass
try:
    hashNum = urllib.unquote_plus(params['hashNum'])
except:
    pass

if mode == 0:
    listTorrents()

elif mode == 1000:
    pauseAll()
    time.sleep(1)
    xbmc.executebuiltin('Container.Update')

elif mode == 1001:
    resumeAll()
    time.sleep(1)
    xbmc.executebuiltin('Container.Update')

elif mode == 1002:
    stopAll()
    time.sleep(1)
    xbmc.executebuiltin('Container.Update')

elif mode == 1003:
    startAll()
    time.sleep(1)
    xbmc.executebuiltin('Container.Update')

elif mode == 1004:
    limitSpeeds()

elif mode == 1005:
    addFiles()

elif 0 < mode < 1000:
    print 'hashnum: %s' %hashNum
    performAction(hashNum)

xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
