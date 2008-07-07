import urllib,urllib2,re,xbmcplugin,xbmcgui
#NOIKET&VUTHANG PLUGIN 2008

def MAINCATS():
        addDir("NOIKET","http://74.54.54.194/",1,"http://74.54.54.194/~noiket/images2/logo.gif")
        addDir( "VUTHANG","http://74.54.54.194/",7,"http://vuthang.com/video/images/logo.gif")
        
def NOIKET():
        addDir("PHIM BO","http://74.54.54.194/",2,"http://74.54.54.194/~noiket/images2/navm1_1.gif")
        addDir("PHIM LE","http://74.54.54.194/",3,"http://74.54.54.194/~noiket/images2/navm2_1.gif")

def VUTHANG():
        addDir("PHIM BO","http://74.54.54.194/",8,"")
        addDir("VIETNAM","http://74.54.54.194/",9,"")
        addDir("A CHAU","http://74.54.54.194/",10,"")
        addDir("PHIM MY","http://74.54.54.194/",11,"")
        addDir("VIDEO CLIPS","http://74.54.54.194/",12,"")

def PHIMBO_VUTANG():
        addDir("PHIM HONG KONG","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=109",13,"")
        addDir("PHIM HAN QUOC","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=110",13,"")
        addDir("PHIM TQ-DL","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=111",13,"")
        addDir("PHIM NHAT BAN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=112",13,"")
        addDir("TRUNG QUOC","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=2",13,"")
        addDir("DAI LOAN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=4",13,"")
        addDir("PHIM CAM TRE EM DUOI 18","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=113",13,"")

def VIETNAM_VUTANG():
        addDir("PHIM VIETNAM","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=115",13,"")
        addDir("HAI KICH","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=116",13,"")
        addDir("CA NHAC","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=117",13,"")
        addDir("PHONG SU - THOI SU","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=118",13,"")
        addDir("PHIM NAU AN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=119",13,"")
        addDir("THIEU NHI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=120",13,"")
        addDir("CAI LUONG","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=142",13,"")
        addDir("PHONG VAN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=143",13,"")
        addDir("KARAOKE","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=164",13,"")

def ACHAU_VUTANG():
        addDir("PHIM VO THUAT / KIEM HIEP","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=122",13,"")
        addDir("PHIM HANH DONG","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=123",13,"")
        addDir("PHIM HAI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=124",13,"")
        addDir("PHIM MA - KINH DI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=125",13,"")
        addDir("PHIM TINH CAM","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=126",13,"")
        addDir("PHIM A CHAU","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=147",13,"")
        addDir("DO THUAT","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=148",13,"")
        addDir("NHAC HAN QUOC TAU","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=149",13,"")
        addDir("PHIM NHAT BAN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=150",13,"")
        addDir("PHIM LE HAN QUOC","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=127",13,"")
        addDir("PHIM HANH DONG","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=128",13,"")
        addDir("PHIM HAI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=129",13,"")
        addDir("PHIM KINH DI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=130",13,"")
        addDir("PHIM TINH CAM","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=131",13,"")
        addDir("KIEMHIEP","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=15",13,"")
        addDir("NHAT BAN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=17",13,"")
        addDir("VIET NAM","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=19",13,"")

def PHIMMY_VUTANG():
        addDir("PHIM HANH DONG","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=133",13,"")
        addDir("PHIM TINH CAM - HAI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=134",13,"")
        addDir("PHIM KINH DI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=135",13,"")
        addDir("NHAC CONCERT","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=21",13,"")
        addDir("NHAC QUOC TE","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=136",13,"")
        addDir("DIVA CHANNEL","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=144",13,"")
        addDir("PHIM AU MY","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=146",13,"")
        addDir("CAC NUOC KHAC","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=22",13,"")
        addDir("PHIM HOAT HINH","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=137",13,"")
        addDir("ANIME","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=18",13,"")
        addDir("PHIM ONLINE","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=140",13,"")
        addDir("PHIM THAI LAN","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=155",13,"")
        addDir("PHIM HAI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=156",13,"")
        addDir("KINH DI - MA","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=157",13,"")
        addDir("TINH CAM","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=158",13,"")
        addDir("PHIEU LUU - KHOA HOC","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=159",13,"")

