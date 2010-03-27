__plugin__  = "KollectiONX"
__author__  = "Brian Millham <brian@millham.net>"
__url__     = ""
__date__    = "26 March 2010"
__version__ = "0.4"
__svn_revision__ = "$Revision:$"
__XBMC_Revision__ = "19457"

import urllib
import re
import xbmc
import xbmcplugin
import xbmcgui
import MovieSQL
import SQL
import mydialog
import sys

platform=sys.platform

limit = [100, 250, 500, 750, 1000, 1500, 2000]
movie_limit = limit[int(xbmcplugin.getSetting('maxmoviecount'))]

MOVIE_LINK_LIST=5
GENRE_TOGGLE=100
BY_GENRE=11
FILTERED=13
UNFILTERED=10
BY_ACTOR=12
BY_YEAR=14
BY_DIRECTOR=15
BY_STUDIO=16
BY_WRITER=17
GENRE_FILTER=50
MOVIES_BY_GENRE=21
ACTOR_LETTER_LIST=22
MOVIES_BY_ACTOR=32
MOVIES_BY_YEAR=24
MOVIES_BY_DIRECTOR=25
MOVIES_BY_STUDIO=26
MOVIES_BY_WRITER=27
MOVIES_BY_LETTER=28
PLAY_ALL_LINKS=30061
PLAY_RANDOM_LINK=30062
PLAY_ALL_RANDOM_LINKS=30063

MainMenu = {xbmc.getLocalizedString(30050): FILTERED, #Filtered
            #xbmc.getLocalizedString(30051): UNFILTERED, # Unfiltered
            xbmc.getLocalizedString(30052): BY_ACTOR, # Actor
            xbmc.getLocalizedString(30053): BY_GENRE, # Genre
            xbmc.getLocalizedString(30054): BY_YEAR, # Year
            xbmc.getLocalizedString(30055): BY_DIRECTOR, # Director
            xbmc.getLocalizedString(30056): BY_STUDIO, # Studio
            xbmc.getLocalizedString(30057): BY_WRITER, # Writer
            xbmc.getLocalizedString(30060): GENRE_FILTER # Genre Filter selection
            }

MyName=xbmc.getLocalizedString(32001)
filter_list = []
if xbmcplugin.getSetting('genreignore') != '':
   filter_list=xbmcplugin.getSetting('genreignore').split(",")

def fixUrl(url):
      if url == '':
        return ''

      r = re.compile('\\\\')
      myfile = r.sub('/', url)
      myfile1 = ''
      l = url.split(':')
      if len(l) == 2:
          myfile1 = myfile
      else:
          myfile1 = "smb:" + myfile
      return(str(myfile1))

def fixHtml(html):
    if html == '': return ''

    r = re.compile('<(b|B)>')
    html = r.sub('[B]', html)
    r = re.compile('</(b|B)>')
    html = r.sub('[/B]', html)
    r = re.compile('<(i|I)>')
    html = r.sub('[I]', html)
    r = re.compile('</(i|I)>')
    html = r.sub('[/I]', html)
    r = re.compile('<.?(p|P)>')
    html = r.sub('[CR]', html)
    r = re.compile('<(.?(l|L)(i|I))>')
    html = r.sub('[CR]', html)
    r = re.compile('<.*?>')
    html = r.sub('', html)
    return html

def mainMenu():
    for k in sorted(MainMenu):
        if MainMenu[k]==GENRE_FILTER:
            u=sys.argv[0]+ \
             "?mode="+str(GENRE_FILTER)+ \
             "&name="+urllib.quote_plus(k)
            liz=xbmcgui.ListItem(k, 
             iconImage="DefaultVideo.png",
             thumbnailImage="DefaultVideo.png")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
             url=u,listitem=liz)
        else:
            addDir(0, name=k, mode=MainMenu[k])

def genreList():
    (results, totalcount) = db.getGenreList()
    for row in results:
        
        if str(row["genreid"]) in filter_list:
            filter = "[Filtered]"
        else:
            filter = ''
        g = " (%d) %s" % (row["MovieCount"], filter)
        addDir(row["GenreID"],
               name=row['displayname'],
               details = g,
               mode=MOVIES_BY_GENRE,
               totalcount=totalcount)


def actorLetterList(letter):
    (results, totalcount) = db.getActorsByLetter(letter)
    for row in results:
        a = "%s (%d)" % (row["ActorName"], row["MovieCount"])
        addDir(row["ActorID"],
               name=a,
               mode=MOVIES_BY_ACTOR,
               totalcount=totalcount)

def actorList():
    (results, totalcount) = db.getActorLetterList()
    for row in results:
        a = "%s (%d)" % (row["letter"], row["letter_count"])
        addDir(row["letter"],
               name=a,
               mode=ACTOR_LETTER_LIST,
               totalcount=totalcount)

