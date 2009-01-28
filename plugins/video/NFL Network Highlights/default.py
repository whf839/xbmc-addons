
__plugin__ = "NFL Network Highlights"
__author__ = "MDPauley"
__url__ = ""
__version__ = "0.0.5"

import urllib, urllib2, re
import string, os, time, datetime
import xbmc, xbmcgui, xbmcplugin

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)

def catsInitial():
	addDir('Featured','http://www.nfl.com/ajax/videos?categoryId=featured', 1 , '')
	addDir('NFL Network','http://www.nfl.com/ajax/videos?categoryId=featured', 2 , '')
	addDir('Teams','http://www.nfl.com/ajax/videos?categoryId=featured', 3 , '')
	addDir('Highlights','http://www.nfl.com/ajax/videos?categoryId=highlights', 50 , '')
	addDir('NFL Films', 'http://nfl.com/ajax/videos?categoryId=nflFilms', 50, '')
	addDir('Events', 'http://nfl.com/ajax/videos?categoryId=events', 50, '')
	addDir('Search', 'search', 25, '')
	
def catsFeatured():
	addDir('Featured Videos','http://www.nfl.com/ajax/videos?categoryId=featured', 50 , '')
	addDir('Video Picks of the Day','http://www.nfl.com/ajax/videos?categoryId=featured&filter=day-picks', 50 , '')
	addDir('Game Previews','http://www.nfl.com/ajax/videos?categoryId=featured&filter=previews', 50 , '')
	addDir('Can\'t-Miss Plays','http://www.nfl.com/ajax/videos?categoryId=featured&filter=cant-miss-plays', 50 , '')
	addDir('Rookie of the Week','http://www.nfl.com/ajax/videos?categoryId=featured&filter=rookies', 50 , '')
	addDir('Defensive Player of the Week','http://www.nfl.com/ajax/videos?categoryId=featured&filter=players-defense', 50 , '')
	addDir('Air & Ground Players of the Week','http://www.nfl.com/ajax/videos?categoryId=featured&filter=players-air-and-ground', 50 , '')
	addDir('Coach of the Week','http://www.nfl.com/ajax/videos?categoryId=featured&filter=coaches', 50 , '')

def catsNFLNetwork():
	addDir('NFL Total Access','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=nfl-total-access', 50 , 'http://www.nfl.com/img/video/logos/total_access.gif')
	addDir('Team Cam','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=team-cam', 50 , 'http://www.nfl.com/img/video/logos/team_cam.gif')
	addDir('NFL GameDay','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=nfl-gameday', 50 , 'http://www.nfl.com/img/video/logos/gameday.gif')
	addDir('NFL Replay','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=nfl-replay', 50 , 'http://www.nfl.com/img/video/logos/replay.gif')
	addDir('Playbook','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=playbook', 50 , 'http://www.nfl.com/img/video/logos/playbook.gif')
	addDir('College Football Now','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=college-daily', 50 , 'http://www.nfl.com/img/video/logos/college_scoreboard.gif')
	addDir('NFL Top Ten','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=nfl-top-10', 50 , 'http://www.nfl.com/img/video/logos/top_ten.gif')
	addDir('Inside Training Camp','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=in-training-camp', 50 , 'http://www.nfl.com/img/video/logos/training_camp.gif')
	addDir('Path to the Draft','http://www.nfl.com/ajax/videos?categoryId=nflNetwork&filter=path-draft', 50 , 'http://www.nfl.com/img/video/logos/path_draft.gif')

def mkTeamDir():
        req = urllib2.Request('http://www.nfl.com/videos')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()	
        code=re.sub('\r','',link)
        code=re.sub('\n',' ',code)
        code=re.sub('\t',' ',code)
        code=re.sub('  ','',code)
        response.close()
	code=code.split('<select class=\"advFields\" name=\"advancedTeam\">')
	code=code[1].split('</select>')
	p=re.compile('<option value=\"(.+?)\">(.+?)</option>')
	match=p.findall(code[0])
        for teamcode, teamname in match:
                addDir(teamname,'http://www.nfl.com/ajax/videos?categoryId=teams&teamId=' + teamcode, 50 , '')	
        