def VIDEOCLIPS_VUTANG():
        addDir("NHAC PHIM ","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=138",13,"")
        addDir("FUNNY CLIPS","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=139",13,"")
        addDir("CHUYEN DO DAY","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=151",13,"")
        addDir("KI THUAT","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=152",13,"")
        addDir("ENTERTAINMENT","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=153",13,"")
        addDir("SEXY","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=154",13,"")
        addDir("NHAC KHONG LOI","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=160",13,"")
        addDir("QUANG CAO CLIPS","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=161",13,"")
        addDir("LIVE SHOW","http://vuthang.com/videos.aspx?c=1&p=1&q=&v=162",13,"")
        
def PHIMBO():
        addDir("HONG KONG","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=1",4,"http://74.54.54.194/~noiket/images2/nav1_1.gif")
        addDir("TRUNG QUOC","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=2",4,"http://74.54.54.194/~noiket/images2/nav2_1.gif")
        addDir("DAI LOAN","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=3",4,"http://74.54.54.194/~noiket/images2/nav3_1.gif")
        addDir("HAN QUOC","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=4",4,"http://74.54.54.194/~noiket/images2/nav4_1.gif")
        addDir("NHAT BAN","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=5",4,"http://74.54.54.194/~noiket/images2/nav5_1.gif")
        addDir("VIET NAM","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=6",4,"http://74.54.54.194/~noiket/images2/nav6_1.gif")
def PHIMLE():
        addDir("HANH DONG","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=11",4,"http://74.54.54.194/~noiket/images2/nav11_1.gif")
        addDir("TINH CAM","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=12",4,"http://74.54.54.194/~noiket/images2/nav12_1.gif")
        addDir("PHIM HAI","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=13",4,"http://74.54.54.194/~noiket/images2/nav13_1.gif")
        addDir("KINH DI","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=14",4,"http://74.54.54.194/~noiket/images2/nav14_1.gif")
        addDir("KIEM HIEP","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=15",4,"http://74.54.54.194/~noiket/images2/nav15_1.gif")
        addDir("HAN QUOC","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=16",4,"http://74.54.54.194/~noiket/images2/nav16_1.gif")
        addDir("NHAT BAN","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=17",4,"http://74.54.54.194/~noiket/images2/nav17_1.gif")
        addDir("ANIME","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=18",4,"http://74.54.54.194/~noiket/images2/nav18_1.gif")
        addDir("VIET NAM","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=19",4,"http://74.54.54.194/~noiket/images2/nav19_1.gif")
        addDir("HAI KICH","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=20",4,"http://74.54.54.194/~noiket/images2/nav20_1.gif")
        addDir("NHAC CONCERT","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=21",4,"http://74.54.54.194/~noiket/images2/nav21_1.gif")
        addDir("CAC NUOC KHAC","http://74.54.54.194/~noiket/video_browse.php?viewtype=&category=&category=&chid=22",4,"http://74.54.54.194/~noiket/images2/nav22_1.gif")