def studioList():
    (results, totalcount) = db.getStudioList()
    for row in results:
        s = "%s (%d)" % (row["DisplayName"], row["MovieCount"])
        addDir(row["StudioID"],
               name=s,
               mode=MOVIES_BY_STUDIO,
               totalcount=totalcount)

def directorList():
    (results, totalcount) = db.getDirectorList()
    for row in results:
        d = "%s (%d)" % (row["DirectorName"], row["MovieCount"])
        addDir(row["DirectorID"],
               name=d,
               mode=MOVIES_BY_DIRECTOR,
               totalcount=totalcount)

def writerList():
    (results, totalcount) = db.getWriterList()
    for row in results:
        d = "%s (%d)" % (row["WriterName"], row["MovieCount"])
        addDir(row["WriterID"],
               name=d,
               mode=MOVIES_BY_WRITER,
               totalcount=totalcount)
        
def yearList():
    (results, totalcount) = db.getYearList()
    for row in results:
         if row["MovieReleaseYear"] != None:
            mry = "%d (%d)" % (row["DisplayName"], row["MovieCount"])
            y = row["MovieReleaseYear"]
            addDir(y,
                   name=mry,
                   mode=MOVIES_BY_YEAR,
                   totalcount=totalcount)

def movieLetterList(clause):
    (results, totalcount) = db.runSQL(SQL.MOVIE_LETTER_LIST % clause)
    for row in results:
        name = "%s (%d)" % (row['letter'], row['lettercount'])
        addDir(row['letter'],
          name=name,
          mode=MOVIES_BY_LETTER,
          totalcount=totalcount)

def movieList(sql, clause='', nomax=False):
        (mcount, mtotal) = db.runSQL(SQL.MOVIE_COUNT % clause, True)
        limit=int(xbmcplugin.getSetting('maxmoviecount'))
        print "Movie count setting: %s" % xbmcplugin.getSetting('maxmoviecount')
        print "Movie count: %d" % mcount['movie_count']
        print "Movie limit: %d, momax: %d" % (movie_limit, nomax)
        if mcount['movie_count'] > movie_limit and not nomax:
            movieLetterList(clause)
        else:
            (results, totalcount) = db.runSQL(sql % clause)
	    for row in results:
	      if row["movieurl"] == "":
	        addDir(row["movieid"],
                 name=row["title"],
                 mode=MOVIE_LINK_LIST,
                 iconimage=fixUrl(row["frontcover"]),
                 totalcount=totalcount,
                 row=row)
	      else:
                addLink(row, totalcount)
        #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
        #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
        #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
                
def linkList(movieid):
        (moviedetails, moviecount) = db.runSQL(SQL.SINGLE_MOVIE % movieid, True)
        (results, totalcount) = db.runSQL(SQL.MOVIE_LINKS % movieid)

        u=sys.argv[0]+ \
          "?mode="+str(PLAY_ALL_LINKS)+ \
          "&movieid="+str(movieid)
        print "U: " + u
        l = xbmcgui.ListItem(xbmc.getLocalizedString(30061),
             iconImage='DefaultFolder.png',
             thumbnailImage=fixUrl(moviedetails["FrontCover"]))
        l.setInfo(type="Video", infoLabels={
              "TVShowTitle": moviedetails["Title"],
              "Title": xbmc.getLocalizedString(30061),
              "Plot": fixHtml(moviedetails["Plot"])})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, l, False)

        for link in results:
            l = xbmcgui.ListItem(link["Description"],
                 iconImage="DefaultFolder.png",
                 thumbnailImage=fixUrl(moviedetails["FrontCover"]))
            l.setInfo(type="Video", infoLabels={
              "TVShowTitle": moviedetails["Title"],
              "Title": link["Description"],
              "Plot": fixHtml(moviedetails["Plot"])})
            print "Adding link: " + link["URL"]
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), fixUrl(link["URL"]), l, False, totalcount)

def playLinks(mode, movieid):
    (moviedetails, moviecount) = db.runSQL(SQL.SINGLE_MOVIE % movieid, True)
    if mode==PLAY_ALL_LINKS:
        query = SQL.MOVIE_LINKS
    elif mode==PLAY_RANDOM_LINK:
        query = SQL.RANDOM_MOVIE_LINK
    elif mode==PLAY_ALL_RANDOM_LINKS:
        query = SQL.ALL_RANDOM_MOVIE_LINKS

    (results, totalcount) = db.runSQL(query % movieid)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()

    for link in results:
       l = xbmcgui.ListItem(link["Description"],
            iconImage="DefaultFolder.png",
            thumbnailImage=fixUrl(moviedetails["FrontCover"]))
       l.setInfo(type="Video", infoLabels={
         "TVShowTitle": moviedetails["Title"],
         "Title": link["Description"],
         "Plot": fixHtml(moviedetails["Plot"])})
       playlist.add(url=fixUrl(link['url']), listitem=l)

    xbmc.Player().play(playlist)

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

