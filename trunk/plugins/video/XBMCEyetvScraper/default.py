#!/usr/bin/env python

# XBMCEyetvScraper
# version 1.51
# by prophead
# ThumbnailOverlayGenerator by Nic Wolfe (midgetspy)

# user variables, these are overidden by the gui settings
# ---------------
# my default path
path = '/Volumes/RAID/Movies/EyeTV/EyeTV Archive'

# my TV Show linked directory path
dummy = '/Volumes/RAID/Movies/TV'

# TOG
# requires Imagemagick, and ffmpeg
# 0=no thumbail overlays, 1=try thumbnail overlays
tog = 1

# TV Show linked directory (library) support
# 0=no linked directory support, 1=try to create linked directory
LDS = 1

# nfo file support
# requires LDS
# 0=no nfo file support, 1=try to create nfo files from Eyetv/thetvdb.com EPG data
nfo = 1

# thetvdb.com scraper support
# requires nfo
# 0=use Eyetv EPG data, 1=try to scrape thetvdb.com for data
STVDB = 1

# 1=Extended output in log
DEBUG = 0

# ---------------

import os, re, glob, sys
import xbmc,xbmcgui,xbmcplugin
from datetime import datetime

# set settings (Eyetv folder) from the XBMC interface
def get_settings():
    settings = {}
    try:        
            settings['path'] =  xbmcplugin.getSetting( 'path' )
            settings['dummy'] =  xbmcplugin.getSetting( 'dummy' )
            settings['EyetvTOG'] = xbmcplugin.getSetting( 'EyetvTOG' )
            return settings
    except:
            print "couldn't load settings"
            pass
# test for Boxee
#BoxeePath = os.getcwd()[:-1]+"/"
#p=re.compile('.+(oxee).+')
#m=p.match(BoxeePath)
#if not m:

# get settings from gui settings
settings=get_settings()
path=settings['path']
dummy=settings['dummy']
tog=settings['EyetvTOG']
if tog == "true":
    tog = 1

#else:
#    print "[XBMCEyetvScraper] - Boxee"

