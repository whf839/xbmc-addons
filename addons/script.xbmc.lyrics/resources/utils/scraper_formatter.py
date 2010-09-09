MAINTAINER = "nuka1195"
EMAIL = ""
DATE = "2010.07.01"
TITLE = "LyricsMode"
BASE_URL = "http://www.lyricsmode.com/lyrics/"
USERAGENT = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"
SONG_JOIN_CHAR = "/"
SONG_SPACE_CHAR = "_"
SONG_CLEAN = [ "false", "true" ][ 1 ]
SONG_CASE = [ "", "lower", "title" ][ 1 ]
SONG_SEARCH_HEAD=""
SONG_URLENCODE = [ "false", "true" ][ 0 ]
ARTIST_TAIL = "/"
ARTIST_SUB = [ "false", "true" ][ 1 ]
ARTIST_GROUP = [ "", "0-9", "A-Z" ][ 1 ]
TITLE_TAIL = ".html"
SOURCE_ENCODING = "iso-8859-1"
LYRICS_TYPE = [ "standard", "lrc" ][ 0 ]
LYRICS_CLEAN = [ "false", "true" ][ 1 ]
LYRICS_REGEX_FLAGS = " ".join( [ "dotall", "ignorecase", "multiline" ][ 0 : 2 ] )
LYRICS_REGEX = "<div.+?id='songlyrics_h'.+?class='dn'>(.+?)</div>"
SONGLIST_SWAP = [ "false", "true" ][ 1 ]
SONGLIST_ALWAYS = [ "false", "true" ][ 0 ]
SONGLIST_SELECT = [ "manual", "auto" ][ 0 ]
SONGLIST_REGEX_FLAGS = " ".join( [ "dotall", "ignorecase", "multiline" ][ 1 : 2 ] )
SONGLIST_REGEX = "<a.+?href=\"/lyrics/([^\"]+)\".+?title=\"[^\"]+\">(.+?) lyrics[^<]*</a>"

#############################################################################################################

def _escape( text ):
    # return unescaped text
    return text.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" ).replace( "\"", "&quot;" )

xml = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<!--Maintainer: %s-->
<!--Email: %s-->
<!--Date: %s-->
<scraper title="%s">
    <url address="%s" useragent="%s">
        <song join="%s" sep="%s" clean="%s" case="%s" search="%s" urlencode="%s">
            <artist tail="%s" sub="%s" group="%s"/>
            <title tail="%s"/>
        </song>
    </url>
    <source encoding="%s">
        <lyrics type="%s" clean="%s">
            <regex flags="%s">%s</regex>
        </lyrics>
        <songlist swap="%s" always="%s" select="%s">
            <regex flags="%s">%s</regex>
        </songlist>
    </source>
</scraper>
"""
open ( TITLE + ".xml", "w" ).write( xml % ( MAINTAINER, EMAIL, DATE, TITLE, BASE_URL, _escape( USERAGENT ), SONG_JOIN_CHAR, SONG_SPACE_CHAR, SONG_CLEAN, SONG_CASE, _escape( SONG_SEARCH_HEAD ), SONG_URLENCODE, ARTIST_TAIL, ARTIST_SUB, ARTIST_GROUP, TITLE_TAIL, SOURCE_ENCODING, LYRICS_TYPE, LYRICS_CLEAN, LYRICS_REGEX_FLAGS, _escape( LYRICS_REGEX ), SONGLIST_SWAP, SONGLIST_ALWAYS, SONGLIST_SELECT, SONGLIST_REGEX_FLAGS, _escape( SONGLIST_REGEX ), ) )

print "Saved %s.xml in current directory" % ( TITLE, )