def createInfoLabels(row, castandrole=None, cast=None, genre_list=None, director_list=None, writer_list=None, studio_list=None):
    infolabels = {}
    if row == None: return infolabels
    infolabels["Title"] = row["title"]
    infolabels["Plot"] = fixHtml(row["plot"])
    #if cast: infolabels["Cast"] = cast
    if castandrole: infolabels['castandrole'] = castandrole
    if genre_list: infolabels["Genre"] = ", ".join(genre_list)
    if director_list: infolabels["Director"] = ", ".join(director_list)
    if writer_list: infolabels["Writer"] = ", ".join(writer_list)
    infolabels["Duration"] = str(row["runningtime"])
    if studio_list: infolabels["Studio"] = ", ".join(studio_list)
    if row["audiencerating"] != None:
        infolabels["mpaa"] = row["audiencerating"]
    if row["IMDbRating"] != '':
        try:
            infolabels["Rating"] = float(row["imdbrating"].split(" ")[0])
        except:
            pass
    if row["year"] != None:
        infolabels["Year"] = row["year"]
    return infolabels

def createContextMenuUrl(type, movieid):
    uplayall=sys.argv[0]+ \
        "?mode="+str(type)+ \
        "&movieid="+str(movieid)
    return 'XBMC.RunPlugin('+uplayall+')'

def addLink(row, totalcount):
        actors = db.getActorsByMovie(row['movieid'])
        castandrole = getList(actors, "ActorAsPart")
        cast = getList(actors, "label1")
        genre_list = getList(db.getGenresByMovie(row["movieid"]), "DisplayName")
        director_list = getList(db.getDirectorsByMovie(row["movieid"]), "DisplayName")
        writer_list = getList(db.getWritersByMovie(row["movieid"]), "DisplayName")
        studio_list = getList(db.getStudiosByMovie(row["movieid"]), "DisplayName")

        name = row["title"]
        url = fixUrl(row["movieurl"])
        iconimage = fixUrl(row["frontcover"])

        liz=xbmcgui.ListItem(name,
         iconImage="DefaultVideo.png",
         thumbnailImage=iconimage)
        liz.setInfo( type="Video",
         infoLabels=createInfoLabels(row, castandrole=castandrole,
          cast=cast, genre_list=genre_list, director_list=director_list,
          writer_list=writer_list, studio_list=studio_list))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
         url=url,listitem=liz,
         totalItems=totalcount)
        return ok


def addDir(movieid=0,
           name=None,
           details=None,
           url='none',
           mode=0,
           iconimage="DefaultVideo.png",
           totalcount=0,
           row=None):
        u=sys.argv[0]+ \
          "?url="+urllib.quote_plus(url)+ \
          "&mode="+str(mode)+ \
          "&name="+urllib.quote_plus(name)+ \
          "&movieid="+str(movieid)

        fullname = name
        if details != None: fullname += details
        liz=xbmcgui.ListItem(fullname,
                             iconImage = "DefaultFolder.png",
                             thumbnailImage = iconimage)
        if row: liz.setInfo( type="Video", infoLabels=createInfoLabels(row))
        if row != None:
            liz.addContextMenuItems([
              (xbmc.getLocalizedString(PLAY_ALL_LINKS),
               createContextMenuUrl(PLAY_ALL_LINKS, movieid),),
               (xbmc.getLocalizedString(PLAY_RANDOM_LINK),
               createContextMenuUrl(PLAY_RANDOM_LINK, movieid),),
               (xbmc.getLocalizedString(PLAY_ALL_RANDOM_LINKS),
               createContextMenuUrl(PLAY_ALL_RANDOM_LINKS, movieid),)
               ], False)
        if mode == MOVIES_BY_GENRE:
            if str(movieid) in filter_list:
                text = "Remove filter for %s" % name
                ufilter="%s?mode=%d&movieid=%d" % (sys.argv[0],
                                                   GENRE_TOGGLE,
                                                   movieid)
            else:
                text = "Add filter for %s" % name
                ufilter="%s?mode=%d&movieid=%d" % (sys.argv[0],
                                                   GENRE_TOGGLE,
                                                   movieid)
            liz.addContextMenuItems([(text,
              'XBMC.RunPlugin('+ufilter+')',)], True)
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                       url=u,
                                       listitem=liz,
                                       isFolder=True,
                                       totalItems=totalcount)
        return ok
        
