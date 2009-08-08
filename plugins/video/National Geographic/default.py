
__scriptname__ = 'National Geographic'
__author__ = 'stacked [http://xbmc.org/forum/member.php?u=26908]'
__url__ = 'http://xbmc.org/forum/showthread.php?t=45132'
__svn_url__ = 'https://xbmc-addons.googlecode.com/svn/trunk/plugins/video/National%20Geographic/'
__date__ = '2009-08-08'
__version__ = "1.0"

import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, string, sys, os, traceback
HEADER = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2'
THUMBNAIL_PATH = os.path.join(os.getcwd().replace( ";", "" ),'resources','media')

def _check_for_update():
	print "National Geographic v"+__version__
	url = 'http://code.google.com/p/xbmc-addons/source/browse/trunk/plugins/video/National%20Geographic/default.py'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	ALL = re.compile('<td class="source">__version__ = &quot;(.+?)&quot;<br></td>').findall(a)
	for link in ALL :
		if link.find(__version__) != 0:
			newVersion=link
			dia = xbmcgui.Dialog()
			ok = dia.ok("National Geographic", 'Updates are available on SVN Repo Installer\n\n'+'Current Version: '+__version__+'\n'+'Update Version: '+newVersion)

def main():
	req=urllib2.Request('http://channel.nationalgeographic.com/channel/videos/feeds/cv/us/player_0000059.xml')
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	categories=re.compile('<categories>(.+?)</categories>', re.DOTALL).findall(data)
	name=re.compile('<name>(.+?)</name>').findall(categories[0])
	thumbnail=re.compile('<thumbnail>(.+?)</thumbnail>').findall(categories[0])
	datafile=re.compile('<datafile>(.+?)</datafile>').findall(categories[0])
	item_count=0
	for label in name:
		listitem=xbmcgui.ListItem(label=clean(label), iconImage=thumbnail[item_count], thumbnailImage=thumbnail[item_count])
		url=sys.argv[0]+"?mode=0&name="+urllib.quote_plus(clean(label))+"&url="+urllib.quote_plus(datafile[item_count])+"&cat="+urllib.quote_plus(clean(label))
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True)
		item_count+=1
	listitem=xbmcgui.ListItem(label='More Nat Geo Videos', iconImage=thumbnail[0], thumbnailImage=thumbnail[0])
	url=sys.argv[0]+"?mode=3&cat="+urllib.quote_plus('More Nat Geo Videos')
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True)

def categories(name,url,cat):
	req=urllib2.Request('http://channel.nationalgeographic.com/channel/videos/feeds/cv/us/'+url)
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	components=re.compile('<components>(.+?)</components>', re.DOTALL).findall(data)
	name=re.compile('<name>(.+?)</name>').findall(components[0])
	datafile=re.compile('<datafile>(.+?)</datafile>').findall(components[0])
	item_count=0
	for label in name:
		listitem=xbmcgui.ListItem(label=clean(label))
		url=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(clean(label))+"&url="+urllib.quote_plus(datafile[item_count])+"&cat="+urllib.quote_plus(cat+' / '+clean(label))
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True)
		item_count+=1

