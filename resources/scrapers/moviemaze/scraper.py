"""
MovieMaze Current Trailer scraper

uses the MovieMaze Trailer Plugin to retrieve videos
"""

import sys
import os

import xbmc
import xbmcaddon
import time
import re
import urllib, urllib2
from random import shuffle, random

__useragent__ = "QuickTime/7.2 (qtver=7.2;os=Windows NT 5.1Service Pack 3)"
_A_ = xbmcaddon.Addon('script.cinema.experience')
_L_ = _A_.getLocalizedString
_S_ = _A_.getSetting
__url__ = "http://www.moviemaze.de/rss/trailer.phtml"

#Moviemazer files
_AM_ = xbmcaddon.Addon('plugin.video.moviemazer')
_LM_ = _AM_.getLocalizedString
_SM_ = _AM_.getSetting
mainurl = 'http://www.moviemaze.de'

_id = _AM_.getAddonInfo('id')
_cachedir = 'special://profile/addon_data/%s/cache/' %(_id)
_imagedir = 'special://home/addons/%s/resources/images/' %(_id)

movieid = ''

class _urlopener( urllib.FancyURLopener ):
    version = __useragent__
# set for user agent
urllib._urlopener = _urlopener()

def set_movieid( movieid ):
    movieid = movieid

def getCurrent():
    returnmovies = []
    fullurl = '%s/media/trailer/' % mainurl
    link = getCachedURL(fullurl, 'mainpage.cache', _SM_('cache_movies_list'))
    matchtacttrailers = re.compile('<tr><td(?: valign="top"><b>[A-Z0-9]</b)?></td><td style="text-align:left;"><a href="/media/trailer/([0-9]+),(?:[0-9]+?,)?([^",]+?)">([^<]+)</a></td></tr>').findall(link)
    for movieid, urlend, title in matchtacttrailers:
        movie = {'movieid': movieid,
                 'title': title,
                 'urlend': urlend,
                 'rank':'',
                 'date':''}
        returnmovies.append(movie)
    return returnmovies


# Function to get a dict of detailed movie information like coverURL, plot and genres

