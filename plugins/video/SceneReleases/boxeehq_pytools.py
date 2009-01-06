#
#       boxeehq_pytools.py
#		module to perform everyday routines
#		by riegersn
#
#       Copyright 'riegersn' 2008 BoxeeHQ.com
#
#		All my scripts are free to use and to change. I only ask that you credit
#		my work in anything you use this for. If its not your code, don't say it is.
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

__plugin__ = "BoxeeHQ Python Tools Module"
__author__ = "riegersn"
__url__ = "http://boxeehq.com"
__version__ = "0.1"

import urllib, urllib2, re
import string, time, datetime, math

def replace_fromtemplate( _str, _template ):
	for match in _template:
		if match in _str:
			_str = _str.replace( match, _template[match] )
	return _str

def strip_tags(value):
    return re.sub(r'<[^>]*?>', '', value).strip()

def getHTML(url, break_one='', break_two=''):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
	lemon = urllib2.urlopen(req);
	response=lemon.read();
	lemon.close()
	if break_one: response = response.split(break_one)[1]
	if break_two: response = response.split(break_two)[0]
	return response

def r_dict( _str, _dict ):
	for match in _dict:
		if match in _str:
			_str = _str.replace( match, _dict[match] )
	return _str


def listin(xstr, xlist):
	for line in xlist:
		if line in xstr:
			return True
	return False

def r_htmlchar( _str ):
	codes = {
		'&#8217;'	: ";",
		'&amp;'		: "&",
		'&nbsp;'	: " ",
		'&#215;'	: "x"
		}
	for match in codes:
		if match in _str:
			_str = _str.replace( match, codes[match] )
	return _str

class IMDB:
	def __init__( self ):
		self.title = ''
		self.tagline = ''
		self.year = 0
		self.rating = ''
		self.director = []
		self.writer = []
		self.release = ''
		self.genre = []
		self.plot = ''
		self.plot_lg = ''
		self.awards = ''
		self.cast = []
		self.mpaa = ''
		self.runtime = ['0']
		self.language = ''
		self.color = ''
		self.film_locations = []
		self.company = ''
		self.soundtrack = ''
		self.poster = ''
		self.poster_lg = ''
		self.country = []

def imdb__number( _imdbnum, _prefs=[] ):

	site = 'http://www.imdb.com'
	url = '%s/title/%s' % ( site, _imdbnum )

	print 'scraping '+url+'\n'

	html = getHTML(url)
	html = html.replace('\n', '')

	_imdb = IMDB()

	try:
		_imdb.poster = re.compile('" src="(.+?)"').findall(html)[0]
	except: pass

	try:
		_pagetitle = re.compile('<title>(.+?) \((.+?)\)</title>').findall(html)[0]
		_imdb.title = _pagetitle[0]
		_imdb.year = _pagetitle[1]
	except: pass

	try:
		_imdb.rating = re.compile('=\"meta\"><b>(.+?)</b>').findall(html)[0]
	except: pass

	_info = re.compile(' class=\"info\"><h5>(.+?)</h5>(.+?)</div>').findall(html)

	_dt = {}
	for i, x in _info:
		#print fix_header(i)
		_dt[imdb__fix_header(i)] = x

	try:
		_imdb.director = strip_tags(_dt['director'])
	except: pass

	try:
		_imdb.release = re.compile(' (.+?) \(').findall(_dt['release date'])[0]
	except: pass

	try:
		_imdb.genre = re.compile('<a href=\"/Sections/Genres/(.+?)/\">').findall(_dt['genre'])
	except: pass

	try:
		_imdb.plot = re.compile('(.+?)<a class=\"').findall(_dt['plot'])[0].replace('|', '').strip()
	except: pass

	try:
		_imdb.mpaa = re.compile(' Rated (.+?) for ').findall(_dt['mpaa'])[0]
	except: pass

	try:
		_imdb.advisory = strip_tags(_dt['mpaa'])
	except: pass

	try:
		_imdb.runtime = re.compile('([0-9]+)').findall(_dt['runtime'])[0]
	except: pass

	try:
		_imdb.awards = re.compile('(.+?)<').findall(_dt['awards'])[0].strip()
	except: pass

	try:
		_imdb.color = strip_tags(_dt['color'])
	except: pass

	try:
		_imdb.language = strip_tags(_dt['language'])
	except: pass

	try:
		_imdb.studio = re.compile('">(.+?)</').findall(_dt['company'])[0]
	except: pass

	try:
		_imdb.film_locations = strip_tags(_dt['filming locations']).replace('more', '').split(', ')
	except: pass

	try:
		_imdb.country = strip_tags(_dt['country']).split(' | ')
	except: pass

	try:
		_imdb.cast = re.compile('"nm">.*?=\"/name/.+?/\">(.+?)</a>').findall(html)[:5]
	except: pass

	try:
		_imdb.writer = re.compile('/\">(.+?)</a>').findall(_dt['writers'])
	except:
		try:
			_imdb.writer = re.compile('/\">(.+?)</a>').findall(_dt['writers (wga)'])
		except: pass

	try:
		_imdb.tagline = strip_tags(_dt['tagline'])
	except: pass

	try:
		_imdb.soundtrack = re.compile('(.+?)<a').findall(_dt['soundtrack'])[0].strip()
	except: pass

	if 'bigplot' in _prefs:
		try:
			plot_lg_link = '%s/title/%s/plotsummary' % ( site, _imdbnum )
			_imdb.plot_lg = getHTML(plot_lg_link, '<p class="plotpar">', '<i>').strip()
		except: pass

	if 'bigposter' in _prefs:
		try:
			poster_lg_link = '%s%s' % ( site, re.compile('<a name="poster" href="(.+?)"').findall(html)[0] )
			bigposter = getHTML(poster_lg_link, '<td valign="middle" align="center">', '</td>')
			_imdb.poster_lg = re.compile('src=\"(.+?)"').findall(bigposter)[0]
		except: pass

	return _imdb

def imdb__fix_header( _str ):
	return strip_tags(_str).replace(':','').lower()

def apple__trailer( _search, _genre ):
	#Search boxee's xml for a specified apple trailer
	_search = _search.replace('.',' ').replace('-',' ').lower().strip()

	print 'scenereleases::info: trailer lookup: title('+_search+') genre('+str(_genre)+')'

	_genres = [
		'Action and Adventure',
		'Comedy',
		'Documentary',
		'Drama',
		'Family',
		'Fantasy',
		'Foreign',
		'Horror',
		'Musical',
		'Romance',
		'Science Fiction',
		'Thriller'
		]

	_lookin = []
	for genre in _genre:
		for _match in _genres:
			if genre.lower() in _match.lower():
				_entry = _match.replace(' ','_').lower()
				_entry = 'http://dir.boxee.tv/amt/genre/%s' % ( _entry )
				_lookin.append(_entry)

	if not _lookin:
		print 'scenereleases::error: unable to identify genre for trailer search!'
		return ''

	trailer = ''
	for i in _lookin:
		xml = getHTML(i).lower().replace('\n', '')
		if '<title>'+_search+'</title>' in xml:
			xml = re.compile('<title>'+_search+'</title>(.+?)</item>').findall(xml)[0]
			trailer = re.compile('url="http://movies\.apple\.com/movies/(.+?)"').findall(xml)
			break

	if not trailer:
		print 'scenereleases::info: no trailers found!'
	else:
		print 'scenereleases::info: ' +str(len(trailer))+ ' trailers found!'

	return trailer