def INDEXNOIKET(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<img src="(.+?)" height=150 alt="" border="0" />\n   \n\t\t</div>\n\t\t</table>\n\t\t\n\t\t        <DIV class=moduleFeaturedTitle style="width:140; padding-top:5">\n        <A href="(.+?)">\n(.+?)\n        </A>')
        match=p.findall(link)
        for thumbnail,url,name in match:
                NEW="http://74.54.54.194/~noiket/"+url
                addDir(name,NEW,5,thumbnail)
        #TRY AGAIN
        p=re.compile('<IMG src="(.+?)" height=150 alt="" border="0">\n   \n\t\t</div>\n\t\t</table>\n\t\t\n\t\t        <DIV class=moduleFeaturedTitle style="width:140; padding-top:5">\n        <A href="(.+?)">\n(.+?)\n        </A>\n\t\t<br />')
        match=p.findall(link)
        for thumbnail,url,name in match:
                NEW2="http://74.54.54.194/~noiket/"+url
                addDir(name,NEW2,5,thumbnail)
        #GET PAGES
        p=re.compile("<a href='(.+?)'><img src='images2/arrow_right_on.gif' border=0 /></a>")
        page=p.findall(link)
        url="http://74.54.54.194/~noiket/"+page[0]
        addDir("                    NEXT PAGE   ",url,4,"http://74.54.54.194/~noiket/images2/arrow_right_on.gif")

def INDEXVUTHANG(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<a href=\'(.+?)#s\' class="prlink11bl">(.+?)</a></b></div>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t<tr>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td align="center" height="150">\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href=\'.+?\'>\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<img src=\'(.+?)\'')
        match=p.findall(link)
        for url,name,thumbnail in match:
                NEW="http://vuthang.com/"+url
                addDir(name,NEW,14,thumbnail)
        #GET PAGES
        p=re.compile(" &nbsp;&nbsp;&nbsp;<a class=\'pagelink\' href=(.+?)>")
        page=p.findall(link)
        try:
                url="http://vuthang.com/"+page[-1]
                addDir("                    NEXT PAGE   ",url,13,"")
        except:
                IndexError
                pass

def EPSNOIKET(url,name):
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<a href="(.+?)">(.+?)</a></li>')
        match=p.findall(link)
        for url,episode in match:
                part="EPISODE  "+episode
                NEW="http://74.54.54.194/~noiket/"+url
                addDir(part,NEW,6,"")

def EPSVUTHANG(url,name):
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<a class="prlink11bl" href=\'(.+?)#s\'>\r\n\t\t\t\t<span id=".+?">(.+?)</span></a>')
        match=p.findall(link)
        for url,episode in match:
                part="EPISODE  "+episode
                addDir(part,url,15,"")
                
                
def ExtractMediaUrl(url, data):
        
        if url.find("megavideo.com") > 0:
                codeRegex = '<ROW url="(.+?)" runtime=".+?" runtimehms=".+?" size=".+?" waitingtime=".+?" k=".+?"></ROW>'
                codeResults = re.findall(codeRegex, data, re.DOTALL + re.IGNORECASE)
                if len(codeResults) > 0:
                        code = codeResults[-1]
                        dictionary = {"0":":","%24": ".", "%25": "/", "%3A": "0", "%3B": "1", "8": "2", "9": "3", "%3E": "4", "%3F": "5", "%3C": "6", "%3D": "7", "2": "8", "3": "9", "a": "k", "b": "h", "c": "i", "d": "n", "e": "o", "f": "l", "g": "m", "h": "b", "i": "c", "k": "a", "l": "f", "m": "g", "n": "d", "o": "e", "p": "z", "s": "y", "%7E": "t", "y": "s","%7C": "v", "%7D": "w", "z": "p"}
                        return RegexReplaceDictionary(code, dictionary) 
                else:
                        return ""
        
def RegexReplaceDictionary(string, dictionary):
      
        rc = re.compile('|'.join(map(re.escape, dictionary)))
        def Translate(match):
                return dictionary[match.group(0)]
        return rc.sub(Translate, string)


