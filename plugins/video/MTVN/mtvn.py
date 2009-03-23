import urllib, urllib2
import os, re, sys, md5, string
import xbmc, xbmcgui, xbmcplugin
import feedparser

def getURL( url ):
        try:
                print 'MTVN --> getHTML :: url = '+url
                req = urllib2.Request(url)
                req.addheaders = [('Referer', 'http://www.mtv.com'),
                                  ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7)')]
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
        except urllib2.URLError, e:
                print 'Error code: ', e.code
                return False
        else:
                return link

#Universal Parameters
#max-results:   Limit the maximum number of results. The default value is 25. The maximum value is 100 	25, 1-100
#example:       ?max-results=25
        
#start-index:   Choose the first result to display in the returns. The first return is
#                       1. When used with the max-results parameter, multiple pages of results can be created.
#                       1, numeric value
#example:       ?start-index=26

#date: 	        Limit the returns to date range specified.	MMDDYYYY-MMDDYYYY
#example:       ?date=01011980-12311989

#sort:          Specifies the sort order for returns.	relevance, date_ascending, date_descending
#example:       ?sort=date_ascending

########################################################################################
#####################################     VIDEO     ####################################       
########################################################################################

#Requires parameters term ?term=
#Returns a list of videos for a specific search term.
def videoSearch(terms):
        VideoSearch = 'http://api.mtvnservices.com/1/video/search/'
        return videos

#Returns a single video by encoded ID.
def videoMethod(videoid):
        VideoMethod = 'http://api.mtvnservices.com/1/video/[video_id]/'
        return video

########################################################################################
#####################################     ARTIST    ####################################       
########################################################################################

#Returns content associated to a specific artist.
def artistAlias(artist):
        ArtistAlias = 'http://api.mtvnservices.com/1/artist/[artist_alias]/'
        return artist

#Returns videos associated to a specific artist.
def artistVideos(artist):
        #ArtistVideos = 'http://api.mtvnservices.com/1/artist/[artist_uri]/videos'
        #url = ArtistVideos.replace('[artist_uri]',artist)
        url = artist+'videos/'
        print url
        feed = feedparser.parse(url)
        videos = []
        for entry in  feed.entries:
                video = []
                video.append(entry.id)
                video.append(entry.title)
                video.append('')
                videos.append(video)
        return videos

#Requires parameters term ?term=
#Returns a list of artists for a specific search term.
def artistSearch(term):
        ArtistSearch = 'http://api.mtvnservices.com/1/artist/search/[parameters]'
        return artists

#Retrieves a list of artists sorted alphabetically.
# a-z and '-' for begining with numbers
def artistBrowse(letter):
        ArtistBrowse = 'http://api.mtvnservices.com/1/artist/browse/[alpha]'
        url = ArtistBrowse.replace('[alpha]',letter)
        feed = feedparser.parse(url)
        artists = []
        for entry in  feed.entries:
                artist = []
                artist.append(entry.id)
                artist.append(entry.title)
                artist.append('')
                artists.append(artist)
        return artists

#Returns a list of artists related to the specified artist.
def relatedArtist(artist):
        RelatedArtist = 'http://api.mtvnservices.com/1/artist/[artist_uri]/related/'
        return related

########################################################################################
#####################################     GENRE     ####################################       
########################################################################################

#Genre Alias            Genre Name
#world_reggae           World/Reggae
#pop                    Pop
#metal                  Metal
#environmental          Environmental
#latin                  Latin
#randb                  R&B
#rock                   Rock
#easy_listening         Easy Listening
#jazz                   Jazz
#country                Country
#hip_hop                Hip-Hop
#classical              Classical
#electronic_dance       Electronic / Dance
#blues_folk             Blues / Folk
#alternative            Alternative
#soundtracks_musicals   Soundtracks / Musicals

#Returns content links for a specified genre.
def genreAlias(genre):
        GenreAlias = 'http://api.mtvnservices.com/1/genre/[genre_alias]/'

#Returns a list of artists for a specified genre.
def genreArtists(genre):
        GenreArtists = 'http://api.mtvnservices.com/1/genre/[genre_alias]/artists/'
        url = GenreArtists.replace('[genre_alias]',genre)
        feed = feedparser.parse(url)
        artists = []
        for entry in  feed.entries:
                artist = []
                artist.append(entry.id)
                artist.append(entry.title)
                artist.append('')
                artists.append(artist)
        return artists

#Returns a list of videos for a specified genre.
def genreVideos(genre):
        GenreVideos = 'http://api.mtvnservices.com/1/genre/[genre_alias]/videos/'
        url = GenreVideos.replace('[genre_alias]',genre)
        feed = feedparser.parse(url)
        videos = []
        for entry in  feed.entries:
                video = []
                video.append(entry.id)
                video.append(entry.title)
                video.append('')
                videos.append(video)
        return videos

########################################################################################
####################################      RTMP      ####################################       
########################################################################################

def getrtmp(url):
        uridata = getURL(url)
        uri = re.compile('content url="(.+?)"').findall(uridata)[0]
        uri = uri.replace('http://media.mtvnservices.com/','')
        print uri
        smilurl = 'http://api-media.mtvnservices.com/player/embed/includes/mediaGen.jhtml?uri='+uri+'&vid='+uri.split(':')[4]+'&ref={ref}'
        smil = getURL(smilurl)
        rtmpurl = re.compile('<src>(.+?)</src>').findall(smil)[0]
        rtmpurl = rtmpurl.replace('rtmp://','')
        rtmpsplit = rtmpurl.split('/ondemand/')
        rtmphost = rtmpsplit[0]
        playpath = rtmpsplit[1].replace('.flv','')
        app = 'ondemand' 
        identurl = 'http://'+rtmphost+'/fcs/ident'
        ident = getURL(identurl)
        ip = re.compile('<fcs><ip>(.+?)</ip></fcs>').findall(ident)[0]
        rtmpurl = 'rtmp://'+ip+'/'+app+'?_fcs_vhost='+rtmphost
        rtmp = []
        rtmp.append(rtmpurl)
        rtmp.append(playpath)
        return rtmp

def getswfUrl():
        swfUrl = "http://media.mtvnservices.com/player/release/?v=3.9.0"
        return swfUrl
