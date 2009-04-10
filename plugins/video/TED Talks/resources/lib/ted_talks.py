"""
    TED Talks
"""
#main imports
import xbmc,xbmcgui,xbmcplugin
import urllib,urllib2,re,sys,os
import feedparser

class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )
        
class Main:

    #MAIN URLS
    themes='http://www.ted.com/index.php/themes/atoz'
    hdFeed='http://feeds.feedburner.com/TedtalksHD'
    sdFeed='http://feeds.feedburner.com/tedtalks_video'
    auFeed='http://feeds.feedburner.com/tedtalks_audio'

    def __init__(self):
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        self._parse_argv()
        self._get_settings()
    ####
        if self.args.mode==None:
            self.showCategories()
            xbmcplugin.addSortMethod(int(sys.argv[1]), 16)#sort by date
        elif self.args.mode=='1':
            #List All
            xbmcplugin.addSortMethod(int(sys.argv[1]), 16)#sort by date
            xbmcplugin.addSortMethod(int(sys.argv[1]), 20)#sort by episode
            t=self.listMedia(self.args.url,self.args.mode)
        elif self.args.mode=='2':
            #List Themes
            self.listThemes()
        elif self.args.mode=='3':
            self.listThemeTalks()
            xbmcplugin.addSortMethod(int(sys.argv[1]), 20)#sort by episode
            xbmcplugin.addSortMethod(int(sys.argv[1]), 16)#sort by date
        elif self.args.mode=='4':
            self.listDownloadedTalks()

    def _parse_argv(self):
        # call _Info() with our formatted argv to create the self.args object
        if (sys.argv[2]=="?Upgrade=True"):
            self.args = _Info( mode=None )
        elif ( sys.argv[ 2 ] ):
            exec "self.args = _Info(%s')" % (sys.argv[ 2 ][ 1 : ].replace( "&", "', " ).replace("=", "='"))
        else:
            self.args = _Info( mode=None )

    def _get_settings(self):
        self.settings = {}
        self.settings['video_quality'] =  xbmcplugin.getSetting( 'video_quality' )
        self.settings['download_mode'] =  xbmcplugin.getSetting( 'download_mode' )
        self.settings['download_path'] =  xbmcplugin.getSetting( 'download_path' )

    def addFullDir(self,name,url,mode,plot,thumb):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=thumb,thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot":plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

    def addFullLink(self,name,url,plot,date,year,genre,author,episode=''):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={"Title":name,"Studio":"Ted","Writer":author,"Plot":plot,"Plotoutline":plot,"Date":date,"Year":year,"Genre":genre,"Episode":episode } )
        if(os.path.isdir(self.settings['download_path']) and self.settings['download_mode']=='1'):
            action = "XBMC.RunPlugin(%s?downloadTalk=True)" % ( sys.argv[ 0 ], )
            liz.addContextMenuItems([(xbmc.getLocalizedString(30020), action,)])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

    def showCategories(self):
            #set rssfeed for 'Browse All'
        if(self.settings['video_quality']=='0'):
            feedUrl=self.hdFeed
        elif(self.settings['video_quality']=='1'):
            feedUrl=self.sdFeed
        elif(self.settings['video_quality']=='2'):
            feedUrl=self.auFeed
            #check for downloads section
        showDownloadCat=False
        if(self.settings['download_mode']=='1'):
            try:
                folder=os.listdir(self.settings['download_path'])
                for file in folder:
                    if file.startswith('TedTalks'):
                        showDownloadCat=True
                        download_plot=xbmc.getLocalizedString(30033)
                        download_thumb='http://images.ted.com/images/ted/215_291x218.jpg'
            except: pass
            ##set plots and thumbs
        all_plot=xbmc.getLocalizedString(30004)
        all_thumb='http://images.ted.com/images/ted/474_291x218.jpg'
        theme_plot=xbmc.getLocalizedString(30003)
        theme_thumb='http://images.ted.com/images/ted/481_291x218.jpg'
            #add folders
        ok=self.addFullDir(' '+xbmc.getLocalizedString(30031),feedUrl,1,all_plot,all_thumb)#space ensures this goes to the top
        #ok=self.addFullDir(xbmc.getLocalizedString(30030),self.themes,2,theme_plot,theme_thumb)
        if showDownloadCat:
            ok=self.addFullDir(xbmc.getLocalizedString(30033),self.settings['download_path'],4,download_plot,download_thumb)
        self.listThemes()
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

    def clean_url(self,url):
        return url.replace("%3A",":").replace("%2F","/")

    def getHTML(self,site):
        print 'TED Talks Plugin --> reading '+site
        req = urllib2.Request(site)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

    def listThemes(self):
        iconDict = {'Live Music': 'http://images.ted.com/images/ted/233_291x218.jpg', 'Speaking at TED2009': 'http://images.ted.com/images/ted/70532_291x218.jpg', 'Whipsmart Comedy': 'http://images.ted.com/images/ted/8614_291x218.jpg', 'Spectacular Performance': 'http://images.ted.com/images/ted/45707_291x218.jpg', 'Peering into Space': 'http://images.ted.com/images/ted/496_291x218.jpg', 'TED Under 30': 'http://images.ted.com/images/ted/67719_291x218.jpg', 'Technology, History and Destiny': 'http://images.ted.com/images/ted/48704_291x218.jpg', 'How the Mind Works': 'http://images.ted.com/images/ted/54229_291x218.jpg', 'The Rise of Collaboration': 'http://images.ted.com/images/ted/481_291x218.jpg', 'Hidden Gems': 'http://images.ted.com/images/ted/200_291x218.jpg', "What's Next in Tech": 'http://images.ted.com/images/ted/63395_291x218.jpg', 'Medicine Without Borders': 'http://images.ted.com/images/ted/39479_291x218.jpg', 'TED Prize Winners': 'http://images.ted.com/images/ted/34766_291x218.jpg', "Evolution's Genius": 'http://images.ted.com/images/ted/1484_291x218.jpg', 'Unconventional Explanations': 'http://images.ted.com/images/ted/63348_291x218.jpg', 'Media That Matters': 'http://images.ted.com/images/ted/55163_291x218.jpg', 'Presentation Innovation': 'http://images.ted.com/images/ted/1473_291x218.jpg', 'Words About Words': 'http://images.ted.com/images/ted/16161_291x218.jpg', 'Art Unusual': 'http://images.ted.com/images/ted/18378_291x218.jpg', 'Not Business as Usual': 'http://images.ted.com/images/ted/143_291x218.jpg', 'To Boldly Go ...': 'http://images.ted.com/images/ted/268_291x218.jpg', 'Architectural Inspiration': 'http://images.ted.com/images/ted/474_291x218.jpg', 'Africa: The Next Chapter': 'http://images.ted.com/images/ted/13929_291x218.jpg', 'TED in 3 Minutes': 'http://images.ted.com/images/ted/68573_291x218.jpg', 'What Makes Us Happy?': 'http://images.ted.com/images/ted/387_291x218.jpg', 'Pangea Day': 'http://images.ted.com/images/ted/35977_291x218.jpg', 'Inspired by Nature': 'http://images.ted.com/images/ted/502_291x218.jpg', 'Is There a God?': 'http://images.ted.com/images/ted/1455_291x218.jpg', 'Tales of Invention': 'http://images.ted.com/images/ted/1497_291x218.jpg', 'Design Like You Give a Damn': 'http://images.ted.com/images/ted/6561_291x218.jpg', 'How We Learn': 'http://images.ted.com/images/ted/221_291x218.jpg', 'Bold Predictions, Stern Warnings': 'http://images.ted.com/images/ted/164_291x218.jpg', 'Master Storytellers': 'http://images.ted.com/images/ted/25111_291x218.jpg', 'Animals That Amaze': 'http://images.ted.com/images/ted/381_291x218.jpg', 'The Power of Cities': 'http://images.ted.com/images/ted/1456_291x218.jpg', 'A Greener Future?': 'http://images.ted.com/images/ted/1616_291x218.jpg', 'Top 10 TEDTalks': 'http://images.ted.com/images/ted/33852_291x218.jpg', 'New on TED.com': 'http://images.ted.com/images/ted/71466_291x218.jpg', 'Rethinking Poverty': 'http://images.ted.com/images/ted/18551_291x218.jpg', 'The Creative Spark': 'http://images.ted.com/images/ted/42622_291x218.jpg', 'Might You Live a Great Deal Longer?': 'http://images.ted.com/images/ted/1474_291x218.jpg'}
        link=self.getHTML(self.themes)
        p=re.compile('<li><a href="(/index\.php/themes.+?)">(.+?)</a></li>')
        items=p.findall(link)
        for i in range(len(items)):
            feedUrl='http://ted.com'+items[i][0]
            ok=self.addFullDir(items[i][1],feedUrl,3,'', iconDict[items[i][1]])
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )

    def listThemeTalks(self):
        link=self.getHTML(self.clean_url(self.args.url))
        p=re.compile('alternate" href="(.*)" type')
        match=p.findall(link)
        p=re.compile('//')
        match=p.sub('//www.',match[0])
        if self.settings['video_quality']=='0':
            d_HD=feedparser.parse(self.hdFeed)
        elif self.settings['video_quality']=='2':
            d_AU=feedparser.parse(self.auFeed)
        talks=self.listMedia(match,self.args.mode)

    def listDownloadedTalks(self):
        path=self.settings['download_path']
        items=os.listdir(path)
        for item in items:
             if item.startswith('TedTalks'):
                name=item.split('TedTalks')[1].split('.mp4')[0]
                path=xbmc.translatePath(os.path.join(path,item))
                liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                liz.setInfo( type="Video", infoLabels={"Title":name} )
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=path,listitem=liz)
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )
                    

    def checkHD(vid):
        p = vid.rindex('.')
        vid_tmp=vid[:p] + '_480.' + vid[p+1:]
        for i in range(len(d_HD.entries)):
            if d_HD.entries[i].has_key('enclosures'):
                if vid_tmp==d_HD.entries[i].enclosures[0].href:
                    vid=vid_tmp
        return vid

    def checkAU(vid):
        try:
            p=vid.rindex('-')
            vid_tmp=vid[:p]+'.mp3'
        except:
            p=vid.rindex('.')
            vid_tmp=vid[:p]+'.mp3'
        for i in range(len(d_AU.entries)):
            if d_AU.entries[i].has_key('enclosures'):
                if vid_tmp==d_AU.entries[i].enclosures[0].href:
                    vid=vid_tmp
        return vid

    def listMedia(self,url,mode):
        talks=[]
        talks.append(xbmc.getLocalizedString(30010))
        url=self.clean_url(url)
        d=feedparser.parse(url)
        for i in range(len(d.entries)):
            if d.entries[i].has_key('title'):
                p=re.compile('TEDTalks : ') #remove tedtalks from title    
                name=p.sub('',d.entries[i].title)
            else:
                name=''
            if d.entries[i].has_key('enclosures'):
                vid=d.entries[i].enclosures[0].href
                if mode==3 and settings['video_quality']=='0':
                    vid=self.checkHD(vid)
                elif mode==3 and settings['video_quality']=='2':
                    vid=self.checkAU(vid)
            else:
                vid=''
            if d.entries[i].has_key('summary'):
                q=re.compile('<img .* />') #remove useless image tag from summary
                plot=q.sub('',d.entries[i].summary)
                
            else:
                plot=''
            if d.entries[i].has_key('date'):
                date_p=d.entries[i].date_parsed
                date=str(date_p[2])+'/'+str(date_p[3])+'/'+str(date_p[0])#date ==dd/mm/yyyy
            else:
                date_p=''
                date=''
            if d.entries[i].has_key('category'):
                genre=d.entries[i].category
            else:
                genre=''
            if d.entries[i].has_key('author'):
                author=d.entries[i].author
            else:
                author=''
            ep=i+1
            talk=[]
            talk=(name,vid,plot,date,date_p[0],genre,author,ep)
            talks.append(talk)
            #print name,vid,plot,date,date_p[0],genre,author,ep
            ok=self.addFullLink(name,vid,plot,date,date_p[0],genre,author,ep)
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=ok )
        return talks