"""
	INDEX()
	Parses the data to create the filelist
"""
def listvideos(data):
	res=[]
	#this is where the fun starts, so we'll print some text here to
	#locate this section of code in the boxee debug logs.
	print '**listvideos()'
		
        req = urllib2.Request(data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&#39;','',link)
        code2=re.sub('&amp;','&',code)
        response.close()
        p=re.compile('\"filePath\":\"(.+?)\",\"fileName\":\"(.+?)\",\"controlPanelImage\":\"(.+?)\",\"mainTitle\":\"(.+?)\".+?\"captionBlurb\":\"(.+?)\".+?\"thumbRunTime\":\"(.+?)\",')
        match=p.findall(code2)
        for filePath, fileName, controlPanelImage, mainTitle, captionBlurb, thumbRunTime in match:
                res.append((filePath, fileName, controlPanelImage, mainTitle, captionBlurb, thumbRunTime))     
        for filePath, fileName, controlPanelImage, mainTitle, captionBlurb, thumbRunTime in res:
		videoinfo = {'Title': mainTitle, "Date": "2009-01-01", 'Plot': captionBlurb, 'Genre': 'Sports', 'Duration': thumbRunTime}
                addLink(filePath + fileName, controlPanelImage, mainTitle, videoinfo)

def listQvideos(data):
	res=[]
	#this is where the fun starts, so we'll print some text here to
	#locate this section of code in the boxee debug logs.
	print '**listvideos()'
		
        req = urllib2.Request(data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&#39;','',link)
        code2=re.sub('&amp;','&',code)
        response.close()
        p=re.compile('\"filePath\":\"(.+?)\",\"fileName\":\"(.+?)\",\"controlPanelImage\":\"(.+?)\",\"mainTitle\":\"\".+?\"captionBlurb\":\"(.+?)\".+?\"thumbRunTime\":\"(.+?)\",')
        match=p.findall(code2)
        for filePath, fileName, controlPanelImage, captionBlurb, thumbRunTime in match:
                res.append((filePath, fileName, controlPanelImage, captionBlurb, thumbRunTime))     
        for filePath, fileName, controlPanelImage, captionBlurb, thumbRunTime in res:
		videoinfo = {'Title': captionBlurb, "Date": "2009-01-01", 'Plot': captionBlurb, 'Genre': 'Sports', 'Duration': thumbRunTime}
                addLink(filePath + fileName, controlPanelImage, captionBlurb, videoinfo)

"""
	addLink()
	this function simply adds a media link to boxee's current screen
"""
def addLink(url, thumb, name, info):
	ok=True
	liz=xbmcgui.ListItem( name, iconImage="DefaultVideo.png", thumbnailImage= thumb )
	liz.setInfo( type="Video", infoLabels=info )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

"""
	addDir()
	this function simply adds a directory link to boxee's current screen
"""
def addDir(name,url,mode,iconimage, plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	if plot:
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
	else:
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def Qsearch(title):
    keyb = xbmc.Keyboard('', title)
    keyb.doModal()
    if (keyb.isConfirmed()):
        term = keyb.getText()
    	term = re.sub(' ','+',term)
    	listQvideos('http://nfl.com/ajax/videos?categoryId=find&quickSearch=' + term)    

"""
	getParams()
	grab parameters passed by the available functions in this script
"""
def getParams():
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

#grab params and assign them if found
params=getParams()
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

#check $mode and execute that mode
if mode==None or url==None or len(url)<1:
    print "CATEGORY INDEX : "
    catsInitial()
elif mode==1:
    catsFeatured()
elif mode==2:
    catsNFLNetwork()
elif mode==3:
    mkTeamDir()
elif mode==25:
    Qsearch('Search')
elif mode==50:
    listvideos(url)
#xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
