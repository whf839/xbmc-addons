#!/usr/bin/env python

import os, re, glob
import xbmc,xbmcgui,xbmcplugin
from datetime import datetime

path = '/Volumes/RAID/Movies/EyeTV/EyeTV Archive'
def get_settings():
    settings = {}
    try:        
            settings['path'] =  xbmcplugin.getSetting( 'path' )
            return settings
    except:
            print "couldn't load settings"
            pass
settings=get_settings()
path=settings['path']

for dirpath, dirnames, filenames in os.walk(path):
    if dirpath.endswith(".eyetv"):
        if not dirpath.endswith("Live TV Buffer.eyetv"):
            # print 'Directory', dirpath
            for filename in filenames:
                if filename.endswith(".mpg"):
                    fqname=dirpath+'/'+filename
                    # print fqname
                    p=re.compile('.+/(.+).eyetv')
                    m=p.match(dirpath)
                    shortdirpath=m.group(1)
                    # print shortdirpath
                    statinfo = os.stat(fqname)
                    size = statinfo.st_size
                    filedate = statinfo.st_ctime
                    objdate=datetime.fromtimestamp(filedate)
                    date=objdate.strftime("%d/%m/%Y")
                    # %H:%M:%S")
                    # print size, date
                    fObj=dirpath+'/*.eyetvp'
                    filePl=str(glob.glob(fObj))
                    # print filePl                 
                    #filePl = filePl.replace("[", "")
                    #filePl = filePl.replace("]", "")
                    filePl = filePl.replace("\"", "")
                    # filePl = filePl.replace("'", "")
                    # print filePl
                    filePl = filePl.strip('[')
                    filePl = filePl.strip(']')
                    filePl = filePl.strip('\'')
                    # print filePl
                    if not filePl=="":
                        title=""
                        subtitle=""
                        episode=""
                        dsubtitle=""
                        depisode=""
                        plot=""
                        file = open(filePl)
                        pl=""
                        for line in file:
                            line = line.replace("\n", "")
                            line = line.replace("\t", "")
                            pl = pl + line
                        epg=str(pl)
                        # print epg
                        # p=re.compile(', \'TITLE\': [\'"](.*?)[\'"],')
                        p=re.compile('<key>TITLE</key><string>(.*?)</string>')
                        m=p.search(epg)
                        if m:
                            title=m.group(1)
                            title = title.strip()
                        #else:
                        #    print epg
                            # print title
                        # p=re.compile(', \'SUBTITLE\': [\'"](.*?)[\'"],')
                        p=re.compile('<key>SUBTITLE</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            subtitle=m.group(1)
                            subtitle = subtitle.strip()
                            if subtitle:
                                dsubtitle='.'+subtitle
                        # print subtitle
                        # p=re.compile(', \'EPISODENUM\': [\'"](.*?)[\'"],')
                        p=re.compile('<key>EPISODENUM</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            episode=m.group(1)
                            episode = episode.strip()
                            if episode:
                                depisode='.'+episode
                        # print episode
                        # p=re.compile(', \'DESCRIPTION\': [\'"](.*?)[\'"],')
                        p=re.compile('<key>DESCRIPTION</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            plot=m.group(1)
                            plot = plot.strip()
                        # print plot
                        libname=title+depisode+dsubtitle
                        # print libname
                    filePl=""
                    icon = "defaultVideo.png"
                    icon2 = "defaultVideoBig.png"
                    # title=shortdirpath
                    liz=xbmcgui.ListItem(shortdirpath, libname, iconImage=icon, thumbnailImage=icon2)
                    # liz.setInfo( type="Video", infoLabels={ "Title": libname, "Date":date, "Size":size, "Plot":plot, "Episode":episode} )
                    liz.setInfo( type="Video", infoLabels={ "Title": libname, "Date":date, "Size":size, "Plot":plot} )
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=fqname,listitem=liz)

#xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')                   
#xbmcplugin.addSortMethod(int(sys.argv[1]),  3)#date
#xbmcplugin.addSortMethod(int(sys.argv[1]), 10)#title
#xbmcplugin.addSortMethod(int(sys.argv[1]),  1)#filename
xbmcplugin.endOfDirectory(int(sys.argv[1]))