def playlist(name,url,cat):
	nexturl=url
	req=urllib2.Request('http://channel.nationalgeographic.com/channel/videos/feeds/cv/us/'+url)
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	videoCount=re.compile('<videoCount>(.+?)</videoCount>').findall(data)
	pageCount=re.compile('<pageCount>(.+?)</pageCount>').findall(data)
	if videoCount[0] == '0':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok('National Geographic', 'Error: No videos available')
		return
	prefixDefaultSort=re.compile('<prefixDefaultSort>(.+?)</prefixDefaultSort>').findall(data)
	prefixSortByName=re.compile('<prefixSortByName>(.+?)</prefixSortByName>').findall(data)
	prefixSortByDate=re.compile('<prefixSortByDate>(.+?)</prefixSortByDate>').findall(data)
	if xbmcplugin.getSetting('sortby') == '0':
		sortby=prefixDefaultSort[0]
	if xbmcplugin.getSetting('sortby') == '1':
		sortby=prefixSortByName[0]
	if xbmcplugin.getSetting('sortby') == '2':
		sortby=prefixSortByDate[0]
	url='http://channel.nationalgeographic.com/channel/videos/feeds/cv/us/'+sortby+str(page)+'.xml'
	req=urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	shortTitle=re.compile('<shortTitle>(.+?)</shortTitle>').findall(data)
	shortDescription=re.compile('<shortDescription>(.*?)</shortDescription>').findall(data)
	datafile=re.compile('<datafile>(.+?)</datafile>').findall(data)
	thumbnail=re.compile('<thumbnail type="url">(.+?)</thumbnail>').findall(data)
	item_count=0
	for name in shortTitle:
		label=str(int(item_count+1)+(9*(page-1)))+'. '+clean(name)+': '+clean(shortDescription[item_count])
		listitem=xbmcgui.ListItem(label=label, iconImage=thumbnail[item_count], thumbnailImage=thumbnail[item_count])
		listitem.setInfo( type="Video", infoLabels={ "Title": clean(name), "Plot": clean(shortDescription[item_count]), "Director": 'National Geographic', "Studio": 'National Geographic', "Genre": cat } )
		url=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(clean(name))+"&url="+urllib.quote_plus(datafile[item_count])+"&cat="+urllib.quote_plus(cat)+"&plot="+urllib.quote_plus(clean(shortDescription[item_count]))
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=False)
		item_count+=1
	if len(shortTitle) >= 9:
		listitem=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		url=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(cat)+"&url="+urllib.quote_plus(nexturl)+"&page="+str(int(page)+1)+"&cat="+urllib.quote_plus(cat)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True)
		
def getVideo(name,url,cat,plot):
	req=urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	video=re.compile('<video>(.+?)</video>').findall(data)
	req=urllib2.Request('http://video.nationalgeographic.com/video/cgi-bin/cdn-auth/cdn_tokenized_url.pl?slug='+video[0]+'&siteid=ngcchannelvideos')
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	tokenizedURL=re.compile('<tokenizedURL>(.+?)</tokenizedURL>').findall(data)
	req=urllib2.Request(tokenizedURL[0].replace('&amp;','&'))
	req.add_header('User-Agent', HEADER)
	response=urllib2.urlopen(req)
	data=response.read()
	response.close()
	serverName=re.compile('<serverName>(.+?)</serverName>').findall(data)
	appName=re.compile('<appName><!\[CDATA\[(.+?)\]\]></appName>').findall(data)
	streamName=re.compile('<streamName><!\[CDATA\[(.+?)\]\]></streamName>').findall(data)
	g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	listitem=xbmcgui.ListItem(name ,iconImage="DefaultVideo.png", thumbnailImage=g_thumbnail)
	listitem.setInfo( type="Video", infoLabels={ "Title": name, "Director": 'National Geographic', "Studio": 'National Geographic', "Genre": cat, "Plot": plot } )
	listitem.setProperty("PlayPath", streamName[0])
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play('rtmp://'+serverName[0]+'/'+appName[0], listitem)

def clean(name):
	remove=[('&amp;','&'),('&quot;','"'),('&#233;','e'),('&#8212;',' - '),('&#39;','\''),('&#46;','.'),('&#58;',':')]
	for trash, crap in remove:
		name=name.replace(trash,crap)
	return name
	
# More Videos
def sectionlist(cat):
	url='http://video.nationalgeographic.com/video/player/data/xml/sectionlist.xml'
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data=re.compile('<section id="(.+?)">(.+?)</section>').findall(a)
	cell=0
	for info in data:
		sectionid=data[cell][0]
		name=data[cell][1]
		name=clean(name)
		url='http://video.nationalgeographic.com/video/player/data/xml/section_'+sectionid+'.xml'
		li=xbmcgui.ListItem(name)
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat+' / '+name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		cell=cell+1