def NOIKETVIDLINKS(url,name):
        
                       
        #VEOH
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<embed src=".+?permalinkId=(.+?)&id=.+?"')
        p=re.compile('<embed  src=".+?permalinkId=(.+?)&id=.+?"')
        match=p.findall(link)
        for VEOH in match:
                url='http://127.0.0.1:64652/'+VEOH+"?.avi"
                addLink("WATCH VEOH HIGH QUALITY",url,"")

        #DAILYMOTION
        
        p=re.compile('<param name="movie" value="http://www.dailymotion.com/swf/(.+?)" />')
        match=p.findall(link)
        for url in match:
                linkage="http://www.dailymotion.com/video/"+url
        try:
                req = urllib2.Request(linkage)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('url=rev=.+?&uid=.+?&lang=en&callback=.+?&preview=.+?&video=(.+?)%40%40spark')
                match=p.findall(link)
                for url1 in match:
                        decode=urllib.unquote(url1)
                        urll="http://www.dailymotion.com"+decode
                        addLink("WATCH DAILYMOTION",urll,"")
        except UnboundLocalError:
                pass
        
        #MEGAVIDEO
        p=re.compile('<embed src="(.+?)" type="application/x-shockwave-flash" ')
        match=p.findall(link)
        for a in match:
                if len(a)<79:
                        a=a[:-43]
                        code=re.sub('http://www.megavideo.com/v/','v=',a)
                        url="http://www.megavideo.com/xml/videolink.php?"+code
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        new=ExtractMediaUrl(url,link)
                        flvappend="voinage.flv"
                        flvlink=new+flvappend
                        addLink("WATCH MEGAVIDEO",flvlink,"")
                        
                
                elif len(a)<80:
                                a=a[:-44]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("WATCH MEGAVIDEO",flvlink,"")
                                
                                        
                                
                elif len(a)<81:
                                a=a[:-45]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("WATCH MEGAVIDEO",flvlink,"")
     
        #GOOGLE
        p=re.compile('<embed style="width:100%; height:100%;" id="VideoPlayback" type="application/x-shockwave-flash" src=".+?docId=(.+?)&hl=en" flashvars="100%">')
        GOOGLE=p.findall(link)
        
        try:
                req = urllib2.Request("http://video.google.com/videoplay?docid="+GOOGLE[0])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('.+?videoUrl.+?.+?.+?.+?(.+?)%26sigh')
                match=p.findall(link)
                for url2 in match:
                        addLink("WATCH GOOGLE HIGH QUALITY",url2,"")
        except IndexError:
                pass

