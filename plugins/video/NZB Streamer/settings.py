import xbmcplugin

#Not used anymore - Enter your username and password in the plugin options
#username_newzbin = ''
#password_newzbin = ''

category_list = ['default','Unknown', 'Anime', 'Apps', 'Books', 'Consoles', 'Emulation', 'Games',
        'Misc', 'Movies', 'Music', 'PDA', 'Resources', 'TV']

'''
dictionary containing the names and RSS feeds for the initial page, feel free to add your own.
The '#' character is a comment in python, delete it to use commented out feeds
'''
#if you use newzbin, add custom rss feeds here
newzbin_rss = [
{'name':'Newzbin - Search', 'url':'http://www.newzbin.com/search/query/?q=%s&area=-1&fpn=p&searchaction=Go&areadone=-1&feed=rss'},
{'name':'Newzbin - TV (Latest)', 'url':'http://www.newzbin.com/browse/category/p/tv/?feed=rss'}, 
{'name':'Newzbin - Movies (Latest)', 'url':'http://www.newzbin.com/browse/category/p/movies/?feed=rss'},
{'name':'Newzbin - Music (Latest)', 'url':'http://www.newzbin.com/browse/category/p/music/?feed=rss'},
#{'name':'Newzbin - Games (Latest)', 'url':'http://www.newzbin.com/browse/category/p/games/?feed=rss'},
#{'name':'Newzbin - Consoles (Latest)', 'url':'http://www.newzbin.com/browse/category/p/consoles/?feed=rss'},
]

binsearch_rss = [
#{'name':'Binsearch - Search', 'url':'http://binsearch.info/index.php/?q=%s&m=&max=250&minsize=0&maxsize=&font=&postdate=&hideposter=on&hidegroup=on'},
{'name':'Binsearch - TV (Latest)', 'url':'http://rss.binsearch.net/rss.php?max=50&g=alt.binaries.multimedia', 'category':'tv'},
{'name':'Binsearch - Movies Divx (Latest)', 'url':'http://rss.binsearch.net/rss.php?max=50&g=alt.binaries.movies.divx', 'category':'movies'},
]

tvnzb_rss = [
{'name':'TVNZB (Latest)', 'url':'http://tvnzb.com/tvnzb_new.rss', 'category':'tv'},
]
'''nzbsrus_rss = [
{'name':'NZBSRUS (Latest)', 'url':'http://www.nzbsrus.com/rssfeed.php'},
]'''
nzbindex_rss = [
{'name':'NZBIndex - Search', 'url':'http://www.nzbindex.nl/rss/?searchitem=%s&x=0&y=0&age=365&group=&min_size=100&max_size=&poster='},
]

""" ADD CUSTOM RSS FEEDS HERE """
#add other rss feeds here, just copy an existing one and change the name and url
other_rss = [

]

#sabnzbd_rss = [
#{'name':'SABnzbd - Queue', 'url':''}, #leave the url blank for this one
#]

#ignore below
rss_dict = []
if xbmcplugin.getSetting( "newzbin_show" ) == "true":
    rss_dict.extend(newzbin_rss)
if xbmcplugin.getSetting( "binsearch_show" ) == "true":
    rss_dict.extend(binsearch_rss)
if xbmcplugin.getSetting( "tvnzb_show" ) == "true":
    rss_dict.extend(tvnzb_rss)
'''if xbmcplugin.getSetting( "nzbsrus_show" ) == "true":
    rss_dict.extend(nzbsrus_rss)'''
if xbmcplugin.getSetting( "nzbindex_show" ) == "true":
    rss_dict.extend(nzbindex_rss)
if xbmcplugin.getSetting( "custom_show" ) == "true":
    rss_dict.extend(other_rss)
#rss_dict.extend(sabnzbd_rss)

