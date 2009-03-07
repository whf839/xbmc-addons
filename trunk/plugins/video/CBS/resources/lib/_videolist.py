import xbmcplugin
import xbmcgui
import xbmc

import common
import urllib,urllib2
import sys
import re

class Main:

    def __init__( self ):
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        name = common.args.name
        showid = common.args.url
        if common.args.mode == 'List':
            self.VIDEOSHOWIDS(showid,name)
        elif common.args.mode == 'Latest':
            self.VIDEOLINKS(showid,name)
        elif common.args.mode == 'Popular':
            self.VIDEOLINKS(showid,name)
        elif common.args.mode == 'Clips':
            self.VIDEOLINKS(showid,name)
        elif common.args.mode == 'Seasons':
            self.VIDEOLINKS(showid,name)        
        elif common.args.mode == 'SeasonsList':
            self.VIDEOSHOWSEASONS(showid,name)
        elif common.args.mode == 'ListHD':
            self.VIDEOLINKS(showid,name)

    def VIDEOSHOWIDS(self,showid,name):
        #All Videos
        #url = "http://www.cbs.com/sitefeeds" + showid + "all.js"
        C = 1
        url = common.SITEFEED_URL + showid + "recent.js"
        if self.TESTURL(url) == True:
                common.addDirectory(str(C) + ". " + "Latest Videos",url,"Latest",common.args.thumbnail,common.args.thumbnail)
                C = C + 1
        url = common.SITEFEED_URL + showid + "popular.js"
        if self.TESTURL(url) == True:
                common.addDirectory(str(C) + ". " + "Most Popular",url,"Popular",common.args.thumbnail,common.args.thumbnail)
                C = C + 1
        url = common.SITEFEED_URL + showid + "clips.js"
        if self.TESTURL(url) == True:
                common.addDirectory(str(C) + ". " + "Clips",url,"Clips",common.args.thumbnail,common.args.thumbnail)
                C = C + 1

        #Special Crimetime case. Normal video lists unavailable
        if showid == "/crimetime/":
                url = "http://www.cbs.com/crimetime/js/video/behind_the_scenes.js"
                common.addDirectory(str(C) + ". " + "Behind the Scenes",url,"Clips",common.args.thumbnail,common.args.thumbnail)
                C = C + 1
                url = "http://www.cbs.com/crimetime/js/video/48_hours.js"
                common.addDirectory(str(C) + ". " + "48 Hours: Crimetime",url,"Clips",common.args.thumbnail,common.args.thumbnail)
                C = C + 1

        #Full Episodes Listings
        url = common.SITEFEED_URL + showid + "episodes.js"
        #Check seasons.js for Season Count
        if self.CHECKSEASONS(showid) > 1:
                common.addDirectory(str(C) + ". " + "Seasons",showid,"SeasonsList",common.args.thumbnail,common.args.thumbnail)
        #Add Episodes
        else:
                if self.TESTURL(url) == True:
                        self.VIDEOLINKS(url,name)

                        
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )


    def VIDEOSHOWSEASONS(self,showid,name):
        #Season Filter
        seasons = self.CHECKSEASONS(showid)
        C = 0
        for season in range(1,30):
                url = common.SITEFEED_URL + showid + str(season) + ".js"
                if self.TESTURL(url) == True:
                        C = C + 1
                        common.addDirectory('Season ' + str(season),url,'Seasons',common.args.thumbnail,common.args.thumbnail)
                        if C == int(seasons):
                            xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )
                            return
        


    #Tests URLs for errors 
    def TESTURL(self, url):
        try:
                link=common.getHTML(url)
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                #CHECKSEASONS
                if "seasons.js" in url:
                        return True
                #Check for a Video count other then 0
                match=re.compile('var videoCount = (.+?);').findall(link)
                videocount = match[0]
                if videocount == '0':
                        return False
                #This is a good Video list
                return True

            
    def CHECKSEASONS(self, showid):
        #Seasons
        url = "http://www.cbs.com/sitefeeds" + showid + "seasons.js"
        if self.TESTURL(url) == True:
                link=common.getHTML(url)
                match=re.compile('var categoryCount = (.+?);').findall(link)
                seasons = int(match[0])
                return seasons


    def VIDEOLINKS(self,url,name):
        showfilter = ''
        if url == "Episodes":
            HD = True
            typefilter = url
            showfilter = name
            url = common.HDVIDEOS_URL
        elif url == "Clips":
            HD = True
            typefilter = url
            showfilter = name
            url = common.HDVIDEOS_URL
        else:
            typefilter = ''
            showfilter = ''
            HD = False
        link=common.getHTML(url)
        match=re.compile('videoProperties(.+?);\r').findall(link)
        #set List Counter to 1 for popular and recent shows
        if "popular" in url or "recent" in url:
                C = 1
        else:
                C = 0
        for url in match:
                # breakurl item list
                #  0 = empty
                #  1 = title1
                #  2 = title2
                #  3 = series_title
                #  4 = season_number
                #  5 = description
                #  6 = episode_number
                #  7 = primary_cid
                #  8 = category_type
                #  9 = runtime
                # 10 = pid or 480p pid
                # 11 = thumbnail 160x120
                # 12 = fullsize thumbnail 640x480
                # 13 = the current category value for the existing show pages(mostly blank)
                # 14 = site name in xml, lowercased and trimmed to match the value passed from the left menu(mostly blank)
                # 15 = empty or 720p pid
                breakurl = url.split("','")
                #change single digit season numbers to 2 digits
                if len(breakurl[4]) == 1:
                        breakurl[4] = "0" + breakurl[4]
                #change single digit episode numbers to 2 digits
                if len(breakurl[6]) == 1:
                        breakurl[6] = "0" + breakurl[6]
                #Standard Definition pid
                breakurl[15] = breakurl[15].replace("')","")
                if breakurl[15] == '':
                        pid = breakurl[10]
                        if HD == True:
                            continue
                #480p and 720p pids
                elif breakurl[15] <> '':
                        pid = breakurl[10] + "<break>" + breakurl[15]

                thumbnail = breakurl[12]
                plot = breakurl[5].replace('\\','')
                duration = breakurl[9]
                if breakurl[4] <> '':
                        season = int(breakurl[4].replace('_','').replace('-','').replace('.',''))
                else:
                        season = 0
                if breakurl[6] <> '':
                        episode = int(breakurl[6].replace('_','').replace('-','').replace('.',''))
                else:
                        episode = 0
                #seriestitle = breakurl[3]
                #episodetitle = breakurl[2]
                #List Order Counter for popular and recent lists
                if C <> 0:
                        if len(str(C)) == 1:
                                ordernumber = "#0" + str(C) + ". "                          
                        else:
                                ordernumber = "#" +str(C) + ". "
                        C = C + 1
                #Blank ordernumber value for all other lists
                else:
                        ordernumber = ''
                #Generate filename for Full Episode - series title + "S" + season number+ "E" + episode number + " - " + episode title
                if breakurl[8] == "Full Episode":
                         if "late" in breakurl[1] or "daytime" in breakurl[1]:
                                finalname = ordernumber + breakurl[2]
                         else:
                                finalname = ordernumber + breakurl[3] + " S" + breakurl[4] + "E" + breakurl[6] + " - " + breakurl[2]
                #Generate filename for Clip - series title + " - " + episode title + " (Clip)"
                elif breakurl[8] == "Clip": 
                        #finalname = ordernumber + breakurl[3] + " - " + breakurl[2] + " (Clip) " + breakurl[9]
                        if breakurl[2] == '':
                                finalname = ordernumber + breakurl[3] + " (Clip)"
                        if breakurl[3] in breakurl[2]:
                                finalname = ordernumber + breakurl[2] + " (Clip)"
                        else:
                                finalname = ordernumber + breakurl[2] + " (Clip) - " + breakurl[3] 
                #HD title and for everything else
                else:
                        if len(breakurl[9]) > 4:
                            finalname = breakurl[3] + " E" + breakurl[6] + " - " + breakurl[2] # + " (" + breakurl[9] + ")"
                        elif len(breakurl[9]) <= 4:
                            if breakurl[3] in breakurl[2]:
                                finalname = breakurl[2] + " (Clip)" # (" + breakurl[9] + ")"
                            else:
                                finalname = breakurl[3] + " - " + breakurl[2] + " (Clip)" # + " (" + breakurl[9] + ")"
                #Clean filename
                finalname = finalname.replace('\\\'','\'')
                if "<break>" in pid:
                    if breakurl[3] == showfilter:
                        if typefilter == "Episodes":
                            if len(breakurl[9]) > 4:
                                passname = finalname.replace(ordernumber,'')
                                url = sys.argv[0]+'?mode="'+'Play'+'"&name="'+urllib.quote_plus(passname)+'"&pid="'+urllib.quote_plus(pid)+'"&thumbnail="'+urllib.quote_plus(thumbnail)+'"'#+'"&plot="'+urllib.quote_plus(plot)+'?duration="'+urllib.quote_plus(duration)+'?season="'+urllib.quote_plus(str(season))+'?episode="'+urllib.quote_plus(str(episode))+'"'
                                item=xbmcgui.ListItem(finalname, iconImage=thumbnail, thumbnailImage=thumbnail)
                                item.setInfo( type="Video",
                                             infoLabels={ "Title": finalname,
                                                            "Season": season,
                                                            "Episode": episode,
                                                            "Duration": duration,
                                                            "Plot": plot})
                                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=item,isFolder=True)
                                continue
                        elif typefilter == "Clips":
                            if len(breakurl[9]) <= 4:
                                passname = finalname.replace(ordernumber,'')
                                url = sys.argv[0]+'?mode="'+'Play'+'"&name="'+urllib.quote_plus(passname)+'"&pid="'+urllib.quote_plus(pid)+'"&thumbnail="'+urllib.quote_plus(thumbnail)+'"'#+'"&plot="'+urllib.quote_plus(plot)+'?duration="'+urllib.quote_plus(duration)+'?season="'+urllib.quote_plus(str(season))+'?episode="'+urllib.quote_plus(str(episode))+'"'
                                item=xbmcgui.ListItem(finalname, iconImage=thumbnail, thumbnailImage=thumbnail)
                                item.setInfo( type="Video",
                                            infoLabels={ "Title": finalname,
                                                            "Season": season,
                                                            "Episode": episode,
                                                            "Duration": duration,
                                                            "Plot": plot})
                                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=item,isFolder=True)
                                continue
                else:
                    passname = finalname.replace(ordernumber,'')
                    url = sys.argv[0]+'?mode="'+'Play'+'"&name="'+urllib.quote_plus(passname)+'"&pid="'+urllib.quote_plus(pid)+'"&thumbnail="'+urllib.quote_plus(thumbnail)+'"'#+'"&plot="'+urllib.quote_plus(plot)+'?duration="'+urllib.quote_plus(duration)+'?season="'+urllib.quote_plus(str(season))+'?episode="'+urllib.quote_plus(str(episode))+'"'
                    item=xbmcgui.ListItem(finalname, iconImage=thumbnail, thumbnailImage=thumbnail)
                    item.setInfo( type="Video",
                                 infoLabels={ "Title": finalname,
                                                "Season": season,
                                                "Episode": episode,
                                                "Duration": duration,
                                                "Plot": plot})
                    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=item)
                    continue
        #add Clips for HD
        #if typefilter == "Episodes":
        #    common.addDirectory(showfilter, "Clips", "ListHD")
        xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ) )
                        
