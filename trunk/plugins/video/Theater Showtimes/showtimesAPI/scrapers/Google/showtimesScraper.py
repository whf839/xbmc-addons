"""
Scraper for http://www.google.com/movies

Nuka1195
"""

import sys
import os

try:
    import xbmc
except:
    pass

from sgmllib import SGMLParser
import re
import urllib
import datetime


__title__ = "Google"
__credit__ = "Nuka1195"


class _Info:
    def __init__( self, *args, **kwargs ):
        self.__dict__.update( kwargs )


class _TheaterListParser:
    # HTML cleaning regex pattern
    pattern_clean = re.compile( '<.+?>' )

    # Theater list regex pattern
    pattern_theater = re.compile( '<a href="(/movies\?near=.*?)<b>([^<]*)</b>[</a>]*?<br><[^>]*>([^<]*)<a href="http://maps.google.co' )
    
    def __init__( self ):
        self.theater_list = {}

    def feed( self, htmlSource ):
        # find all theaters
        theaters = self.pattern_theater.findall( htmlSource )
        # if there are theaters
        if ( theaters ):
            # enumerate thru the list of theaters and parse the info
            for theater in theaters:
                # theater url: if there are more than one theater, should contain a tid value
                if ( "&tid=" in theater[ 0 ] ):
                    url = theater[ 0 ].split( '<a href="' )[ -1 ][ : -2 ]
                else:
                    url = theater[ 0 ].split( '<a href="' )[ -1 ].split( "&" )[ 0 ]
                # split the data into address and phone parts
                parts = theater[ 2 ].replace( "&nbsp;", " " ).split( " - " )
                # set our _info() object
                self.theater_list[ self._clean_text( theater[ 1 ] ) ] = _Info( trailer="", imdb="", label2=self._clean_text( parts[ 1 ] ), mpaa="", duration=self._clean_text( parts[ 0 ] ), genre="", premiered="", plot="", thumbnail="", url="http://www.google.com%s" % url )

    def _clean_text( self, text ):
        # remove html source
        text = re.sub( self.pattern_clean, '', text ).strip()
        # replace entities and return iso-8859-1 unicode
        return unicode( text.replace( "&lt;", "<" ).replace( "&gt;", ">" ).replace( "&quot;", '"' ).replace( "&#38;", "&" ).replace( "&#39;", "'" ).replace( "&amp;", "&" ), "iso-8859-1" )


class _ShowtimesParser_re:
    """ 
        Parser Class: parses an html document for movie showtimes
        - creates a key { theater: [#:##] }
    """
    # HTML cleaning regex pattern
    pattern_clean = re.compile( '<.+?>' )

    # Theater list regex pattern
    pattern_theaters = re.compile( '<a href="(/movies\?near=[^&]*&tid=[^"]*)">.*?<a href="' )
    pattern_showtimes = re.compile( '<a href="(/movies\?near=[^"]*)"><b>([^<]*)</b>[</a>]*?<br>([^<]*)<')#([^<]*)<a href="http://maps.google.co' )
    
    #<a href="/movies?near=48161&mid=444dbdc49f2ca7c2"><b>Doomsday</b></a><br>1hr&nbsp;45min - Rated&nbsp;R - Action/Adventure/Suspense/Thriller/Horror - <a href="http://www.google.com/url?q=http://www.apple.com/trailers/universal/doomsday/&sa=X&oi=moviesa&ii=6&usg=AFQjCNElPWQ1Xshc5wRIz1D9-HhCvDjt7A" class=fl>Trailer</a> - <a href="http://www.google.com/url?q=http://www.imdb.com/title/tt0483607/&sa=X&oi=moviesi&ii=6&usg=AFQjCNH9T40ECPcFFc7BPQp5XINJe5w-9w" class=fl>IMDb</a><br>12:15&nbsp; 2:45&nbsp; 5:30&nbsp; 8:00&nbsp; 10:35pm</font>
    #<a href="/movies?near=2830&mid=e9e66ac4af0fab81"><b>10,000 B.C.</b></a><br>1hr&nbsp;49min - Rated&nbsp;M - Drama - <a href="http://www.google.com/url?q=http://www.apple.com/trailers/wb/10000bc/&sa=X&oi=moviesa&ii=6&usg=AFQjCNHkKU_06VCg4TB6zZk4liwd3ZP3tw" class=fl>Trailer</a><br>11:30am&nbsp; 1:50&nbsp; 8:30pm</font></td><td>&nbsp;&nbsp;&nbsp;</td><td align=center>
    def __init__( self ):
        self.theaters = {}

    def feed( self, htmlSource ):
        # find all theaters
        theaters = self.pattern_theaters.findall( htmlSource )
        # if there are theaters
        if ( theaters ):
            # enumerate thru the list of theaters and parse the info
            for theater in theaters:
                #if ( "&tid=" in theater ):
                print theater
                ## theater url: if there are more than one theater, should contain a tid value
                #if ( "&tid=" in theater[ 0 ] ):
                #    url = theater[ 0 ].split( '<a href="' )[ -1 ][ : -2 ]
                #else:
                #    url = theater[ 0 ].split( '<a href="' )[ -1 ].split( "&" )[ 0 ]
                ## split the data into address and phone parts
                #parts = theater[ 2 ].replace( "&nbsp;", " " ).split( " - " )
                ## set our _info() object
                #self.theater_list[ self._clean_text( theater[ 1 ] ) ] = _Info( trailer="", imdb="", label2=self._clean_text( parts[ 1 ] ), mpaa="", duration=self._clean_text( parts[ 0 ] ), genre="", premiered="", plot="", thumbnail="", url="http://www.google.com%s" % url )

    def _clean_text( self, text ):
        # remove html source
        text = re.sub( self.pattern_clean, '', text ).strip()
        # replace entities and return iso-8859-1 unicode
        return unicode( text.replace( "&lt;", "<" ).replace( "&gt;", ">" ).replace( "&quot;", '"' ).replace( "&#38;", "&" ).replace( "&#39;", "'" ).replace( "&amp;", "&" ), "iso-8859-1" )