def getList((results, totalcount), field):
    list = []
    for row in results:
        r = row[field.lower()]
        list.append(r)
    return list

params=getParams()
url=None
name=None
mode=None
movieid=None

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
try:
        movieid=params["movieid"]
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "MovieID: "+str(movieid)
print "Platform: %s" % platform

db = MovieSQL.MovieSQL()

if mode == None:
    db.connect(host=xbmcplugin.getSetting('mysqlhost'),
             port=int(xbmcplugin.getSetting('mysqlport')),
             user=xbmcplugin.getSetting('mysqluser'),
             passwd=xbmcplugin.getSetting('mysqlpassword'),
             db=xbmcplugin.getSetting("mysqldatabase"),
             nowait=1)
else: #and mode != MainMenu["Genre Filter"]:
  constat = 0
  while constat != 1:
      constat = db.connect(host=xbmcplugin.getSetting('mysqlhost'),
             port=int(xbmcplugin.getSetting('mysqlport')),
             user=xbmcplugin.getSetting('mysqluser'),
             passwd=xbmcplugin.getSetting('mysqlpassword'),
             db=xbmcplugin.getSetting("mysqldatabase"))
      if constat == 1: break
      if constat == 0:
          ans = xbmcgui.Dialog().yesno(MyName,
            xbmc.getLocalizedString(32003),
            xbmc.getLocalizedString(32004),
            xbmc.getLocalizedString(32005))
          if ans == False:
              break
          xbmcplugin.openSettings(url=sys.argv[0])
      if constat == -1:
          xbmcgui.Dialog().ok(MyName,
            xbmc.getLocalizedString(32002))
          break

if mode==GENRE_FILTER:

    mydialog.MyDialog(db.getGenreList())

if mode==None or not db.isConnected():
        mainMenu()
elif mode==UNFILTERED or (mode==FILTERED and xbmcplugin.getSetting('genreignore') == ''):
    movieList(SQL.ALL_MOVIES)
elif mode==BY_GENRE:
    genreList()
elif mode==BY_ACTOR:
    actorList()
elif mode==BY_YEAR:
    yearList()
elif mode==FILTERED and xbmcplugin.getSetting('genreignore') != '':
    movieList(SQL.ALL_MOVIES, clause=SQL.IGNORE_GENRE_WHERE % xbmcplugin.getSetting('genreignore'))
elif mode==BY_DIRECTOR:
    directorList()
elif mode==BY_STUDIO:
    studioList()
elif mode==BY_WRITER:
    writerList()
elif mode==MOVIES_BY_GENRE:
    movieList(SQL.ALL_MOVIES, clause=SQL.GENRE_WHERE % movieid, nomax=True)
elif mode==ACTOR_LETTER_LIST:
    actorLetterList(movieid)
elif mode==MOVIES_BY_ACTOR:
    movieList(SQL.ALL_MOVIES, clause=SQL.ACTOR_WHERE % movieid)
elif mode==MOVIES_BY_YEAR:
    movieList(SQL.ALL_MOVIES, clause=SQL.YEAR_WHERE % int(movieid))
elif mode==MOVIES_BY_DIRECTOR:
    movieList(SQL.ALL_MOVIES, clause=SQL.DIRECTOR_WHERE % movieid)
elif mode==MOVIES_BY_STUDIO:
    movieList(SQL.ALL_MOVIES, clause=SQL.STUDIO_WHERE % movieid)
elif mode==MOVIES_BY_WRITER:
    movieList(SQL.ALL_MOVIES, clause=SQL.WRITER_WHERE % movieid)
elif mode==MOVIES_BY_LETTER:
    if len(filter_list) == 0:
        f = '-1'
    else:
        f = ",".join(filter_list)
    if movieid == '.': movieid = '\\\\.'
    lclause = SQL.MOVIE_BY_LETTER % (f, movieid)
    print "Clause: %s" % lclause
    movieList(SQL.ALL_MOVIES, clause=lclause, nomax=True)
elif mode==PLAY_ALL_LINKS or mode==PLAY_RANDOM_LINK or mode==PLAY_ALL_RANDOM_LINKS:
    playLinks(mode, movieid)
elif mode==GENRE_TOGGLE:
    if str(movieid) in filter_list:
        filter_list.remove(movieid)
    else:
        filter_list.append(movieid)
    xbmcplugin.setSetting('genreignore', ",".join(filter_list))
    xbmc.executebuiltin('Container.Refresh')
elif mode==MOVIE_LINK_LIST:
    linkList(movieid)

if mode != GENRE_FILTER and mode != GENRE_TOGGLE:
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
