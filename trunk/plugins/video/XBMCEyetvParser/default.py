#!/usr/bin/env python

# XBMCEyetvParser
# version 1.40
# by prophead
# ThumbnailOverlayGenerator by Nic Wolfe (midgetspy)

# user variables, these are overidden by the gui settings
# ---------------
# my default path
path = '/Volumes/RAID/Movies/EyeTV/EyeTV Archive'

# TOG
# requires Imagemagick, and ffmpeg
# 0=no thumbail overlays, 1=try thumbnail overlays
tog = 0
# ---------------

# import modules
import os, re, glob, sys, shutil
import xbmc,xbmcgui,xbmcplugin
from datetime import datetime

# set settings (Eyetv folder) from the XBMC interface
def get_settings():
    settings = {}
    try:        
            settings['path'] =  xbmcplugin.getSetting( 'path' )
            settings['EyetvTOG'] = xbmcplugin.getSetting( 'EyetvTOG' )
            return settings
    except:
            print "couldn't load settings"
            pass
## test for Boxee
#BoxeePath = os.getcwd()[:-1]+"/"
#p=re.compile('.+(oxee).+')
#m=p.match(BoxeePath)
#if not m:

# get settings from gui settings
settings=get_settings()
path=settings['path']
tog=settings['EyetvTOG']
if tog == "true":
    tog = 1

#else:
#    print "[XBMCEyetvParser] - Boxee"
    
def go_tog(cmd, scandir):
    #  TOG
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
    # 1=Extended output in log
    DEBUG = 0
    
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
                        togname = fqname.encode( 'utf-8' )
                        togname = togname.replace("'", "\'")
                        if tog == 1:
                            try:
                                go_tog('-scan', togname)
                            except:
                                print "Failed to set thumbnail overlay for:"+togname
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
                    for file in os.listdir(dirpath):
                        if( re.search('.eyetvp$', file)):
                            filePl = dirpath+"/"+file
                    # print filePl+" - "+str(type(filePl))

                    # filePl = filePl.replace("\"", "")
                    # filePl = filePl.strip('[')
                    # filePl = filePl.strip(']')
                    # filePl = filePl.strip('\'')

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
                        actorlist=[]

                        file = open(filePl)
                        pl=""
                        for line in file:
                            line = line.replace("\n", "")
                            line = line.replace("\t", "")
                            pl = pl + line
                        # epg=str(pl)
                        epg = unicode( pl, "utf-8" )
                        # print epg
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
                        # libname = unicode( libname, "utf-8" )
                        libname = libname.encode( 'utf-8' )
                        p=re.compile('<key>ACTORS</key><string>(.*?)</string>')
                        m=p.search(epg)
                        if m:
                            actors=m.group(1)
                            actors = actors.strip()
                            actorlist = actors.split(', ')
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
                    filePl=""
                    #icon = "defaultVideo.png"
                    #icon2 = "defaultVideoBig.png"
                    #icon = tbn.decode( 'utf8', 'backslashreplace')
                    #icon = tbn.encode( 'utf8' )
                    #icon = icon.replace("'", "\'")
                    
                    # ugly hack to get XBMC to work with utf-8 thumbnails
                    tbn = tbn.encode( 'utf8' )
                    tbn = tbn.replace("'", "\'")
                    p=re.compile('.+/(.+)\.(tbn|tiff)')
                    m=p.match(tbn)
                    shorticonname=m.group(1)
                    newpath=path+'../thumbnails/'
                    if not os.path.isdir(newpath):
                        os.mkdir(newpath)
                    newicon = newpath+shorticonname+'.tbn'
                    # print 'newicon='+newicon
                    # cp tbn newicon
                    if not os.path.isfile(newicon):
                        shutil.copyfile(tbn, newicon)
                    icon=newicon

                    icon2 = icon

                    # title=shortdirpath
                    liz=xbmcgui.ListItem(shortdirpath, libname, iconImage=icon, thumbnailImage=icon2)
                    # liz.setInfo( type="Video", infoLabels={ "Title": libname, "Date":date, "Size":size, "Plot":plot, "Episode":episode} )
                    liz.setInfo( type="Video", infoLabels={ "Title": libname, "Date":date, "Size":size, "Plot":plot, "Genre":genre, "Cast":actorlist} )
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=fqname,listitem=liz)

#xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')                   
#xbmcplugin.addSortMethod(int(sys.argv[1]), 3)#date
#xbmcplugin.addSortMethod(int(sys.argv[1]), 10)#title
#xbmcplugin.addSortMethod(int(sys.argv[1]),  1)#filename
xbmcplugin.endOfDirectory(int(sys.argv[1]))