def go_tog(cmd, scandir):
    #  Author: Nic Wolfe (midgetspy)
    #  Contact: PM me on the xbmc.org forums
    #  Version: 0.3.3.EM
    
    ###########################
    ## Configuration Options ##
    ###########################
        # relative size of the overlays
    IMG_HEIGHT = 0.24
        # default to macport standards
    FFMPEG_PATH = '/opt/local/bin'
    FFMPEG_PROCESS = 'ffmpeg'
    IMAGEMAGICK_PATH = '/opt/local/bin'
    IMAGEMAGICK_IDENTIFY_PROCESS = 'identify'
    IMAGEMAGICK_COMPOSITE_PROCESS = 'composite'
    IMAGEMAGICK_CONVERT_PROCESS = 'convert'
    AUTOSCAN_EXTENSIONS = ('.mpg')
    
    # moved to global
    # 1=Extended output in log
    # DEBUG = 1
    
    # put the dimensions of your logos here (height/width)
    LOGO_RATIO = 1024/1024
    
    #################################################################################################################
    #################################################################################################################
    #################################################################################################################
    # Don't touch below this line unless you know what you're doing.
    SUCCESS = 1
    FAILURE = 2
    SKIPPED = 3
    IMG_MARGIN = 0.02
    
    import sys
    import shutil
    import os
    import re
    import subprocess
    
    
    def checkDependencies ():
        result = SUCCESS

        if not os.path.isfile(os.path.join(FFMPEG_PATH, FFMPEG_PROCESS)):
                print "ERROR: unable to find ffmpeg. Verify that it's installed and that FFMPEG_PATH is set correctly."
                result = FAILURE
        if not os.path.isfile(os.path.join(IMAGEMAGICK_PATH, IMAGEMAGICK_IDENTIFY_PROCESS)):
                print "ERROR: unable to find identify (part of ImageMagick). Verify that it's installed and that IMAGEMAGICK_PATH is set correctly."
                result = FAILURE
        if not os.path.isfile(os.path.join(IMAGEMAGICK_PATH, IMAGEMAGICK_COMPOSITE_PROCESS)):
                print "ERROR: unable to find composite (part of ImageMagick). Verify that it's installed and that IMAGEMAGICK_PATH is set correctly."
                result = FAILURE

        if result != SUCCESS:
                print "Quitting..."
                sys.exit()
    
    def doFile (filename, results=None):
        print "Doing overlays for "+filename

        if results == None:
                ffmpegResults = parseffmpegInfo(getffmpegInfo(filename))
        else:
                ffmpegResults = results

        if DEBUG:
                print "DEBUG: INFO: Scanned"+filename+"got", ffmpegResults

        if ffmpegResults == None:
                print "ERROR: unable to scan "+filename+" with ffmpeg"
                return FAILURE

        thumbName = changeExtension(filename, "tbn")
        thumbOrigName = changeExtension(filename, "tbn-orig")
        eyethumb = changeExtension(filename, "tiff")
        
        # if they have only tbn-orig then they want me to regenerate the thumb
        if os.path.isfile(thumbOrigName) and not os.path.isfile(thumbName):
                shutil.copyfile(thumbOrigName, thumbName)

        # if they have only a tbn (and not an eyetv tiff) I need to back it up then make the thumb
        elif os.path.isfile(thumbName) and not os.path.isfile(thumbOrigName) and not os.path.isfile(eyethumb):
                shutil.copyfile(thumbName, thumbOrigName)

        # if they have both I'm assuming it's done and leaving it alone
        elif os.path.isfile(thumbName) and os.path.isfile(eyethumb):
                print filename+" already has a generated thumb, skipping"
                return SKIPPED

        # no thumb files means nothing I can do
        # added support for no thumb, grab thumb from tiff
        else:
                thumbName = changeExtension(filename, "jpg")
                thumbOrigName = changeExtension(filename, "tiff")
                if os.path.isfile(thumbOrigName):
                        print filename+" converting eyetv tiff icon to jpg icon"
                        # convert to jpg
                        convProcCmd = os.path.join(IMAGEMAGICK_PATH, IMAGEMAGICK_CONVERT_PROCESS)+' \"'+thumbOrigName+'\" \"'+thumbName+'\"'
                        # convProcCmd = convProcCmd.replace("'", "\\'")
                        # convProcCmd = convProcCmd.replace('\"', '\\"')
                        if DEBUG:
                                print 'DEBUG: Convert command: '+convProcCmd
                        os.system(convProcCmd)
                        # use XBMC tbn standard
                        XBMCthumbName = changeExtension(filename, "tbn")
                        shutil.move(thumbName, XBMCthumbName)
                        thumbName = XBMCthumbName
                else:
                        print "ERROR: no thumbnail found for"+filename
                        return FAILURE

        # get thumb size
        identifyProcCmd = (os.path.join(IMAGEMAGICK_PATH, IMAGEMAGICK_IDENTIFY_PROCESS), '-ping', thumbName)
        if DEBUG:
                print 'DEBUG: Identify command: ', identifyProcCmd
        identifyProc = subprocess.Popen(identifyProcCmd, stdout=subprocess.PIPE)
        identifyOutput = identifyProc.communicate()[0]
        thumbSize = [int(a) for a in identifyOutput[len(thumbName)+1:-1].split(' ')[1].split('x')]
        #thumbSize[0]=int(1024)
        #thumbSize[1]=int(1024)
        if DEBUG:
                print 'DEBUG: thumbsize=', thumbSize
        # use ImageMagick to overlay "images/" + ffmpegResults[1] + ".png" onto thumbName bottom left corner
        videoOverlayFilename = os.path.join(sys.path[0], 'EyetvTOG/images', ffmpegResults[1] + '.png')
        if not os.path.isfile(videoOverlayFilename):

                print "WARN: Couldn't find "+videoOverlayFilename+" skipping video overlay"
        else:
                videoImgProcCmd = (os.path.join(IMAGEMAGICK_PATH, IMAGEMAGICK_COMPOSITE_PROCESS), '-compose', 'atop', '-geometry', '1000x' + str(int(thumbSize[1]*IMG_HEIGHT)) + '+' + str(int(thumbSize[0]*IMG_MARGIN)) + '+' + str(int(thumbSize[1]*(1-IMG_HEIGHT)-thumbSize[0]*IMG_MARGIN)), videoOverlayFilename, thumbName, thumbName)
                videoImgProc = subprocess.Popen(videoImgProcCmd, stderr=subprocess.PIPE)
                videoImgProcOutput = videoImgProc.communicate()
        
                #check stderr for errors
                if len(videoImgProcOutput[1]) > 0:
                        print 'ERROR: '
                        print videoImgProcOutput[1]
        
        # use ImageMagick to overlay "images/" + ffmpegResults[3] + ".png" onto thumbName in bottom right corner
        audioOverlayFilename = os.path.join(sys.path[0], 'EyetvTOG/images', ffmpegResults[3] + '.png')
        if not os.path.isfile(audioOverlayFilename):
                print "WARN: Couldn't find "+audioOverlayFilename+" skipping audio overlay"
        else:
                audioImgProcCmd = (os.path.join(IMAGEMAGICK_PATH, IMAGEMAGICK_COMPOSITE_PROCESS), '-compose', 'atop', '-geometry', '1000x' + str(int(thumbSize[1]*IMG_HEIGHT)) + '+' + str(int(thumbSize[0]-thumbSize[1]*(IMG_HEIGHT/LOGO_RATIO)-thumbSize[0]*IMG_MARGIN)) + '+' + str(int(thumbSize[1]*(1.0-IMG_HEIGHT)-thumbSize[0]*IMG_MARGIN)), audioOverlayFilename, thumbName, thumbName)
                audioImgProc = subprocess.Popen(audioImgProcCmd, stderr=subprocess.PIPE)
                audioImgProcOutput = audioImgProc.communicate()
        
                # check stderr for errors
                if len(audioImgProcOutput[1]) > 0:
                        print 'ERROR: '
                        print audioImgProcOutput[1]

        return SUCCESS

    
    def revertFile (filename):
        thumbName = changeExtension(filename, "tbn")
        thumbOrigName = changeExtension(filename, "tbn-orig")
                
        # if they have tbn-orig then I restore for them
        if os.path.isfile(thumbOrigName):
                shutil.copyfile(thumbOrigName, thumbName)
                os.remove(thumbOrigName)
                return SUCCESS

        # if they have only a tbn there's nothing I can do
        elif os.path.isfile(thumbName):
                print "WARN: no tbn-orig file for "+filename+" unable to revert"
                return FAILURE

        # no thumb files means nothing I can do
        else:
                print "WARN: no thumbnail for"+filename
                return SKIPPED
 
    def changeExtension (filename, newExtension):
        "Replaces filename's extension with newExtension"

        stubName = filename[:filename.rfind(".")+1]

        return stubName + newExtension
    
    def getffmpegInfo (filename):
        ffmpegProcCmd = (os.path.join(FFMPEG_PATH, FFMPEG_PROCESS), '-i', filename)

        if DEBUG:
                print 'DEBUG: Command string:', ffmpegProcCmd
        ffmpegProc = subprocess.Popen(ffmpegProcCmd, stderr=subprocess.PIPE)

        output = ffmpegProc.communicate()[1].split('\n')

        if DEBUG:
                print "DEBUG: ffmpeg output:", output

        return output
    
    def parseffmpegInfo (output):
        streamRegex = re.compile("\s+Stream #0\.(\d)(\[\w+\])?.*?: (Video|Audio): (.+)")

        videoCodec = None
        videoResolution = None
        audioCodec = None
        audioChannels = None
        
        for line in output:

                if DEBUG:
                        print "PARSING:"+line

                streamResult = streamRegex.match(line)

                if streamResult != None:

                        params = streamResult.group(4).split(", ")

                        if streamResult.group(3) == "Video" and videoCodec == None and videoResolution == None:
                                if len(params) < 3:
                                    continue
                                print "PARSING: Found video line containing "+params[0]+" and "+params[2]
                                videoCodec = params[0]
                                videoResolution = params[2]
                        elif streamResult.group(3) == "Audio" and audioCodec == None and audioChannels == None:
                                print "PARSING: Found audio line containing "+params[0]+" and "+params[2]
                                audioCodec = params[0]
                                audioChannels = params[2]

                elif DEBUG:
                        print "PARSING: Line didn't match known results format."

        if (videoCodec == None or videoResolution == None) and (audioCodec == None or audioChannels == None):
                return None
                                
        return [videoCodec, parseVideoResolution(videoResolution), parseAudioCodec(audioCodec), parseAudioChannels(audioChannels)]
    
    def parseAudioCodec (codec):
        if codec == "0x0000":
                return "AC3"
        elif codec == "mp3":
                return "MP3"
        elif codec == "dca":
                return "DTS"
        else:
                return "??"
    
    def parseAudioChannels (channels):
        if channels == "5:1":
                return "5.1"
        elif channels == "7:1":
                return "7.1"
        else:
                return channels
    
    def parseVideoResolution (resolution):
        if DEBUG:
                print 'DEBUG: Parsing resolution to tuple:'+resolution

        width = int(resolution.split("x")[0])
        
        if width < 1280:
                return "SD"
        elif 1280 <= width < 1920:
                return "720p"
        elif width >= 1920:
                return "1080p"
        else:
                return "??"
    
    def scanAllFiles (file):
        i = 0
        good = 0
        bad = 0
        skipped = 0

        # for file in files:
        
                # if it's a folder, scan it automatically for all applicable files (recursive)
                #if os.path.isdir(file):
                #
                #        results = scanAllFiles (filter(lambda x: x.endswith(AUTOSCAN_EXTENSIONS) or os.path.isdir(x), [os.path.join(file, x) for x in os.listdir(file)]))
                #        good += results[0]
                #        bad += results[1]
                #        skipped += results[2]
                #
                #else:

        i += 1
        # print "PDEBUG- file-"+file
        result = doFile(file)
        if result == SUCCESS:
                good += 1
        elif result == SKIPPED:
                skipped += 1
        else:
                bad += 1

        return (good, bad, skipped)
     
    def revertAllFiles (files):
        good = 0
        bad = 0
        skipped = 0

        for file in files:
                # if it's a folder, scan it automatically for all mkv and avi files (recursive)
                if os.path.isdir(file):
                        results = revertAllFiles (filter(lambda x: x.endswith(AUTOSCAN_EXTENSIONS) or os.path.isdir(x), [os.path.join(file, x) for x in os.listdir(file)]))
                        good += results[0]
                        bad += results[1]
                        skipped += results[2]

                else:
                        result = revertFile(file);
                        if result == SUCCESS:
                                good += 1
                        elif result == SKIPPED:
                                skipped += 1
                        else:
                                bad += 1
        
        return (good, bad, skipped)
                    
    def getSyntax (name):
       return 'Syntax: python ' + name + ' <-scan|-revert> [file/folder list]\n\tpython ' + name + ' -force <1080p|720p|SD> <7.1|5.1|stereo|mono> <filename>'
    
    # main TOG function
    
    checkDependencies()
    
    if len(sys.argv) == 1:
            print getSyntax(sys.argv[0])
    elif sys.argv[1] == '-revert' and len(sys.argv) >= 3:
            results = revertAllFiles(sys.argv[2:])
            print 'Successfully reverted overlays on'+results[0]+'of'+results[0]+results[1]+results[2]+'thumbnails (' + str(results[1]) + ' failures)'
    # this is the only option used in this context
    elif cmd == '-scan':
            results = scanAllFiles(scandir)
            print 'Successfully created overlays on '+str(results[0])+' of 1 thumbnails (' + str(results[1]) + ' failures)'
    elif sys.argv[1] == '-force' and len(sys.argv) == 5:
            doFile(sys.argv[4], ('', sys.argv[2], '', sys.argv[3]))
    else:
            print getSyntax(sys.argv[0])
