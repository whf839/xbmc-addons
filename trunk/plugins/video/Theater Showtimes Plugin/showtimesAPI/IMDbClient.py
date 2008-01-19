"""
IMDb api client module

Nuka1195
"""

import sys
import os

if ( __name__ != "__main__" ):
    import xbmc

import urllib
import re
from htmllib import HTMLParser


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class _IMDBParser:
    """ 
        Parser Class: parses an html document for movie info
    """
    # HTML cleaning regex pattern
    pattern_clean = re.compile( '<.+?>' )

    # IMDb regex patterns
    pattern_title = re.compile( '<meta name="title" content="([^"]*) \(([0-9]*)\)' )
    pattern_year = re.compile( 'a href="/Sections/Years/([0-9]*)">' )
    pattern_top250 = re.compile( 'Top 250: #([0-9]*)</a>' )
    pattern_user_rating = re.compile( '<b>User Rating:</b>[^<]*<b>([0-9.]+)/10</b>[^<]*<small>\(<a href="ratings">([0-9,]+) votes</a>\)</small>' )
    pattern_director = re.compile( '<h5>Directors?[^:]*:</h5>[\n]*(.*)' )
    pattern_director2 = re.compile( '<a href="/name/[^>]*>([^<]*)' )
    pattern_writer = re.compile( '<h5>Writers?[^:]*:</h5>[\n]*(.*)' )
    pattern_writer2 = re.compile( '<a href="/name/[^>]*>(.*?)<br/>' )
    pattern_release_date = re.compile( '<h5>Release Date:</h5>[^0-9]*([0-9]* [A-Za-z]* [0-9]*)' )
    pattern_genres = re.compile( '"/Sections/Genres/[^/]*/">([^<]*)</a>' )
    pattern_tagline = re.compile( '<h5>Tagline:</h5>([^<]*)' )
    pattern_plot = re.compile( 'Plot (Outline|Summary):</h5>([^<]*)' )
    pattern_awards = re.compile( '<h5>Awards:</h5>([^<]*)' )
    pattern_user_comments = re.compile( '<h5>User Comments:</h5>([^<]*)' )
    pattern_mpaa = re.compile( 'MPAA</a>:</h5>([^<]*)' )
    pattern_duration = re.compile( '<h5>Runtime:</h5>[^0-9]*([^<]*)' )
    pattern_countries = re.compile( '<h5>Countr[ies|y]:</h5>[^>]*>([^<]*)' )
    pattern_language = re.compile( '<h5>Language:</h5>[^>]*>([^<]*)' )
    pattern_aspect_ratio = re.compile( '<h5>Aspect Ratio:</h5>([^<]*)' )
    pattern_sound_mix = re.compile( '<h5>Sound Mix:</h5>[\n]*(.*)' )
    pattern_sound_mix2 = re.compile( '<a href="/List[^>]*>([^<]*)' )
    pattern_certification = re.compile( '<a href="/List\?certificates=[^"]*">([^<]*)</a>[^<]*(<i>([^<]*)</i>)?' )
    pattern_locations = re.compile( '<h5>Filming Locations:</h5>[.]*[\n]*[^>]*>(.*)' )
    pattern_movie_meter = re.compile( '<h5>MOVIEmeter:.*\n.*\n[^"]*"([^"]*)">[^>]*>([^<]*)</span>(.*)' )
    pattern_studio = re.compile( '"/company/[^/]*/">([^<]*)</a>' )
    pattern_trivia = re.compile( '<h5>Trivia:</h5>[\n]*(.*)' )
    pattern_goofs = re.compile( '<h5>Goofs:</h5>[\n]*(.*)' )
    pattern_quotes = re.compile( '<h5>Quotes:.*?</div>', re.DOTALL )
    pattern_quotes2 = re.compile( '/name/[^>]*>([^<]*).*\n(\[[^\]]*\])*([^<]*)' )
    pattern_poster = re.compile( '<a name="poster".*?src="([^"]*)' )
    pattern_cast = re.compile( '<table class="cast">.*' )
    pattern_cast2 = re.compile( 'href="/name/nm[0-9]*/">([^<]*).*?<td class="char">(.*?)</td>' )

    def __init__( self ):
        self.info = _Info()

    def parse( self, htmlSource ):
        # title
        self.info.title = ""
        matches = self.pattern_title.findall( htmlSource )
        if ( matches ):
            self.info.title = self._clean_text( matches[ 0 ][ 0 ] )

        # year
        self.info.year = 0
        matches = self.pattern_year.findall( htmlSource )
        if ( matches ):
            self.info.year = int( self._clean_text( matches[ 0 ] ) )

        # top 250
        self.info.top_250 = ""
        matches = self.pattern_top250.findall( htmlSource )
        if ( matches ):
            self.info.top_250 = self._clean_text( matches[ 0 ] )

        # user rating
        self.info.user_rating = 0.0
        self.info.user_votes = ""
        matches = self.pattern_user_rating.findall( htmlSource )
        if ( matches ):
            self.info.user_rating = float( matches[ 0 ][ 0 ] ) 
            self.info.user_votes = matches[ 0 ][ 1 ]

        # director
        self.info.director = ""
        # the first match gets all html code
        matches = self.pattern_director.search( htmlSource )
        if ( matches ):
            # we need to assign element 0 to a variable
            text = matches.groups()[ 0 ]
            # now findall directors
            matches = self.pattern_director2.findall( text )
            if ( matches ):
                self.info.director = self._clean_text( ' / '.join( matches ) )

        # writer
        self.info.writer = ""
        # the first match gets all html code
        matches = self.pattern_writer.search( htmlSource )
        if ( matches ):
            # we need to assign element 0 to a variable
            text = matches.groups()[ 0 ]
            # now findall writers
            matches = self.pattern_writer2.findall( text )
            if ( matches ):
                self.info.writer = self._clean_text( ' '.join( matches ) )

        # release date
        self.info.release_date = ""
        matches = self.pattern_release_date.findall( htmlSource )
        if ( matches ):
            self.info.release_date = self._clean_text( matches[ 0 ] )

        # genres
        self.info.genre = ""
        matches = self.pattern_genres.findall( htmlSource )
        if ( matches ):
            self.info.genre = self._clean_text( ' / '.join( matches ) )

        # tagline
        self.info.tagline = ""
        matches = self.pattern_tagline.findall( htmlSource )
        if ( matches ):
            self.info.tagline = self._clean_text( matches[ 0 ] )

        # plot
        self.info.plot = ""
        matches = self.pattern_plot.findall( htmlSource )
        if ( matches ):
            self.info.plot = self._clean_text( matches[ 0 ][ 1 ] )

        # awards
        self.info.awards = ""
        matches = self.pattern_awards.findall( htmlSource )
        if ( matches ):
            self.info.awards = self._clean_text( matches[ 0 ].replace( "\n", " " ) )

        # user comments
        self.info.user_comments = ""
        matches = self.pattern_user_comments.findall( htmlSource )
        if ( matches ):
            self.info.user_comments = self._clean_text( matches[ 0 ] )

        # mpaa
        self.info.mpaa = ""
        matches = self.pattern_mpaa.findall( htmlSource )
        if ( matches ):
            self.info.mpaa = self._clean_text( matches[ 0 ] )

        # duration
        self.info.duration = ""
        matches = self.pattern_duration.findall( htmlSource )
        if ( matches ):
            self.info.duration = self._clean_text( matches[ 0 ] )

        # countries
        self.info.countries = ""
        matches = self.pattern_countries.findall( htmlSource )
        if ( matches ):
            self.info.countries = self._clean_text( matches[ 0 ] )

        # language
        self.info.language = ""
        matches = self.pattern_language.findall( htmlSource )
        if ( matches ):
            self.info.language = self._clean_text( matches[ 0 ] )

        # aspect ratio
        self.info.aspect_ratio = ""
        matches = self.pattern_aspect_ratio.findall( htmlSource )
        if ( matches ):
            self.info.aspect_ratio = self._clean_text( matches[ 0 ] )

        # sound mix
        self.info.sound_mix = ""
        # the first match gets all html code
        matches = self.pattern_sound_mix.search( htmlSource )
        if ( matches ):
            # we need to assign element 0 to a variable
            text = matches.groups()[ 0 ]
            # now find all sound mixes
            matches = self.pattern_sound_mix2.findall( text )
            if ( matches ):
                self.info.sound_mix = self._clean_text( ' / '.join( matches ) )

        # certification
        self.info.certification = ""
        matches = self.pattern_certification.findall( htmlSource )
        if ( matches ):
            self.info.certification = ""
            for match in matches:
                self.info.certification += "%s%s%s%s" % ( ( "", " / ", )[ self.info.certification != "" ], match[ 0 ], ( "", " ", )[ match[ 2 ] != "" ], match[ 2 ], )

        # filming locations
        self.info.locations = ""
        matches = self.pattern_locations.findall( htmlSource )
        if ( matches ):
            self.info.locations = self._clean_text( matches[ 0 ] )

        # movie meter
        self.info.movie_meter = ""
        matches = self.pattern_movie_meter.findall( htmlSource )
        if ( matches ):
            self.info.movie_meter = self._clean_text( ''.join( matches[ 0 ] ) )

        # studio
        self.info.studio = ""
        matches = self.pattern_studio.findall( htmlSource )
        if ( matches ):
            self.info.studio = self._clean_text( matches[ 0 ] )

        # trivia
        self.info.trivia = ""
        matches = self.pattern_trivia.findall( htmlSource )
        if ( matches ):
            self.info.trivia = self._clean_text( matches[ 0 ] )

        # goofs
        self.info.goofs = ""
        matches = self.pattern_goofs.findall( htmlSource )
        if ( matches ):
            self.info.goofs = self._clean_text( matches[ 0 ] )

        # quotes
        self.info.quotes = []
        # the first match gets all html code
        matches = self.pattern_quotes.search( htmlSource )
        if ( matches ):
            # we need to assign element 0 to a variable
            text = matches.group()
            # now find all sound mixes
            matches = self.pattern_quotes2.findall( text )
            if ( matches ):
                for actor, scene, quote in matches:
                    self.info.quotes += [ '%s%s%s - "%s"' % ( self._clean_text( actor ), ( "", " ", )[ self._clean_text( scene ) != "" ], self._clean_text( scene ), self._clean_text( quote ), ) ]

        # poster
        self.info.poster = ""
        matches = self.pattern_poster.findall( htmlSource )
        if ( matches ):
            self.info.poster = matches[ 0 ].replace( "m.jpg", "f.jpg")

        # cast
        self.info.cast = []
        # the first match gets all html code
        matches = self.pattern_cast.search( htmlSource )
        if ( matches ):
            # we need to assign element 0 to a variable
            text = matches.group()
            # now find all sound mixes
            matches = self.pattern_cast2.findall( text )
            if ( matches ):
                for actor, role in matches:
                    self.info.cast += [ ( self._clean_text( actor ), self._clean_text( role ), ) ]

    def _clean_text1( self, text ):
        text = re.sub( self.pattern_clean, '', text ).strip()
        return unicode( text.replace( "&lt;", "<" ).replace( "&gt;", ">" ).replace( "&quot;", '"' ).replace( "&amp;", "&" ).replace( "&#38;", "&" ).replace( "&#39;", "'" ), "iso-8859-1" )

    def _clean_text( self, text ):
        try:
            text = text.strip()
            parser = HTMLParser( None )
            parser.save_bgn()
            parser.feed( text )
            return unicode( parser.save_end().replace( "[1]", "" ), "iso-8859-1" )
        except:
            return text