class _ShowtimesParser( SGMLParser ):
    """ 
        Parser Class: parses an html document for movie showtimes
        - creates a key { theater: [#:##] }
    """
    def reset( self ):
        SGMLParser.reset( self )
        self.theaters = {}
        self.current_theater = ""
        self.theater_id = ""
        self.theater_set = False
        self.start_theaters = False

    def start_a( self, attrs ):
        for key, value in attrs:
            if ( key == "href" and value.startswith( "/movies?near=" ) ):
                self.theater_id = value
                self.current_theater = ""
            elif ( key == "href" and "www.imdb.com" in value and self.theaters.has_key( self.current_theater ) ):
                url = value.split( "&" )[ 0 ]
                url = url.split( "=" )[ 1 ]
                self.theaters[ self.current_theater ].imdb = url
            elif ( key == "href" and "www.apple.com" in value ):
                pass
                #TODO: this is not an actual trailer url, maybe consider parsing it for actual trailers
                #self.theaters[ self.current_theater ].trailer = value

    def end_a( self ):
        if ( self.start_theaters ):
            if ( self.theater_id ):
                self.theaters[ self.current_theater ] = _Info( trailer="", imdb="", label2="", mpaa="", duration="", genre="", premiered="", plot="", thumbnail="", url="http://www.google.com%s" % self.theater_id )
                self.theater_id = ""
                self.show_info = ""
                self.theater_set = True

    def handle_data( self, text ):
        if ( self.start_theaters and text.strip() ):
            if ( self.theater_id ):
                self.current_theater += text
            elif ( text.strip()[ 0 ].isdigit() and ":" in text ):
                if ( self.theaters[ self.current_theater ].premiered ):
                    self.theaters[ self.current_theater ].premiered += ", "
                self.theaters[ self.current_theater ].premiered += text.strip()
                self.theater_set = False
            elif ( self.theater_set and text != "Map" and text != "Trailer" and text != "IMDb" ):
                self.show_info += "%s " % text.strip()
            elif ( self.theater_set and self.show_info ):
                try:
                    self.theaters[ self.current_theater ].duration = self.show_info.split( "-" )[ 0 ].strip()
                    self.theaters[ self.current_theater ].mpaa = self.show_info.split( "-" )[ 1 ].strip()
                    self.theaters[ self.current_theater ].genre = self.show_info.split( "-" )[ 2 ].strip()
                except:
                    pass
        elif ( text == "Show more movies" or text == "Show more films" or text == "Show more theaters" ):
            self.start_theaters = True
            self.theater_id = ""


