## Scraper module
#-*- coding: utf-8 -*-

import os

try:
    import xbmc
    import xbmcgui
    # set scrapers path
    SCRAPER_PATH = os.path.join( os.getcwd(), "resources", "scrapers" )
except:
    # get dummy xbmc modules (Debugging)
    from debug import *
    xbmc = XBMC()
    xbmcgui = XBMCGUI()
    # set scrapers path
    SCRAPER_PATH = os.path.join( os.path.dirname( os.getcwd() ), "scrapers" )

import StringIO
import gzip
import urllib2
from urllib import quote_plus
import re
from unicodedata import normalize

# needs to be global as song and prefetched_song are two instances
artist_aliases = dict()


class Scraper:
    """
        Scrapes lyrics from internet sites using xml based scrapers.
    """

    def __init__( self, Addon, prefetch ):
        # set our Addon class
        self.Addon = Addon
        # our we prefetching
        self.prefetch = prefetch
        # regex's
        self.clean_song_regex = re.compile( "[\[\(]+.+?[\]\)]+" )# FIXME: do we want to strip inside ()?
        self.clean_br_regex = re.compile( "(<br>|<br />|<br/>)[\s]*" )
        self.clean_lyrics_regex = re.compile( "<.+?>" )
        self.clean_lrc_lyrics_regex = re.compile( "(^\[[0-9]+:[^\]]+\]\s)*(\[[0-9]+:[^\]]+\]$)*" )
        self.normalize_lyrics_regex = re.compile( "&#[x]*(?P<name>[0-9]+);*" )
        # get scraper info
        self._get_scraper_info()
        # get artist aliases, only need to grab it once
        if ( prefetch or self.Addon.getSetting( "prefetch_lyrics" ) != "true" ):
            self._alias_file()

    def fetch_lyrics( self, song ):
        # log message
        xbmc.log( "Scraper::fetch_lyrics             (artist=%s, title=%s, prefetch=%s)" % ( repr( song.artist ), repr( song.title ), repr( self.prefetch ), ), xbmc.LOGDEBUG )
        # sometimes you don't have internet
        if ( not xbmc.getCondVisibility( "System.InternetState" ) ):
            song.lyrics = self.Addon.getLocalizedString( 30851 ) % ( "No Internet connection!", )
            song.message = self.Addon.getLocalizedString( 30851 ) % ( "No Internet connection!", )
            song.status = False
            song.website = ""            
            return
        # variable to hold a new artist alias
        self.new_alias = dict()
        # used for aliases and song selection
        self.artist = song.artist
        self.title = song.title
        # fetch lyrics
        song.lyrics, song.message, song.status, song.website = self._fetch_lyrics_from_internet( self.artist, self.title )

    def _fetch_lyrics_from_internet( self, artist, title, songlist=False ):
        # initialize our variables
        scraper = 0
        lyrics = message = None
        status = False
        # loop until we have success or run out of scrapers
        while not status and scraper < len( self.SCRAPERS ):
            # fetch list if scraper only returns a list first or we found no lyrics
            if ( self.SCRAPERS[ scraper ][ "source" ][ "songlist" ][ "always" ] or songlist ):
                # initialize to None, so we don't try and fetch lyrics if we are prefetching
                url = None
                # do not interrupt user if prefetching
                if ( not self.prefetch or self.SCRAPERS[ scraper ][ "source" ][ "songlist" ][ "autoselect" ] ):
                    url, message = self._fetch_song_list( artist, scraper=scraper, usetitle=not songlist )
            else:
                url = artist
            # fetch lyrics
            if ( url is not None ):
                lyrics, message, status, website = self._fetch_lyrics( url, title, scraper=scraper )
            # increment scraper
            scraper += 1
        # if we succeeded or we are prefetching return results
        if ( status or self.prefetch ):
            return lyrics, message, status, website
        # we failed, try to fetch a songlist if we haven't already
        elif( not songlist ):
            return self._fetch_lyrics_from_internet( artist, title, songlist=True )
        # no artist was found, so get an alias
        else:
            # get artist alias
            self.new_alias = self._get_artist_alias( artist )
            # if user entered alias, try all over again
            if ( self.new_alias ):
                return self._fetch_lyrics_from_internet( self.new_alias[ self.artist ], title )
        # we failed all trys
        return self.Addon.getLocalizedString( 30851 ) % ( message, ), self.Addon.getLocalizedString( 30851 ) % ( message, ), False, ""

    def _fetch_lyrics( self, artist, title="", scraper=0 ):
        try:
            # log message
            xbmc.log( "  %s Scraper::_fetch_lyrics       (scraper=%s)" % ( [ "%d." % ( scraper + 1, ), "  " ][ artist.startswith( "http://" ) ], repr( self.SCRAPERS[ scraper ][ "title" ] ), ), xbmc.LOGDEBUG )
            # format url based on scraper if artist is not a url
            url = self._format_url( artist, title, scraper )
            # fetch source
            source = self._fetch_source( url, self.SCRAPERS[ scraper ][ "url" ][ "useragent" ], self.SCRAPERS[ scraper ][ "source" ][ "encoding" ] )
            # scrape and clean lyrics
            lyrics = self._scrape_lyrics( source, scraper )
            # save alias if we have one
            if ( self.new_alias ):
                self._alias_file( self.new_alias )
            # return results
            return lyrics, self.Addon.getLocalizedString( 30860 ), True, self.SCRAPERS[ scraper ][ "title" ]
        except Exception, e:
            # failure return None
            return None, str( e ), False, None

    def _scrape_lyrics( self, source, scraper ):
        # scrape lyrics
        lyrics = self.SCRAPERS[ scraper ][ "source" ][ "lyrics" ][ "regex" ].search( source ).group( 1 )
        # sometimes the lyrics are not human readable or poorly formatted
        if ( self.SCRAPERS[ scraper ][ "source" ][ "lyrics" ][ "clean" ] ):
            lyrics = self.clean_br_regex.sub( "\n", lyrics ).strip()
            lyrics = self.clean_lyrics_regex.sub( "", lyrics ).strip()
            lyrics = self.normalize_lyrics_regex.sub( lambda m: unichr( int( m.group( 1 ) ) ), lyrics ).encode( "utf-8", "replace" ).decode( "utf-8" )
            lyrics = u"\n".join( [ lyric.strip() for lyric in lyrics.splitlines() ] )
            # clean first and last blank lines for lrc lyrics
            if ( self.SCRAPERS[ scraper ][ "source" ][ "lyrics" ][ "type" ] == "lrc" ):
                lyrics = self.clean_lrc_lyrics_regex.sub( "", lyrics ).strip()
        # return result
        return lyrics

    def _fetch_song_list( self, artist, scraper=0, usetitle=False ):
        try:
            # log message
            xbmc.log( "  %d. Scraper::_fetch_song_list    (scraper=%s, autoselect=%s)" % ( scraper + 1, repr( self.SCRAPERS[ scraper ][ "title" ] ), repr( self.SCRAPERS[ scraper ][ "source" ][ "songlist" ][ "autoselect" ] ), ), xbmc.LOGDEBUG )
            # do we want to include title
            title = [ "", self.title ][ usetitle ]
            # format url based on scraper
            url = self._format_url( artist, title, scraper )
            # fetch source
            source = self._fetch_source( url, self.SCRAPERS[ scraper ][ "url" ][ "useragent" ], self.SCRAPERS[ scraper ][ "source" ][ "encoding" ] )
            # scrape song list
            songs = self.SCRAPERS[ scraper ][ "source" ][ "songlist" ][ "regex" ].findall( source )
            # raise an error if no songs found
            if ( not len( songs ) ): raise
            # get user selection
            url = self._get_song_selection( songs, self.SCRAPERS[ scraper ][ "source" ][ "songlist" ][ "swap" ], self.SCRAPERS[ scraper ][ "source" ][ "songlist" ][ "autoselect" ] )
            # if selection, format url
            if ( url is not None ):
                url = self.SCRAPERS[ scraper ][ "url" ][ "address" ] + url
            # return result
            return url, None
        # an error occurred, should only happen if artist was not found
        except Exception, e:
            # no artist found
            return None, str( e )

    def _get_song_selection( self, songs, swap, autoselect ):
        """ Returns a user selected song's url from a list of supplied songs """
        # sort songs, removing duplicates
        titles, dupes = self._sort_songs( songs, swap )
        # if autoselect, try to find a match
        if ( autoselect ):
            # set key
            if ( len( songs[ 0 ] ) == 3 ):
                # we use an artist alias if one was entered
                key = " - ".join( [ self.title, self.new_alias.get( self.artist, artist_aliases.get( self.artist, self.artist ) ) ] ).lower()
            else:
                key = self.title.lower()
            # loop thru and find a match FIXME: titles is sorted, so may not return best result?
            choice = [ count for count, k in enumerate( titles ) if ( k.lower() == key ) ]
            # if we have a match return it
            if ( choice ):
                return dupes[ titles[ choice[ 0 ] ] ]
        # if we are prefetching skip selection, we only go this far for autoselect scrapers
        if ( self.prefetch ):
            return None
        # set the time to auto close in msec, 90% of time remaining is plenty of time and gives prefetch some time
        autoclose = int( ( xbmc.Player().getTotalTime() - xbmc.Player().getTime() ) * 1000 * 0.90 )
        # get user selection
        choice = xbmcgui.Dialog().select( self.title, titles, autoclose )
        # return selection
        if ( choice >= 0 ):
            return dupes[ titles[ choice ] ]
        # log message only if no selection
        xbmc.log( "     Scraper::_get_song_selection (message='No selection made')", xbmc.LOGDEBUG )
        # no selection return None
        return None

    def _sort_songs( self, songs, swap ):
        """ Returns a sorted list with duplicates removed """
        # loop thru eliminating duplicates
        if ( swap ):
            dupes = dict( [ [ " - ".join( song[ 1 : ] ), song[ 0 ] ] for song in songs ] )
        else:
            dupes = dict( [ [ " - ".join( song[ 0 : -1 ] ), song[ -1 ] ] for song in songs ] )
        # we want the keys, this holds song title
        titles = dupes.keys()
        # sort list
        titles.sort()
        # return list of songs
        return titles, dupes

    def _get_artist_alias( self, artist ):
        # initialize alias
        alias = dict()
        # set the time to auto close in msec, 90% of time remaining is plenty of time and gives prefetch some time
        autoclose = int( ( xbmc.Player().getTotalTime() - xbmc.Player().getTime() ) * 1000 * 0.90 )
        # get keyboard object
        keyboard = xbmc.Keyboard( artist, self.Addon.getLocalizedString( 30810 ) % ( self.artist, ) )
        # show keyboard
        keyboard.doModal( autoclose )
        # set new alias from user input
        if ( keyboard.isConfirmed() ):
            alias = { self.artist: unicode( keyboard.getText(), "utf-8" ) }
        # log message
        xbmc.log( "     Scraper::_get_artist_alias   (artist=%s, new=%s)" % ( repr( self.artist ), repr( alias.get( self.artist, None ) ), ), xbmc.LOGDEBUG )
        # return result
        return alias

    def _format_url( self, artist, title, scraper ):
        # if we already have a url return it
        if ( artist.startswith( "http://" ) ): return artist
        # log message
        xbmc.log( "     Scraper::_format_url         (artist=%s, alias=%s, title=%s)" % ( repr( artist ), repr( artist_aliases.get( artist, self.new_alias.get( self.artist, None ) ) ), repr( title ), ), xbmc.LOGDEBUG )
        # get alias if there is one
        artist = artist_aliases.get( artist, self.new_alias.get( self.artist, self._format_item( artist, scraper ) ) )
        # only need to format title if it exists
        if ( title ):
            title = self._format_item( title, scraper ) + self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "title" ][ "tail" ]
        # add artist tail if no title
        else:
            artist += self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "artist" ][ "tail" ]
        # does the website subcategorize artists?
        if ( self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "artist" ][ "sub" ] ):
            # group numbers
            if ( "0-9" in self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "artist" ][ "group" ] and artist[ 0 ].isdigit() ):
                sub = "0-9"
            # group letters FIXME: probably not necessary
            elif ( "A-Z" in self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "artist" ][ "group" ] and artist[ 0 ].isalpha() ):
                sub = "A-Z"
            else:
                sub = artist[ 0 ].lower()
            # join sub and artist
            artist = self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "join" ].join( [ sub, artist ] )
        # join items together
        _search = [ artist, self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "join" ].join( [ artist, title ] ) ][ title != "" ]
        # return formatted url
        return self.SCRAPERS[ scraper ][ "url" ][ "address" ] + self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "search" ] + _search

    def _format_item( self, text, scraper ):
        # strip anything inside () or [] FIXME: maybe put back under clean
        text = self.clean_song_regex.sub( "", text ).strip()
        # clean text
        if ( self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "clean" ] ):
            # normalize text
            text = normalize( "NFKD", text ).encode( "ascii", "replace" )
            # remove bad characters
            text = "".join( [ char for char in text if char.isalnum() or char.isspace() or char == "/" ] )
        # format text
        if ( self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "case" ] == "lower" ):
            text = text.lower()
        elif ( self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "case" ] == "title" and not text.isupper() ):
            text = " ".join( [ word.capitalize() for word in text.split() ] )
        #elif ( self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "case" ] == "title" ):
        #    text = " ".join( [ [ word.capitalize(), word ][ word.isupper() ] for word in text.split() ] )
        # replace url characters with separator
        for char in " /":
            text = text.replace( char, self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "space" ] )
        # urlencode item
        if ( self.SCRAPERS[ scraper ][ "url" ][ "song" ][ "urlencode" ] ):
            text = quote_plus( text.encode( "utf-8" ) )
        # return result
        return text

    def _fetch_source( self, url, useragent, encoding="utf-8" ):
        # log message
        xbmc.log( "     Scraper::_fetch_source       (url=%s)" % ( repr( url ), ), xbmc.LOGDEBUG )
        # request url
        request = urllib2.Request( url )
        # add headers
        request.add_header( "User-Agent", useragent )
        request.add_header( "Accept", "text/html; charset=%s" % ( encoding, ) )
        request.add_header( "Accept-Encoding", "gzip" )
        # open requested url
        usock = urllib2.urlopen( request )
        # if gzipped, we need to unzip the source
        if ( usock.info().getheader( "Content-Encoding" ) == "gzip" ):
            source = gzip.GzipFile( fileobj=StringIO.StringIO( usock.read() ) ).read()
        else:
            source = usock.read()
        # close socket
        usock.close()
        # simple check for utf-8 FIXME: verify this works correctly, "Ã" seems to be right, but "â" may not be right â€™
        if ( source.find( "Ã" ) >= 0 or source.find( "â" ) >= 0 ):
            encoding = "utf-8"
        # return a unicode object
        return unicode( source, encoding, "replace" )

    def _alias_file( self, alias=dict() ):
        try:
            # needs to be global as song and prefetched_song are two instances
            global artist_aliases
            # create path to alias file
            _path = os.path.join( self.Addon.getAddonInfo( "Profile" ), "artist_aliases.txt" )
            # read/write aliases file
            if ( alias ):
                # update aliases
                artist_aliases.update( alias )
                # save aliases
                open( _path, "w" ).write( repr( artist_aliases ) )
            else:
                # read aliases
                artist_aliases = eval( open( _path, "r" ).read() )
        except Exception, e:
            # log message
            xbmc.log( "Scraper::_alias_file              (message='Missing or invalid alias file', path=%s)" % ( repr( _path ), ), xbmc.LOGDEBUG )
            # reset aliases
            artist_aliases = dict()

    def _get_scraper_info( self ):
        # unescape "&quot;", "&amp;", "&lt;", and "&gt;" in a string 
        def _unescape( text ):
            # return unescaped text
            return text.replace( "&amp;", "&" ).replace( "&lt;", "<" ).replace( "&gt;", ">" ).replace( "&quot;", "\"" )
        # initialize our scrapers list
        self.SCRAPERS = list()
        # get list of scrapers
        scrapers = os.listdir( SCRAPER_PATH )
        # scrapers regex
        scraper_regex = re.compile( "<scraper.+?title=\"([^\"]+)\".*?>\s[^<]+<url.+?address=\"([^\"]+)\".*?useragent=\"([^\"]+)\".*?>\s[^<]+<song.*?join=\"([^\"]*)\".*?space=\"([^\"]*)\".*?clean=\"([^\"]*)\".*?case=\"([^\"]*)\".*?search=\"([^\"]*)\".*?urlencode=\"([^\"]*)\".*?>\s[^<]+<artist.+?tail=\"([^\"]*)\".*?sub=\"([^\"]*)\".*?group=\"([^\"]*)\".*?/>\s[^<]+<title.+?tail=\"([^\"]*)\".*?/>\s[^<]+</song>\s[^<]+</url>\s[^<]+<source.+?encoding=\"([^\"]*)\".*?>\s[^<]+<lyrics.+?type=\"([^\"]*)\".*?clean=\"([^\"]*)\".*?>\s[^<]+<regex.+?flags=\"([^\"]*)\".*?>([^<]+)</regex>\s[^<]+</lyrics>\s[^<]+<songlist.+?swap=\"([^\"]*)\".*?always=\"([^\"]*)\".*?select=\"([^\"]*)\".*?>\s[^<]+<regex.+?flags=\"([^\"]*)\".*?>([^<]+)</regex>\s[^<]+</songlist>", re.IGNORECASE )
        # re flags
        regex_flags = {
            "dotall": re.DOTALL,
            "ignorecase": re.IGNORECASE,
            "multiline": re.MULTILINE,
        }
        # loop thru and set our info
        for scraper in scrapers:
            # is this scraper enabled?
            if ( not scraper.endswith( ".xml" ) or ( scraper.replace( ".xml", "" ) != self.Addon.getSetting( "primary_scraper" ) and self.Addon.getSetting( "scraper_%s" % ( scraper.replace( ".xml", "" ).replace( "-", "_" ).lower(), ) ) == "false" ) ): continue
            # set full path to file
            _path = os.path.join( SCRAPER_PATH, scraper )
            # skip any malformed scrapers
            try:
                # get scrapers xml source
                xmlSource = unicode( open( _path, "r" ).read(), "utf-8" )
                # get info
                info = scraper_regex.search( xmlSource ).groups()
                # create scraper
                tmp_scraper = {
                    "title": info[ 0 ],
                    "url": {
                        "address": info[ 1 ],
                        "useragent": _unescape( info[ 2 ] ),
                        "song": {
                            "join": info[ 3 ],
                            "space": info[ 4 ],
                            "clean": info[ 5 ] == "true",
                            "case": info[ 6 ],
                            "search": _unescape( info[ 7 ] ),
                            "urlencode": info[ 8 ] == "true",
                            "artist": {
                                "tail": info[ 9 ],
                                "sub": info[ 10 ] == "true",
                                "group": info[ 11 ],
                            },
                            "title": {
                                "tail": info[ 12 ],
                            },
                        },
                    },
                    "source": {
                        "encoding": info[ 13 ],
                        "lyrics": {
                            "type": info[ 14 ],
                            "clean": info[ 15 ] == "true",
                            "regex": re.compile( _unescape( info[ 17 ] ), sum( [ regex_flags[ flag ] for flag in info[ 16 ].split() ] ) ),
                        },
                        "songlist": {
                            "swap": info[ 18 ] == "true",
                            "always": info[ 19 ] == "true",
                            "autoselect": info[ 20 ] == "auto",
                            "regex": re.compile( _unescape( info[ 22 ] ), sum( [ regex_flags[ flag ] for flag in info[ 21 ].split() ] ) ),
                        },
                    },
                }
                # we want the primary scraper first
                if ( scraper.replace( ".xml", "" ) == self.Addon.getSetting( "primary_scraper" ) ):
                    self.SCRAPERS.insert( 0, tmp_scraper )
                else:
                    self.SCRAPERS.append( tmp_scraper )
            # an invalid scraper file, skip it
            except Exception, e:
                # log error
                xbmc.log( "Invalid scraper file! - %s (%s)" % ( scraper, e, ), xbmc.LOGERROR )


if ( __name__ == "__main__" ):
    songno = 0
    artists = [ u"ABBA", u"AC/DC", u"Blue Öyster Cult", u"The Rolling Stones (feat. Cheryl Crow)", u"38 Special", u"ABBA", u"Enya", u"Enya", u"*NSync", u"Enya", u"ABBA" ]
    songs = [ u"Eagle", u"Have a Drink on Me", u"Isn't it Time", u"Wild Horses [Live]", u"Hold on Loosely", u"Eagle", u"Aniron (I Desire)", u"Book of Days", u"Bye Bye Bye", u"Orinoco Flow", u"S.O.S." ]

    class SONG:
        artist = artists[songno]
        title = songs[songno]
    _song = SONG()

    scraper = Scraper( Addon=XBMCADDON().Addon( "python.testing" ), prefetch=False )
    scraper.fetch_lyrics( _song )
    print [ _song.status, repr( _song.message ), repr(_song.website) ]
    print
    for lyric in _song.lyrics.splitlines():
        print repr(lyric)
