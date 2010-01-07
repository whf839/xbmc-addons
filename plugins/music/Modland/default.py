import sys
import urllib, cgi, xml.dom.minidom
import xbmc, xbmcgui, xbmcplugin

# plugin constants
__plugin__     = "Modland"
__author__     = 'BuZz [buzz@exotica.org.uk] / http://www.exotica.org.uk'
__svn_url__    = "http://xbmc-addons.googlecode.com/svn/trunk/plugins/music/modland"
__version__    = "2010-01-06"

MODLAND_URL = 'http://www.exotica.org.uk/mediawiki/extensions/ExoticASearch/Modland_xbmc.php'
#MODLAND_URL = 'http://exotica.travelmate/mediawiki/extensions/ExoticASearch/Modland_xbmc.php'

handle = int(sys.argv[1])

def get_params(defaults):
  new_params = defaults
  params = cgi.parse_qs(sys.argv[2][1:])
  for key, value in params.iteritems():
    new_params[key] = urllib.unquote_plus(params[key][0])
  return new_params

def show_options():
  url =  sys.argv[0] + '?' + urllib.urlencode( { 'mode': 'search' } )
  li = xbmcgui.ListItem( label = 'Search for game/demo music on Modland')
  ok = xbmcplugin.addDirectoryItem(handle, url, listitem = li, isFolder = True)
  xbmcplugin.endOfDirectory(handle, succeeded = True)

def get_search():
  kb = xbmc.Keyboard('', 'Enter search string')
  kb.doModal()
  if not kb.isConfirmed():
    return None
  search = kb.getText()
  return search

def get_results(search):

  url = MODLAND_URL + '?' + urllib.urlencode( { 'qs': search } )

  response = urllib.urlopen(url)
  resultsxml = response.read()
  response.close

  dom = xml.dom.minidom.parseString(resultsxml)
  items = dom.getElementsByTagName("item")
  count = items.length
  for item in items:
    title = item.getElementsByTagName("title")[0].firstChild.data
    artist = item.getElementsByTagName("author")[0].firstChild.data
    format = item.getElementsByTagName("format")[0].firstChild.data
    stream_url = item.getElementsByTagName("url")[0].firstChild.data
    
    label = title + ' - ' + artist + ' - ' + format

    li = xbmcgui.ListItem( label )
    li.setInfo( type = 'music', infoLabels = { 'title': label, 'genre': format, 'artist': artist } )
    url = sys.argv[0] + '?'
    url += urllib.urlencode( { 'mode': 'play', 'title': title, 'artist': artist, 'genre': format, 'url': stream_url } )
    ok = xbmcplugin.addDirectoryItem(handle, url = url, listitem = li, isFolder = False, totalItems = count)

  xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_TITLE)
  xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_ARTIST)
  xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_GENRE)
  xbmcplugin.endOfDirectory(handle = handle, succeeded = True)

def play_stream(url, title, info):
  listitem = xbmcgui.ListItem(title)
  listitem.setInfo ( 'music', info )
  player = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
  player.play(url, listitem)

params = get_params( { 'mode': None } )
mode = params["mode"]

if mode == None:
  show_options()
  
elif mode == 'search':
  search = get_search()
  if search != None and len(search) >= 3:
    get_results(search)
  else:
    show_options()

elif mode == 'play':
  title = urllib.unquote_plus(params['title'])
  artist = urllib.unquote_plus(params['artist'])
  genre = urllib.unquote_plus(params['genre'])
  url = urllib.unquote_plus(params['url'])

  info = { 'title': title, 'artist': artist, 'genre': genre }
  play_stream(url, title, info)