class ShowtimesFetcher:
    def __init__( self ):
        self.base_url = "http://www.google.com"

    def get_theater_list( self, location ):
        """ *REQUIRED: Returns a list of theaters in your local """
        # format the location
        location = self._format_param( location )
        # get the list of theaters
        theaters = self._get_theater_list( self.base_url + "/movies?near=%s" % ( location, ) )
        # return the list
        return theaters
    
    def get_selection( self, url, day=0 ):
        """ *REQUIRED: Returns movie listing and date for the selected theater or
        theater listing for a specific movie """
        # fetch the list of showtimes
        date, showtimes = self._fetch_showtimes( url, day )
        # if no showtimes, try todays date
        if ( showtimes is None and day > 0 ):
            date, showtimes = self._fetch_showtimes( url, 0 )
        # return our results
        return date, showtimes

    def _fetch_showtimes( self, url, day ):
        """ Fetch showtimes if available """
        try:
            # add the appropriate number of days to todays date
            date = datetime.date.today() + datetime.timedelta( days=day )
            # get the current locals long date format and convert it to what strftime() expects
            try:
                format = xbmc.getRegion( "datelong" ).replace( "DDDD", "%A" ).replace( "MMMM", "%B" ).replace( "D", "%d" ).replace( "YYYY", "%Y" )
            except:
                format = "%A, %B %d, %Y"
            # format our date
            date = date.strftime( format )
            # create our url
            url = "%s&date=%d" % ( url, day, )
            # open url or local file (if debug)
            if ( not debug ):
                usock = urllib.urlopen( url )
            else:
                usock = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source.txt" ), "r" )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
            # if no showtimes were found raise an error
            if ( htmlSource.find( "No showtimes were found" ) >= 0 ):
                raise
            # save htmlSource to a file for testing scraper (if debugWrite)
            if ( debugWrite ):
                file_object = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source.txt" ), "w" )
                file_object.write( htmlSource )
                file_object.close()
            # parse htmlSource for showtimes
            parser = _ShowtimesParser()
            parser.feed( htmlSource )
            #parser.close()
            return date, parser.theaters
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return date, None
        
    def _format_param( self, param ):
        """ Converts param to the form expected by www.google.com/movies """
        result = urllib.quote_plus( param )
        return result

    def _get_theater_list( self, url ):
        try:
            # open url or local file (if debug)
            if ( not debug ):
                usock = urllib.urlopen( url )
            else:
                usock = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source3c.txt" ), "r" )
            # read source
            htmlSource = usock.read()
            # close socket
            usock.close()
            # save htmlSource to a file for testing scraper (if debugWrite)
            if ( debugWrite ):
                file_object = open( os.path.join( os.getcwd().replace( ";", "" ), "showtimes_source3.txt" ), "w" )
                file_object.write( htmlSource )
                file_object.close()
            # parse htmlSource for theaters
            parser = _TheaterListParser()
            parser.feed( htmlSource )
            #parser.close()
            return parser.theater_list
        except:
            # oops print error message
            print "ERROR: %s::%s (%d) - %s" % ( self.__class__.__name__, sys.exc_info()[ 2 ].tb_frame.f_code.co_name, sys.exc_info()[ 2 ].tb_lineno, sys.exc_info()[ 1 ], )
            return None


# used for testing only
debug = False
debugWrite = False

if ( __name__ == "__main__" ):
    # used to test get_lyrics() 
    movie = [ "wall•e", "Bee Movie", "The Seeker: the Dark is Rising", "el cantante", "Rush Hour 3", "The Simpsons Movie", "Transformers", "I Now Pronounce You Chuck & Larry", "Transformers", "I Now Pronounce You Chuck & Larry" ]
    location = [ "NSW 2000", "2830", "detroit", "Houston", "detroit", "new york", "London", "Toronto", "33102", "W2 4YL", "T1A 3T9" ]
    url = [ "http://www.google.com/movies?near=detroit&tid=3de92b236832db4f", "http://www.google.com/movies?near=2830", "http://www.google.com/movies?near=90210&tid=63dad2c3a9a07013" ]

    for cnt in range( 2,3 ):
        #date = "today"
        #theaters = ShowtimesFetcher().get_theater_list( location[ cnt ] )
        date, theaters = ShowtimesFetcher().get_selection( url[ cnt ], 0 )
        print date
        print
        if ( theaters ):
            theater_names = theaters.keys()
            theater_names.sort()
            for theater in theater_names:
                print theater
                for attr in dir( theaters[ theater ] ):
                    if ( not attr.startswith( "__" ) ):
                        print "%s:" % attr.replace( "_", " " ).title(), getattr( theaters[ theater ], attr )
                print "---------------"