# EOT

# check eyetv dir
for dirpath, dirnames, filenames in os.walk(path):
    # ignore eyetvsched files
    if dirpath.endswith(".eyetv"):
        # ignore eyetv buffer (for now)
        if not dirpath.endswith("Live TV Buffer.eyetv"):
            # print 'Directory', dirpath
            for filename in filenames:
                if filename.endswith(".mpg"):
                    fqname=dirpath+'/'+filename
                    fqname = unicode(fqname, "utf-8" )
                    # print fqname
                    p=re.compile('.+/(.+).eyetv')
                    m=p.match(dirpath)
                    shortdirpath=m.group(1)
                    shortdirpath = unicode( shortdirpath, "utf-8" )
                    # match icon name
                    p=re.compile('(.+)\.mpg')
                    m=p.match(fqname)
                    tbn=m.group(1)
                    tifftbn=tbn+'.tiff'
                    # detect tbn /integrate with tog
                    tbn=tbn+'.tbn'
                    if os.path.isfile(tifftbn) and not os.path.isfile(tbn):
                        # convert Unicode string to regular string
                        togname = str(fqname)
                        togname = togname.replace("'", "\'")
                        if tog == 1:
                            try:
                                go_tog('-scan', togname)
                            except:
                                print "Failed to set thumbnail overlay for:"+togname
                                pass
                        # if TOG fails fallback to tiff tbns
                        if os.path.isfile(tifftbn) and not os.path.isfile(tbn):
                            tbn = tifftbn
                    statinfo = os.stat(fqname)
                    size = statinfo.st_size
                    filedate = statinfo.st_ctime
                    objdate=datetime.fromtimestamp(filedate)
                    date=objdate.strftime("%d/%m/%Y")
                    # %H:%M:%S")
                    # print size, date
                    # open Eyetv program info xml file
                    fObj=dirpath+'/*.eyetvp'
                    filePl=unicode((str(glob.glob(fObj))), "utf-8" )
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
                        actors=""
                        genre=""
                        director=""
                        aired=""
                        
                        file = open(filePl)
                        pl=""
                        for line in file:
                            line = line.replace("\n", "")
                            line = line.replace("\t", "")
                            line = line.replace("'", "\'")
                            pl = pl + line
                        file.close()
                        epg=unicode(pl, "utf-8" )                       
                        p=re.compile('<key>TITLE</key><string>(.*?)</string>')
                        m=p.search(epg)
                        if m:
                            title=m.group(1)
                            title = title.strip()
                        p=re.compile('<key>SUBTITLE</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            subtitle=m.group(1)
                            subtitle = subtitle.strip()
                            if subtitle:
                                dsubtitle='.'+subtitle
                        # print subtitle
                        p=re.compile('<key>EPISODENUM</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            episode=m.group(1)
                            episode = episode.strip()
                            if episode:
                                depisode='.'+episode
                        # print episode
                        p=re.compile('<key>DESCRIPTION</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            plot=m.group(1)
                            plot = plot.strip()
                        # print plot
                        libname=title+depisode+dsubtitle
                        # print libname
                        
                        p=re.compile('<key>ACTORS</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            actors=m.group(1)
                            actors = actors.strip()
                        p=re.compile('<key>CONTENT</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            genre=m.group(1)
                            genre = genre.strip()
                        p=re.compile('<key>DIRECTOR</key><string>(.*?)</string>')                        
                        m=p.search(epg)
                        if m:
                            director=m.group(1)
                            director = director.strip()
                        p=re.compile('<date>(\d\d\d\d-\d\d-\d\d).*?\d\d:\d\d:\d\d.*?</date>')                        
                        m=p.search(epg)
                        if m:
                            aired=m.group(1)
                            aired = aired.strip()
                        
                        # linked directory support
                        if LDS == 1:    
                            # build dummy dir
                            if not os.path.isdir(dummy):
                                os.mkdir(dummy)
                            dummyShowName = dummy+'/'+title
                            if not os.path.isdir(dummyShowName):
                                os.mkdir(dummyShowName)
                             
                            scrapethetvdb = STVDB
                            done = 0
                            if DEBUG:
                                print 'processing - '+title+'-'+subtitle
                             
                            # .nfo file support
                            if nfo == 1:
                                # thetvdb.com scraper support
                                while scrapethetvdb == 1 and done == 0:
                                    import urllib,urllib2
                                    # scrape thetvdb.com
                                    # load search results
                                    UEtitle = urllib.quote_plus(title, safe='/')
                                    Base_URL = "http://www.thetvdb.com/index.php?seriesname="+UEtitle+"&fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&searching=Search&tab=advancedsearch"
                                    WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                    WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                    WebSock.close()                     # Closes connection to url
                                    
                                    # parse series search results page
                                    seriesLink = re.compile('<tr><td class="odd">1</td><td class="odd"><a href="(/index.php\?tab=series&amp;id=\d+&amp;lid=\d)">', re.IGNORECASE).findall(WebHTML)
                                    
                                    if len(seriesLink) == 0:
                                        if DEBUG:
                                            print 'seriesLink not match -'+title+'-'+subtitle
                                        scrapethetvdb = 0
                                        break
                                    
                                    # ...
                                    # load series page
                                    Base_URL = "http://www.thetvdb.com"+urllib.unquote(seriesLink[0])
                                    Base_URL = Base_URL.replace('&amp;', '&')
                                    if DEBUG:
                                        print 'Base_URL-'+Base_URL
                                    
                                    WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                    WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                    WebSock.close()                     # Closes connection to url
                                    # ...
                                    
                                    # parse series page
                                    m = re.compile('<a href="(/\?tab=seasonall&id=\d+&amp;lid=\d)" class="seasonlink">All</a>', re.IGNORECASE).findall(WebHTML)
                                    if len(m) == 0:
                                        if DEBUG:
                                            print 'episodesLink not matched -'+title+'-'+subtitle
                                        scrapethtvdb = 0
                                        break
                                    episodesLink = str(m[0])
                                    episodesLink = episodesLink.replace('&amp;', '&')
                                    episodesLink = 'http://www.thetvdb.com'+episodesLink
                                    if DEBUG:
                                        print 'episodesLink-'+episodesLink
                                    m = re.compile('<!-- Right upper -->\s+<td>\s+<div id="content">\s+<h1>.+</h1>\s*(.+)\s*', re.IGNORECASE).findall(WebHTML)
                                    if len(m) == 0:
                                        if DEBUG:
                                            print 'thetvdbPlot not matched'
                                        scrapethtvdb = 0
                                        break
                                    thetvdbPlot = str(m[0])
                                    if DEBUG:
                                        print 'thetvdbPlot-'+thetvdbPlot
                                    pSID = re.compile('/\?tab=seasonall&id=(\d+)&lid=\d')
                                    mSID = pSID.search(episodesLink)
                                    if mSID:
                                        SID=mSID.group(1)
                                    else:
                                        if DEBUG:
                                            print 'ShowID not matched -'+title+'-'+subtitle
                                        scrapethtvdb = 0
                                        break
                                    
                                    if DEBUG:
                                        print 'SID-'+SID
                                    
                                    actorsLink = 'http://www.thetvdb.com/?tab=actors&id='+SID
                                    if DEBUG:
                                        print 'actorsLink-'+actorsLink
                                    #bannersLink = 'http://www.thetvdb.com/?tab=seriesbanners&id='+SID
                                    #fanartLink =  'http://www.thetvdb.com/?tab=seriesfanart&id='+SID
                                    thetvdbBanners = re.compile('<img src="(.*)" class="banner" border="0"></a>', re.IGNORECASE).findall(WebHTML)
                                    if DEBUG:
                                        print 'thetvdbBanners[0]-'+thetvdbBanners[0]
                                    firstBanner = 'http://www.thetvdb.com'+thetvdbBanners[0]
                                    thetvdbFanart = re.compile('<div id="fanart" style="background-image: url\((.*)\)">', re.IGNORECASE).findall(WebHTML)
                                    if DEBUG:
                                        print 'thetvdbFanart[0]-'+thetvdbFanart[0]
                                    firstFanart = 'http://www.thetvdb.com'+thetvdbFanart[0]
                                    # ...
                                    # load actors page
                                    Base_URL = actorsLink
                                    WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                    WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                    WebSock.close()                     # Closes connection to url
                                    # ...
                                    # parse actors page
                                    actorLists= re.compile('<table cellspacing="0" cellpadding="0" border="0" width="100%" class="infotable"><tr><td>\s+<img src="(.*)" class="banner" border="0" alt=".*">\s+<h2><a href="http://www.imdb.com/find\?s=nm&q=.*" target="_blank">(.*)</a></h2>(?:as )*(.*)(?:<br>)*').findall(WebHTML)
                                    
                                    #if DEBUG:
                                    #    print 'actorLists - '+str(actorLists)
                                    
                                    thetvdbActorThumbs = []
                                    thetvdbActors = []
                                    thetvdbActorRoles = []
                                    v=0
                                    if len(actorLists) == 0:
                                        print "Actors did not match"
                                        scrapethtvdb = 0
                                        break
                                    while v < len(actorLists):
                                        record = actorLists[v]
                                        #if DEBUG:
                                        #    print 'record - '+str(record)
                                        thetvdbActorThumbs.append(record[0])
                                        thetvdbActors.append(record[1])
                                        thetvdbActorRoles.append(record[2])
                                        v=v+1
                                    
                                    #if DEBUG:
                                    #    print "thetvdbActorThumbs - "+str(thetvdbActorThumbs)
                                    #    print "thetvdbActors - "+str(thetvdbActors)
                                    #    print "thetvdbActorRoles - "+str(thetvdbActorRoles)
                                    
                                    # ...
                                    # load banners page
                                    #Base_URL = bannersLink
                                    #WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                    #WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                    #WebSock.close()                     # Closes connection to url
                                    ## ...
                                    ## parse banners page
                                    #thetvdbBanners = re.compile('<img src="(.*)" class="banner" border="0"></a>', re.IGNORECASE).findall(WebHTML)
                                    # ...
                                    # load fanart page
                                    #Base_URL = fanartLink
                                    #WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                    #WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                    #WebSock.close()                     # Closes connection to url
                                    ## ...
                                    ## parse fanart page
                                    #thetvdbFanarts = re.compile('<img src="(.*)" class="banner" border="0"></a>', re.IGNORECASE).findall(WebHTML)
                                    # ...
                                    # load episodes page
                                    Base_URL = episodesLink
                                    WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                    WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                    WebSock.close()                     # Closes connection to url
                                    # ...
                                    
                                    # parse episodes page
                                    def fuzzy_substring(needle, haystack):
                                        """Calculates the fuzzy match of needle in haystack,
                                        using a modified version of the Levenshtein distance
                                        algorithm.
                                        The function is modified from the levenshtein function
                                        in the bktree module by Adam Hupp"""
                                        m, n = len(needle), len(haystack)
                                        # base cases
                                        if m == 1:
                                            return not needle in haystack
                                        if not n:
                                            return m
                                        row1 = [0] * (n+1)
                                        for i in range(0,m):
                                            row2 = [i+1]
                                            for j in range(0,n):
                                                cost = ( needle[i] != haystack[j] )
                                                row2.append( min(row1[j+1]+1, # deletion
                                                                   row2[j]+1, #insertion
                                                                   row1[j]+cost) #substitution
                                                               )
                                            row1 = row2
                                        return min(row1)
                                    
                                    episodeList = re.compile('<tr><td class="(?:even|odd)+"><a href="/\?tab=episode&seriesid=\d+&seasonid=\d*&id=\d*&amp;lid=\d">(\d*)(?: - )*(\d*)</a></td><td class="(?:even|odd)+"><a href="/\?tab=episode&seriesid=\d+&seasonid=(\d*)&id=(\d*)&amp;lid=\d">(.+)</a></td>').findall(WebHTML)
                                    candidateSeasons = []
                                    candidateEpisodes = []
                                    candidateSeasonID = []
                                    candidateSpecificEpisodeID = []
                                    specificEpisodeCandidates = []
                                    v=0
                                    if len(episodeList) == 0:
                                        print 'Empty episodeList'
                                        scrapethtvdb = 0
                                        break
                                    while v < len(episodeList):
                                        record = episodeList[v]
                                        #if DEBUG:
                                        #    print 'record - '+str(record)
                                        candidateSeasons.append(record[0])
                                        candidateEpisodes.append(record[1])
                                        candidateSeasonID.append(record[2])
                                        candidateSpecificEpisodeID.append(record[3])
                                        specificEpisodeCandidates.append(record[4])
                                        v=v+1
                                    
                                    # for specificEpisodeCandidate in specificEpisodeCandidates:
                                    i=0
                                    candidateScore = []
                                    while i < len(specificEpisodeCandidates):
                                        specificEpisodeCandidate = specificEpisodeCandidates[i]
                                        # attempt fuzzy match
                                        candidateScore.append(fuzzy_substring(subtitle, specificEpisodeCandidate))
                                        i=i+1
                                    # grab best match
                                    bestMatch = min(candidateScore)
                                    if DEBUG:
                                        print 'bestMatch-'+str(bestMatch)
                                    BMI = candidateScore.index(bestMatch)
                                    if DEBUG:
                                        print 'BMI-'+str(BMI)
                                    if bestMatch > 11:
                                        if DEBUG:
                                            print 'no specific episode found for:'+title+'-'+subtitle
                                        scrapethetvdb = 0
                                        break
                                    else:
                                        SSID = candidateSeasonID[BMI]
                                        SEID = candidateSpecificEpisodeID[BMI]
                                        SpecificEpisodeLink = 'http://www.thetvdb.com/?tab=episode&seriesid='+SID+'&seasonid='+SSID+'&id='+SEID+'&lid=7'
                                        if DEBUG:
                                            print 'SpecificEpisodeLink - '+str(SpecificEpisodeLink)
                                        # ...
                                        # load specific episode page
                                        Base_URL = SpecificEpisodeLink
                                        WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                        WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                        WebSock.close()                     # Closes connection to url
                                        # ...
                                        # parse specific episode page
                                        scrapermatch = re.compile('<input type="text" name="EpisodeName_\d+" value="(.*)" style="display: inline" >', re.IGNORECASE).findall(WebHTML)
                                        if len(scrapermatch) == 0:
                                            print 'Empty scrapersubtitle'
                                            scrapersubtitle = ''
                                        else:
                                            scrapersubtitle = scrapermatch[0]
                                            if DEBUG:
                                                print 'scrapersubtitle - '+str(scrapersubtitle)
                                        scraperseason = candidateSeasons[BMI]
                                        if DEBUG:
                                            print 'scraperseason - '+str(scraperseason)
                                        scrapermatch = re.compile('<td><input type="text" name="EpisodeNumber" value="(.*)" maxlength="45"></td>', re.IGNORECASE).findall(WebHTML)
                                        if len(scrapermatch) == 0:
                                            print 'Empty scraperepisode'
                                            scraperepisode = ''
                                        else:
                                            scraperepisode = scrapermatch[0]
                                            if DEBUG:
                                                print 'scraperepisode - '+str(scraperepisode)
                                        scrapermatch = re.compile('<textarea rows="\d+" cols="\d+" name="Overview_\d+" style="display: inline">(.*)</textarea>', re.IGNORECASE).findall(WebHTML)
                                        if len(scrapermatch) == 0:
                                            print 'Empty scraperplot'
                                            scraperplot = ''
                                        else:
                                            scraperplot = scrapermatch[0]
                                            if DEBUG:
                                                print 'scraperplot - '+str(scraperplot)
                                        scrapermatch = re.compile('<td><input name="Director" value="(.*)" maxlength="255" type="text"></td>', re.IGNORECASE).findall(WebHTML)
                                        if len(scrapermatch) == 0:
                                            print 'Empty scraperdirector'
                                            scraperdirector = ''
                                        else:
                                            scraperdirector = scrapermatch[0]
                                            if DEBUG:
                                                print 'scraperdirector - '+str(scraperdirector)
                                        scrapermatch = re.compile('<td><input name="FirstAired" value="(.*)" maxlength="255" type="text"></td>', re.IGNORECASE).findall(WebHTML)
                                        if len(scrapermatch) == 0:
                                            print 'Empty scraperaired'
                                            scraperaired = ''
                                        else:
                                            scraperaired = scrapermatch[0]
                                            if DEBUG:
                                                print 'scraperaired - '+str(scraperaired)
                                        scrapername = title+'.S'+scraperseason+'E'+scraperepisode+'.'+scrapersubtitle
                                        if DEBUG:
                                            print 'scrapername - '+str(scrapername)
                                        # ...
                                    # use thetvdb.com data for show nfo
                                    # test for existing  tvshow.nfo
                                    shownfo=dummyShowName+'/tvshow.nfo'
                                    if not os.path.isfile(shownfo):
                                        if DEBUG:
                                            print 'using thetvdb.com data for show nfo - '+title
                                        # write tvshow.nfo (Series Info)
                                        shownfofile=open(shownfo, 'w')
                                        shownfofile.write('<tvshow>\n')
                                        shownfofile.write(' <title>'+title+'</title>\n')
                                        shownfofile.write(' <season>-1</season>\n')
                                        shownfofile.write(' <episode>0</episode>\n')
                                        shownfofile.write(' <displayseason>-1</displayseason>\n')
                                        shownfofile.write(' <displayepisode>-1</displayepisode>\n')
                                        if not genre == '':
                                            shownfofile.write(' <genre>'+genre+'</genre>\n')
                                        if not thetvdbPlot == '':
                                            shownfofile.write(' <plot>'+thetvdbPlot+'</plot>\n')
                                        if not thetvdbActors == '':
                                            j=0
                                            #for actor in thetvdbActors:
                                            y=len(thetvdbActors)
                                            while j<y:
                                                actor = thetvdbActors[j]
                                                if not actor == '':
                                                    shownfofile.write('  <actor>\n')
                                                    shownfofile.write('      <name>'+actor+'</name>\n')
                                                    if not thetvdbActorRoles[j] == '':
                                                        thetvdbActorRole = thetvdbActorRoles[j]
                                                        if not thetvdbActorRole == '':
                                                            shownfofile.write('      <role>'+thetvdbActorRole+'</role>\n')
                                                    if not thetvdbActorThumbs[j] == '':
                                                        thetvdbActorThumb = thetvdbActorThumbs[j]
                                                        if not thetvdbActorThumb == '':
                                                            if not thetvdbActorThumb == '/banners/actors/0.jpg':
                                                                thetvdbActorThumb = 'http://www.thetvdb.com'+thetvdbActorThumb
                                                                shownfofile.write('      <thumb>'+thetvdbActorThumb+'</thumb>\n')
                                                    shownfofile.write('  </actor>\n')
                                                j=j+1
                                        shownfofile.write('</tvshow>\n')
                                        shownfofile.close()
                                        
                                        # banners and fanart
                                        if DEBUG:
                                            print 'firstBanner - '+firstBanner
                                        Base_URL = firstBanner
                                        WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                        WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                        WebSock.close()                     # Closes connection to url
                                        if not WebHTML == '':
                                            showBanner=dummyShowName+'/folder.jpg'
                                            if not os.path.isfile(showBanner):
                                                showBannerFile=open(showBanner, 'w')
                                                showBannerFile.write(WebHTML)
                                                showBannerFile.close()
                                        if DEBUG:
                                            print 'firstFanart - '+firstFanart
                                        if not firstFanart == 'http://www.thetvdb.com/banners/actors/0.jpg' or firstFanart == 'http://www.thetvdb.com':
                                            Base_URL = firstFanart
                                            WebSock = urllib.urlopen(Base_URL)  # Opens a 'Socket' to URL
                                            WebHTML = WebSock.read()            # Reads Contents of URL and saves to Variable
                                            WebSock.close()                     # Closes connection to url
                                            if not WebHTML == '':
                                                showFanart=dummyShowName+'/fanart.jpg'
                                                if not os.path.isfile(showFanart):
                                                    showFanartFile=open(showFanart, 'w')
                                                    showFanartFile.write(WebHTML)
                                                    showFanartFile.close()
                                    done = 1
                                # else:
                                if not done == 1:
                                    # use Eyetv EPG data for show nfo
                                    # test for existing  tvshow.nfo
                                    shownfo=dummyShowName+'/tvshow.nfo'
                                    if not os.path.isfile(shownfo):
                                        if DEBUG:
                                            print 'using Eyetv.com data for show nfo - '+title
                                        # write tvshow.nfo (Series Info)
                                        shownfofile=open(shownfo, 'w')
                                        shownfofile.write('<tvshow>\n')
                                        shownfofile.write(' <title>'+title+'</title>\n')
                                        shownfofile.write(' <season>-1</season>\n')
                                        shownfofile.write(' <episode>0</episode>\n')
                                        shownfofile.write(' <displayseason>-1</displayseason>\n')
                                        shownfofile.write(' <displayepisode>-1</displayepisode>\n')
                                        if not genre == '':
                                            shownfofile.write(' <genre>'+genre+'</genre>\n')
                                        if not actors == '':
                                            for actor in actors.split(', '):
                                                if not actor == '':
                                                    shownfofile.write('  <actor>\n')
                                                    shownfofile.write('      <name>'+actor+'</name>\n')
                                                    shownfofile.write('  </actor>\n')
                                        shownfofile.write('</tvshow>\n')
                                        shownfofile.close()
                            
                            if scrapethetvdb == 1 and done == 1:
                                # create symbolic links from thetvdb.com
                                dummyShowLink = dummyShowName+'/'+scrapername+'.mpg'
                                if not os.path.islink(dummyShowLink):
                                    os.symlink(fqname, dummyShowLink)
                                dummyShowThumb = dummyShowName+'/'+scrapername+'.tbn'
                                if not os.path.islink(dummyShowThumb):
                                    os.symlink(tbn, dummyShowThumb)
                            else:
                                # create symbolic links from Eyetv EPG data
                                dummyShowLink = dummyShowName+'/'+libname+'.mpg'
                                if not os.path.islink(dummyShowLink):
                                    os.symlink(fqname, dummyShowLink)
                                dummyShowThumb = dummyShowName+'/'+libname+'.tbn'
                                if not os.path.islink(dummyShowThumb):
                                    os.symlink(tbn, dummyShowThumb)
                                
                            # .nfo file support
                            if nfo == 1:
                                if scrapethetvdb == 1 and done == 1:
                                    # use thetvdb.com data for episode nfo
                                    episodenfo = dummyShowName+'/'+scrapername+'.nfo'
                                    # test for existing  filename.nfo
                                    if not os.path.isfile(episodenfo):
                                        if DEBUG:
                                            print 'using thetvdb.com data for episode nfo - '+title+'-'+subtitle
                                        episodenfofile=open(episodenfo, 'w')
                                        episodenfofile.write('<episodedetails>\n')
                                        episodenfofile.write('  <title>'+scrapersubtitle+'</title>\n')
                                        episodenfofile.write('  <season>'+scraperseason+'</season>\n')
                                        episodenfofile.write('  <episode>'+scraperepisode+'</episode>\n')
                                        episodenfofile.write('  <plot>'+scraperplot+'</plot>\n')
                                        if not scraperdirector == '':
                                            episodenfofile.write('  <director>'+scraperdirector+'</director>\n')
                                        if not scraperaired == '':
                                            episodenfofile.write('  <aired>'+scraperaired+'</aired>\n')
                                        if not thetvdbActors == '':
                                            j=0
                                            #for actor in thetvdbActors:
                                            y=len(thetvdbActors)
                                            while j<y:
                                                actor = thetvdbActors[j]
                                                if not actor == '':
                                                    episodenfofile.write('  <actor>\n')
                                                    episodenfofile.write('      <name>'+actor+'</name>\n')
                                                    if not thetvdbActorRoles[j] == '':
                                                        thetvdbActorRole = thetvdbActorRoles[j]
                                                        if not thetvdbActorRole == '':
                                                            episodenfofile.write('      <role>'+thetvdbActorRole+'</role>\n')
                                                    if not thetvdbActorThumbs[j] == '':
                                                        thetvdbActorThumb = thetvdbActorThumbs[j]
                                                        if not thetvdbActorThumb == '':
                                                            if not thetvdbActorThumb == '/banners/actors/0.jpg':
                                                                thetvdbActorThumb = 'http://www.thetvdb.com'+thetvdbActorThumb
                                                                episodenfofile.write('      <thumb>'+thetvdbActorThumb+'</thumb>\n')
                                                    episodenfofile.write('  </actor>\n')
                                                j=j+1
                                        episodenfofile.write('</episodedetails>\n')
                                        episodenfofile.close()
                                       
                                if not done == 1:
                                    # use Eyetv EPG data for episode nfo
                                    episodenfo = dummyShowName+'/'+libname+'.nfo'
                                    # test for existing  filename.nfo
                                    if not os.path.isfile(episodenfo):
                                        if DEBUG:
                                            print 'using Eyetv data for episode nfo - '+title+'-'+subtitle
                                        episodenfofile=open(episodenfo, 'w')
                                        episodenfofile.write('<episodedetails>\n')
                                        episodenfofile.write('  <title>'+subtitle+'</title>\n')
                                        episodenfofile.write('  <episode>'+episode+'</episode>\n')
                                        episodenfofile.write('  <plot>'+plot+'</plot>\n')
                                        if not director == '':
                                            episodenfofile.write('  <director>'+director+'</director>\n')
                                        if not aired == '':
                                            episodenfofile.write('  <aired>'+aired+'</aired>\n')
                                        if not actors == '':
                                            for actor in actors.split(', '):
                                                if not actor == '':
                                                    episodenfofile.write('  <actor>\n')
                                                    episodenfofile.write('      <name>'+actor+'</name>\n')
                                                    episodenfofile.write('  </actor>\n')
                                        episodenfofile.write('</episodedetails>\n')
                                        episodenfofile.close()
                                    
                    filePl=""
                    #icon = "defaultVideo.png"
                    #icon2 = "defaultVideoBig.png"
                    icon = tbn
                    icon2 = tbn
                    # title=shortdirpath
                    liz=xbmcgui.ListItem(shortdirpath, libname, iconImage=icon, thumbnailImage=icon2)
                    # liz.setInfo( type="Video", infoLabels={ "Title": libname, "Date":date, "Size":size, "Plot":plot, "Episode":episode} )
                    liz.setInfo( type="Video", infoLabels={ "Title": libname, "Date":date, "Size":size, "Plot":plot, "Genre":genre, "Cast":actors} )
                    if LDS == 1:
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=dummyShowLink,listitem=liz)
                    else:
                        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=fqname,listitem=liz)

#xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
#xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
#xbmcplugin.addSortMethod(int(sys.argv[1]),  3)#date
#xbmcplugin.addSortMethod(int(sys.argv[1]), 10)#title
#xbmcplugin.addSortMethod(int(sys.argv[1]),  1)#filename
xbmcplugin.endOfDirectory(int(sys.argv[1]))
