import urllib, urllib2
import os, re, sys, md5
import xbmc, xbmcgui, xbmcplugin

from elementtree.ElementTree import *
from pyamf.remoting.client import RemotingService

baseurl = 'http://www.nbc.com/'
liburl = 'http://www.nbc.com/Video/library/'
fullurl = 'http://www.nbc.com/Video/library/full-episodes/'
weburl = 'http://www.nbc.com/Video/library/webisodes/'

showsxml_url = 'http://www.nbc.com/assets/xml/video/shows.xml'

def getHTML( url ):
        try:
                print 'NBC Universal --> getHTML :: url = '+url
                req = urllib2.Request(url)
                req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)'),
                                  ('Referer', 'http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf')]
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                return link

#Process NBC Vid Library page for videos or shows
def processHTML( url ):
        items = getHTML(url)
        #<div id="scet_browse_pager"> <!-- #browse_results -->
        items = re.sub('\n', '', items)
        items = re.sub('\t', '', items)
        topmenu=re.compile('<!-- #video_lib -->.*<div id="scet_browse_pager">').findall(items)[0]
        match=re.compile('<li><a href="(.+?)" title="(.+?)"><img src="(.+?)" alt="(.+?)" width="80" height="45" /></a><p>').findall(topmenu)
        shows = []
        for url, name, thumbnail , name2 in match:
                show = []
                show.append(url)
                show.append(name)
                show.append(thumbnail)
                shows.append(show)
        return shows

def processSHOWFULL( url ):
        html = getHTML(url)
        match=re.compile('<!-- debug info --><a href="(.+?)" title="(.+?)"><img src="(.+?)"').findall(html)
        return match

#Process Full Episode or Season Vid Library page.
def processFULL ( url ):
        html = getHTML(url)
        match=re.compile('<a class="list_full_det_thumb" href="(.+?)" title="(.+?)"><img src="(.+?)"').findall(html)
        return match

#Get show list
def processSHOWS(url):
        url = 'http://www.nbc.com/Video/library/'
        items = getHTML(url)
        items = re.sub('\n', '', items)
        topmenu=re.compile('<h2>Video Library</h2>.*<!-- #video_lib -->').findall(items)[0]
        topmenu=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(topmenu)
        shows = []
        for url, sho in topmenu:
                show = []
                show.append(url)
                show.append(sho)
                show.append('')#Blank thumb
                shows.append(show)
        return shows

#returns showlist
def shows():
        shows = processSHOWFULL(fullurl)
        #shows = shows + processSHOWFULL(weburl)
        #shows = processSHOWS(liburl)
        return shows
       
def episodes(url):
        #episodes = processFULL(url)
        #episodes = processHTML(url)
        if 'episodes' in url:
                url = url.split('episodes/')[0] + 'episodes/init.xml'                
        else:
                url = url.split('categories/')[0] + 'episodes/init.xml'
        episodes = episodesxml(url)
        return episodes

def episodesxml(episodesurl):
        episodesxml = getHTML(episodesurl)
        xml = ElementTree(fromstring(episodesxml))
        episodes = []
        for ep in xml.getroot().findall('episodes/episode'):
                name = ep.find('epiTitle').text
                epiNumber = ep.find('epiNumber').text
                smallthumb = ep.find('epiImage').text
                plot = ep.find('epiDescription').text
                pid = smallthumb.replace('http://video.nbc.com/nbcrewind2/thumb/','').replace('_large.jpg','')
                vid = ep.find('videoID').text
                finalname = epiNumber + ': ' + name
                episode = []
                episode.append(vid)
                episode.append(finalname)
                episode.append(smallthumb)
                episodes.append(episode)
        return episodes


#Sends over AMF the VID with parameters to get smil from AMF gateway
#figure out last 2 parameters. most likely decompile player. 
def getsmil(vid):
        gw = RemotingService(url='http://video.nbcuni.com/amfphp/gateway.php',
                     referer='http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf',
                     user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)',
                     )
        ClipAll_service = gw.getService('getClipInfo.getClipAll')
        geo  ="US"
        num1 = "632"
        num2 = "-1"
        response = ClipAll_service(vid,geo,num1,num2)
        url = 'http://video.nbcuni.com/' + response['clipurl']
        return url

#get rtmp host and app from amf server congfig. gateway: http://video.nbcuni.com/amfphp/gateway.php Service: getConfigInfo.getConfigAll
def getrtmp():
        #rtmpurl = 'rtmp://cp37307.edgefcs.net:80/ondemand?'
        gw = RemotingService(url='http://video.nbcuni.com/amfphp/gateway.php',
                     referer='http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf',
                     user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)',
                     )
        ClipAll_service = gw.getService('getConfigInfo.getConfigAll')
        #Not sure where this number is coming from need to look further at action script.
        num1 = "17010"
        response = ClipAll_service(num1)
        rtmphost= response['akamaiHostName'] 
        app = response['akamaiAppName']
        rtmpurl = 'rtmp://'+rtmphost+':80/'+app+'?'
        return rtmpurl


#constant right now. not sure how to get this be cause sometimes its another swf module the player loads that access the rtmp server
def getswfUrl():
        swfUrl = "http://www.nbc.com/assets/video/3-0/swf/NBCVideoApp.swf"
        return swfUrl


#INTERNATIONAL MODE   

def showsxml():        
        showsxml=getHTML(showsxml_url)
        xml = ElementTree(fromstring(showsxml))
        for sh in xml.getroot().findall('show'):
                sh.find('name').text
                sh.find('link').text

def getsmilxml(pid,name):
        url = 'http://video.nbcuni.com/nbcrewind2/smil/' + pid + '.smil'
        PLAYRTMP(url, name)