class IMDBFetcher:
    def __init__( self ):
        # create the cache folder if it does not exist
        self.base_cache_path = self._create_base_cache_path()

    def _create_base_cache_path( self ):
        """ creates the base cache folder """
        # split our path into folders, we replace / with \ for compatability
        path = os.getcwd().replace( ";", "" ).replace( "/", "\\" ).split( "\\" )
        # join the main plugin folders to create our base path
        base_cache_path = os.path.join( "P:\\plugin_data", path[ -2 ], path[ -1 ], "cache" )
        if ( __name__ != "__main__" ):
            # if cache path does not exist, create it
            if ( not os.path.isdir( xbmc.translatePath( base_cache_path ) ) ):
                os.makedirs( xbmc.translatePath( base_cache_path ) )
        # return our cache path
        return base_cache_path

    def fetch_info( self, url ):
        """ Fetch showtimes if available else return a list of theaters """
        try:
            # create the cache filename
            file_path = self._get_cache_name( url )
            # Open url or local cache file
            if ( os.path.exists( file_path ) ):
                usock = open( file_path, "r" )
            else:
                usock = urllib.urlopen( url )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
            if ( __name__ != "__main__" ):
                # Save htmlSource to a file for testing scraper
                if ( not os.path.exists( file_path ) ):
                    file_object = open( file_path, "w" )
                    file_object.write( htmlSource )
                    file_object.close()
            # Parse htmlSource for showtimes
            parser = _IMDBParser()
            parser.parse( htmlSource )
            return parser.info
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return None

    def _get_cache_name( self, url ):
        # get the imdb title code
        title = url.split( "/" )[ -2 ]
        # append imdb title code to cache path
        file_path = os.path.join( self.base_cache_path, title )
        # return our complete file path
        if ( __name__ != "__main__" ):
            return xbmc.translatePath( file_path )
        else:
            return file_path

# used for testing only
debug = False
debugWrite = False

if ( __name__ == "__main__" ):
    url = [ "http://www.imdb.com/title/tt0080684/", "http://www.imdb.com/title/tt0472062/",  "http://www.imdb.com/title/tt0462499/", "http://www.imdb.com/title/tt0389790/", "http://www.imdb.com/title/tt0442933/", "http://www.imdb.com/title/tt0085106/" ]

    for cnt in range( 1,2 ):
        info = IMDBFetcher().fetch_info( url[ cnt ] )
        if ( info ):
            for attr in dir( info ):
                if ( not attr.startswith( "__" ) ):
                    print "%s:" % attr.replace( "_", " " ).title(), getattr( info, attr )
            print "---------------"