def section(url, name, cat):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data=re.compile('<children>(.+?)</children>', re.DOTALL).findall(a)
	catdata=re.compile('<category id="(.+?)" >').findall(data[0])
	title=re.compile('<name>(.+?)</name>').findall(data[0])
	check=re.compile('<hasVideo>(.+?)</hasVideo>').findall(data[0])
	cell=0
	for info in catdata:
		categoryid=catdata[cell]
		name=title[cell]
		name=clean(name)
		if (check[cell]=='true'):
			url='http://video.nationalgeographic.com/video/player/data/xml/category_assets_'+categoryid+'.xml'
			u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat+' / '+name)
		else:
			url='http://video.nationalgeographic.com/video/player/data/xml/category_'+categoryid+'.xml'
			u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat+' / '+name)
		thumb='http://video.nationalgeographic.com/video/player/media/featured_categories/'+categoryid+'_102x68.jpg'
		li=xbmcgui.ListItem(name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		cell=cell+1

def category(url, name, cat):
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data=re.compile('<children>(.+?)</children>', re.DOTALL).findall(a)
	catdata=re.compile('<category id="(.+?)" >').findall(data[0])
	title=re.compile('<name>(.+?)</name>').findall(data[0])
	cell=0
	for info in catdata:
		categoryid=catdata[cell]
		name=title[cell]
		name=clean(name)
		url='http://video.nationalgeographic.com/video/player/data/xml/category_assets_'+categoryid+'.xml'
		thumb='http://video.nationalgeographic.com/video/player/media/'+categoryid+'/'+categoryid+'_150x100.jpg'
		li=xbmcgui.ListItem(name)
		u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat+' / '+name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		cell=cell+1

def category_assets(url, name, cat):
	thisurl=url
	new=url[:-4]
	if ((page-1) != 0):
		req = urllib2.Request(new+'_'+str(int(page))+'.xml')
	else:
		req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data=re.compile('<videoasset refid="(.+?)">').findall(a)
	data2=re.compile('<title>(.+?)</title>').findall(a)
	data3=re.compile('<assetlist total="(.+?)" totalpages="(.+?)" page="(.+?)" pagesize="(.+?)">').findall(a)
	cell=0
	for info in data:
		refid=data[cell]
		name=data2[cell]
		name1=clean(name)
		name = str((cell+1)+((page-1)*10)-(1*(page-1)))+'. '+name1
		url='http://video.nationalgeographic.com/video/cgi-bin/cdn-auth/cdn_tokenized_url.pl?slug='+refid+'&siteid=popupmain'
		thumb='http://video.nationalgeographic.com/video/player/media/'+refid+'/'+refid+'_480x360.jpg'
		li=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name1)+"&url="+urllib.quote_plus(url)+"&cat="+urllib.quote_plus(cat)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
		cell=cell+1
	if (data3[0][1] != data3[0][2]):
		li=xbmcgui.ListItem("Next Page",iconImage="DefaultVideo.png", thumbnailImage=os.path.join(THUMBNAIL_PATH, 'next.png'))
		u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(thisurl)+"&page="+str(int(page)+1)+"&cat="+urllib.quote_plus(cat)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		
def playVideo(url, name, cat):
	saveName=name
	req = urllib2.Request(url)
	req.add_header('User-Agent', HEADER)
	f=urllib2.urlopen(req)
	a=f.read()
	f.close()
	data=re.compile('<tokenizedURL>(.+?)</tokenizedURL>').findall(a)
	url=data[0]
	url=url.replace('amp;','')
	badchars = '\\/:*?\"<>|'
	for c in badchars:
		name = name.replace(c, '')
	name=name+'.flv'
	g_thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	listitem=xbmcgui.ListItem(saveName ,iconImage="DefaultVideo.png", thumbnailImage=g_thumbnail)
	listitem.setInfo( type="Video", infoLabels={ "Title": saveName, "Director": 'National Geographic', "Studio": 'National Geographic', "Genre": cat } )
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(str(url),listitem)

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

params=get_params()
mode=None
name=None
url=None
page=1
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
        page=int(params["page"])
except:
        pass
try:
		cat=urllib.unquote_plus(params["cat"])
except:
        pass
try:
		plot=urllib.unquote_plus(params["plot"])
except:
        pass

if mode==None:
	cat=''
	_check_for_update()
	main()
elif mode==0:
	categories(name,url,cat)
elif mode==1:
	playlist(name,url,cat)
elif mode==2:
	getVideo(name,url,cat,plot)
elif mode==3:
	sectionlist(cat)
elif mode==4:
	section(url, name, cat)
elif mode==5:
	category(url, name, cat)
elif mode==6:
	category_assets(url, name, cat)
elif mode==7:
	playVideo(url, name, cat)
if len(cat) >= 35:
	cat = cat[:35]+'...'
xbmcplugin.setPluginCategory(int(sys.argv[1]), cat )
#xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