def VIDSVUTHANG(url,name):
                               
        #VEOH
        req = urllib2.Request("http://vuthang.com/v.aspx"+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile("<embed src=\'.+?permalinkId=(.+?)\'")
        match=p.findall(link)
        for VEOH in match:
                url='http://127.0.0.1:64652/'+VEOH+"?.avi"
                addLink("WATCH VEOH HIGH QUALITY",url,"")
        p=re.compile('<embed src=".+?permalinkId=(.+?)&id=.+?&player=videodetailsembedded&videoAutoPlay=0"')
        match=p.findall(link)
        for VEOH in match:
                url='http://127.0.0.1:64652/'+VEOH+"?.avi"
                addLink("WATCH VEOH HIGH QUALITY",url,"")
        p=re.compile("<embed id='phim' title='phim online' src='.+?permalinkId=(.+?)&id=anonymous&player=videodetailsembedded&videoAutoPlay=0'")
        match=p.findall(link)
        for VEOH in match:
                url='http://127.0.0.1:64652/'+VEOH+"?.avi"
                addLink("WATCH VEOH HIGH QUALITY",url,"")
                
        #DAILYMOTION
        req = urllib2.Request("http://vuthang.com/v.aspx"+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()        
        p=re.compile('<embed src="http://www.dailymotion.com/swf/(.+?)" type="application/x-shockwave-flash" width="100%" height="100%" allowFullScreen="true" allowScriptAccess="always"></embed>')
        match=p.findall(link)
        for url in match:
                linkage="http://www.dailymotion.com/video/"+url
        try:
                req = urllib2.Request(linkage)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('url=rev=.+?&uid=.+?&lang=en&callback=.+?&preview=.+?&video=(.+?)%40%40spark')
                match=p.findall(link)
                for url1 in match:
                        decode=urllib.unquote(url1)
                        urll="http://www.dailymotion.com"+decode
                        addLink("WATCH DAILYMOTION",urll,"")
        except UnboundLocalError:
                pass
        
        #MEGAVIDEO
        req = urllib2.Request("http://vuthang.com/v.aspx"+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<embed src="(.+?)" type="application/x-shockwave-flash" ')
        match=p.findall(link)
        for a in match:
                if len(a)<79:
                        a=a[:-43]
                        code=re.sub('http://www.megavideo.com/v/','v=',a)
                        url="http://www.megavideo.com/xml/videolink.php?"+code
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        new=ExtractMediaUrl(url,link)
                        flvappend="voinage.flv"
                        flvlink=new+flvappend
                        addLink("WATCH MEGAVIDEO",flvlink,"")
                        
                
                elif len(a)<80:
                                a=a[:-44]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("WATCH MEGAVIDEO",flvlink,"")
                                
                                        
                                
                elif len(a)<81:
                                a=a[:-45]
                                code=re.sub('http://www.megavideo.com/v/','v=',a)
                                url="http://www.megavideo.com/xml/videolink.php?"+code
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                                new=ExtractMediaUrl(url,link)
                                flvappend="voinage.flv"
                                flvlink=new+flvappend
                                addLink("WATCH MEGAVIDEO",flvlink,"")
       
        #GOOGLE
        req = urllib2.Request("http://vuthang.com/v.aspx"+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile("<embed src='.+?docId=(.+?)' style='width:680px; height:505px;' id='VideoPlayback' type='application/x-shockwave-flash'> </embed>")
        GOOGLE=p.findall(link)
        try:
                req = urllib2.Request("http://video.google.com/videoplay?docid="+GOOGLE[0])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('.+?videoUrl.+?.+?.+?.+?(.+?)%26sigh')
                match=p.findall(link)
                for url2 in match:
                        addLink("WATCH GOOGLE HIGH QUALITY",url2,"")
        except IndexError:
                pass
        p=re.compile('<embed style="width:100%; height:100%;" id="VideoPlayback" type="application/x-shockwave-flash" src=".+?docId=(.+?)&hl=en"')
        GOOGLE=p.findall(link)
        try:
                req = urllib2.Request("http://video.google.com/videoplay?docid="+GOOGLE[0])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                p=re.compile('.+?videoUrl.+?.+?.+?.+?(.+?)%26sigh')
                match=p.findall(link)
                for url2 in match:
                        addLink("WATCH GOOGLE HIGH QUALITY",url2,"")
        except IndexError:
                pass

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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
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
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
        print "CATEGORY INDEX : "
        MAINCATS()
elif mode==1:
        print "NOIKET CATS : "+url
        NOIKET()
elif mode==2:
        print "INDEX OF NOIKET: "+url
        PHIMBO()
elif mode==3:
        print "INDEX OF NOIKET: "+url
        PHIMLE()
elif mode==4:
        print "INDEX OF NOIKET: "+url
        INDEXNOIKET(url,name)
elif mode==5:
        print "INDEX OF NOIKET: "+url
        EPSNOIKET(url,name)
elif mode==6:
        print " NOIKET VIDLINKS " +url
        NOIKETVIDLINKS(url,name)
elif mode==7:
        print "VUTHANG CATS: "+url
        VUTHANG()
elif mode==8:
        print "INDEX OF VUTHANG PHIMBO: "+url
        PHIMBO_VUTANG()
elif mode==9:
        print "INDEX OF VUTANG VIETNAM: "+url
        VIETNAM_VUTANG()
elif mode==10:
        print "INDEX OF ACHAU VUTANG: "+url
        ACHAU_VUTANG()
elif mode==11:
        print " INDEX OF PHIMMY VUTANG " +url
        PHIMMY_VUTANG()
elif mode==12:
        print " INDEX OF VIDEO CLIPS VUTANG " +url
        VIDEOCLIPS_VUTANG()
elif mode==13:
        print " INDEX OF VUTANG " +url
        INDEXVUTHANG(url,name)
elif mode==14:
        print " INDEX OF EPS VUTANG " +url
        EPSVUTHANG(url,name)
elif mode==15:
        print " INDEX OF VIDS VUTANG " +url
        VIDSVUTHANG(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