def getMovieInfo(movieid, urlend='movie.html'):
    returnmovie = {'movieid': movieid,
                   'title': '',
                   'otitle': '',
                   'coverurl': '',
                   'plot': '',
                   'genres': '',
                   'date': ''}
    fullurl = '%s/media/trailer/%s,15,%s' %(mainurl,
                                            movieid,
                                            urlend)
    cachefile = 'id%s.cache' %(movieid)
    link = getCachedURL(fullurl, cachefile, _SM_('cache_movie_info'))
    titlematch = re.compile('<h1>(.+?)</h1>.*<h2>\((.+?)\)</h2>', re.DOTALL).findall(link)
    for title, otitle in titlematch:
        returnmovie.update({'title': title, 'otitle': otitle})
    covermatch = re.compile('src="([^"]+?)" width="150"').findall(link)
    for coverurl in covermatch:
        if coverurl != '/filme/grafiken/kein_poster.jpg':
            returnmovie.update({'coverurl': mainurl + coverurl})
    plotmatch = re.compile('WERDEN! -->(.+?)</span>').findall(link)
    for plot in plotmatch:
        plot = re.sub('<[^<]*?/?>','' , plot)
        returnmovie.update({'plot': plot})
    releasedatematch = re.compile('Dt. Start:</b> ([0-9]+.+?)<img').findall(link)
    for releasedateugly in releasedatematch:
        datearray = releasedateugly.split(' ')
        months_de_long = ['', 'Januar', 'Februar', 'M\xe4rz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
        date = datearray[0]+ str(months_de_long.index(datearray[1])).zfill(2) + '.' + datearray[2]
        returnmovie.update({'date': date})
    genresmatch = re.compile('<b style="font-weight:bold;">Genre:</b> (.+?)<br />', re.DOTALL).findall(link)
    for allgenres in genresmatch:
        returnmovie.update({'genres': allgenres})
    return returnmovie


# Function to get a list of dicts which contains trailer- URL, resolution, releasedate

def GetMovieTrailers(movieid, urlend='movie.html'):
    returntrailers = []
    fullurl = '%s/media/trailer/%s,15,%s' %(mainurl,
                                            movieid,
                                            urlend)
    cachefile = 'id%s.cache' %(movieid)
    link = getCachedURL(fullurl, cachefile, _SM_('cache_movie_info'))
    matchtrailerblock = re.compile('<table border=0 cellpadding=0 cellspacing=0 align=center width=100%><tr><td class="standard">.+?<b style="font-weight:bold;">(.+?)</b><br />\(([0-9:]+) Minuten\)(.+?</td></tr></table><br /></td></tr></table><br />)', re.DOTALL).findall(link)
    for trailername, duration, trailerblock in matchtrailerblock:
        matchlanguageblock = re.compile('alt="Sprache: (..)">(.+?)>([^<]+)</td></tr></table></td>', re.DOTALL).findall(trailerblock)
        for language, languageblock, date in matchlanguageblock:
            datearray = date.split(' ')
            months_de_short = ['', 'Jan', 'Feb', 'M\xe4rz', 'Apr', 'Mai', 'Juni', 'Juli', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
            try: date = datearray[0]+ str(months_de_short.index(datearray[1])).zfill(2) +  '.2010' #fixme: this could be made better, no idea how :)
            except: date = ''
            matchtrailer = re.compile('generateDownloadLink\("([^"]+_([0-9]+)\.(?:mov|mp4)\?down=1)"\)').findall(languageblock)
            for trailerurl, resolution in matchtrailer:
                trailer = {'trailername': trailername,
                           'duration': duration,
                           'language': language,
                           'resolution': resolution,
                           'date': date,
                           'trailerurl': mainurl+trailerurl}
                returntrailers.append(trailer)
    return returntrailers

def guessPrefTrailer(movietrailers):
    prefres = int(_SM_('trailer_xres'))
    allres = ['1920', '1280', '1024', '848', '720', '640', '512', '480', '320']
    prefmovietrailers = []
    diff = 0
    if len(filterdic(movietrailers, 'language', _SM_('trailer_lang'))) > 0:
        movietrailers = filterdic(movietrailers, 'language', _SM_('trailer_lang'))
    while len(prefmovietrailers) == 0:
        searchres = prefres + diff
        if not searchres >= len(allres):
            prefmovietrailers = filterdic(movietrailers, 'resolution', allres[searchres])
        if len(prefmovietrailers) == 0 and not diff == 0:
            searchres = prefres - diff
            if searchres >= 0:
                prefmovietrailers = filterdic(movietrailers, 'resolution', allres[searchres])
        diff += 1
        if diff > len(allres) +1:
            break
    prefmovietrailer = prefmovietrailers[len(prefmovietrailers) - 1]
    trailercaption = '%s - %s - %s (%s)' %(prefmovietrailer['trailername'],
                                           prefmovietrailer['language'],
                                           prefmovietrailer['resolution'],
                                           prefmovietrailer['date'])
    movieinfo = getMovieInfo(movieid)
    trailer = {'trailerurl': prefmovietrailer['trailerurl'],
               'title': movieinfo['title'],
               'studio': trailercaption,
               'coverurl':movieinfo['coverurl']}
    return trailer

def getCachedURL(url, filename, timetolive=1):
    requestheader = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9'
    cachefilefullpath = _cachedir + filename
    timetolive = int(timetolive) * 60 * 60
    if (not os.path.isdir(_cachedir)):
        os.makedirs(_cachedir)
    try: cachefiledate = os.path.getmtime(cachefilefullpath)
    except: cachefiledate = 0
    if (time.time() - (timetolive)) > cachefiledate:
        sock = urllib.urlopen( url )
        link = sock.read()
        encoding = sock.headers['Content-type'].split('charset=')[1]
        outfile = open(cachefilefullpath,'w')
        outfile.write(link)
        outfile.close()
    else:
        sock = open(cachefilefullpath,'r')
        link = sock.read()
    sock.close()
    return link


def filterdic(dic, key, value):
    return [d for d in dic if (d.get(key)==value)]


class Main:
    print "MovieMaze Trailer scraper"
    # base url
    BASE_CURRENT_URL = __url__
    # base paths
    BASE_CURRENT_SOURCE_PATH = os.path.join( xbmc.translatePath( "special://profile/addon_data" ), os.path.basename( _A_.getAddonInfo('path') ) )

    def __init__( self, mpaa=None, genre=None, settings=None, movie=None ):
        self.mpaa = mpaa
        self.genre = genre
        self.settings = settings

    def fetch_trailers( self ):
        # initialize trailers list
        movieid = url = thumbnail = trailer_name = language = resolution = date = title = genre = director = mpaa = studio = plot = runtime = ''
        trailers = []
        current = getCurrent()
        for movie in current:
            '''
                movie = {'movieid': movieid,
                            'title': title,
                           'urlend': urlend,
                             'rank':'',
                             'date':''}
            '''
            set_movieid( movie["movieid"] )
            get_movie_trailer = GetMovieTrailers( movie["movieid"] )
            preftrailer = guessPrefTrailer( get_movie_trailer )
            '''
                trailer = {'trailerurl': '',
                           'title': '',
                           'studio': '',     -> trailer name - language - resolution (date)
                           'coverurl': ''}
            '''
            trailer_name, language, resolution = preftrailer["studio"].split(" - ")
            resolution, date = resolution.split(" ")
            title = preftrailer["title"] + " - " + trailer_name
            movieid = movie["movieid"]
            url = preftrailer["trailerurl"]
            thumbnail = preftrailer["coverurl"]
            trailer = ( movieid, title, url, thumbnail, plot, runtime, mpaa, date, studio, genre, '', director )
            trailers += trailer
            print "----------------------------"
            print trailer
            print "----------------------------"
        return trailers
