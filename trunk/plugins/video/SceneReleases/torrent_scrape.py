#
#       torrent_scrape.py
#		Plugin to search and scrape different torrent sites, returning the
#		results. Can be used with many different projects
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

__plugin__ = "Torrent Scrape Module"
__author__ = "riegersn"
__url__ = "http://boxeehq.com"
__version__ = "0.1"

import urllib, urllib2, re
import boxeehq_pytools as bhq

class Torrent:
	def __init__( self ):
		self.title = ''
		self.file = ''
		self.seed = 0
		self.leech = 0
		self.date = ''
		self.site = ''


def piratebay__search( _search, minseed = 1 ):
	#Search thepiratebay.org and return results

	_search = bhq.r_dict( _search, { '.':' ', '-':' ' } )
	_url = urllib.quote('thepiratebay.org/search/%s/0/7/200' % ( _search ))
	html = bhq.getHTML( 'http://%s' % (_url) )

	print 'scenereleases::info: searching piratebay ('+_url+')'

	if 'No hits. Try adding an asterisk' in html:
		return 0

	regx = '<a .+?="detLink"[^>]+?>([^<]+?)</a>[^>]+?td>\s.+?>(.+?[0-9]{2}:[0-9]{2})</td>\s.+?<a.+?href="([^"]+?)".*?\s<td align="right">([^<]+?[G|M]iB).+?\s<td[^>]+?>([0-9]+?)<.+?\s.+?>([0-9]+?)<'
	pb = re.compile(regx).findall(html)
	pb = eval(str(pb).replace('&nbsp;',' '))

	if not pb:
		return 0

	_rslt = []

	for title, date, file, size, seed, leech in pb:
		pb = Torrent()
		if int(seed) >= minseed:
			pb.title = title
			pb.seed = seed
			pb.file = file.replace('http://', 'torrent://')
			pb.size = size
			pb.leech = leech
			pb.date = date
			pb.site = 'thepiratebay'
			_rslt.append(pb)

	return _rslt


def mininova__search( _search, minseed = 1 ):
	#Search mininova.org and return results

	_search = bhq.r_dict( _search, { '.':' ', '-':' ' } )
	_url = urllib.quote('www.mininova.org/search/%s/4/seeds' % ( _search ))
	html = bhq.getHTML( 'http://%s' % (_url) )

	print 'scenereleases::info: searching mininova ('+_url+')'

	if '<h1>No results for ' in html:
		return 0

	regx = '<td>([0-9]{2}.+?[A-Z][a-z]{2}.+?[0-9]{2})</td>.*?"/get/([^"]+?)".+?</a><a[^>]+?>([^<]+?)<.*?align="right">([^<]+?)</td>.+?([0-9]+?)<.+?([0-9]+?)<'
	mn = re.compile(regx).findall(html)
	mn = eval(str(mn).replace('&nbsp;',' '))

	if not mn:
		return 0

	_rslt = []

	for date, file, title, size, seed, leech in mn:
		mn = Torrent()
		if int(seed) >= minseed:
			mn.title = title
			mn.seed = seed
			mn.file = 'torrent://mininova.org/get/%s' % ( file )
			mn.size = size
			mn.leech = leech
			mn.date = date
			mn.site = 'mininova'
			_rslt.append(mn)

	return _rslt


def reactor__search( _search, minseed = 1 ):
	#Search torrentreactor and return results

	_search = bhq.r_dict( _search, { '.':'+', '-':'+', ' ':'+' } )
	_url = 'www.torrentreactor.net/search.php?search=&words=%s&cid=5&sid=&type=1&exclude=&orderby=a.seeds&asc=0&x=33&y=8' % ( _search )
	print 'http://%s' % (_url)
	html = bhq.getHTML( 'http://%s' % (_url), 'Torrentreactor search results:' )
	html = bhq.r_dict( html, { '\n':'', '\t':'' } ).strip()

	print 'scenereleases::info: searching torrentreactor ('+_url+')'

	if 'No results.. "' in html:
		return 0

	regx = '<td class="center">([^<]+?)</td>.+?href="http://([^"]+?)".+?<td>([^<]+?)</td><td>([^<]+?)</td><td>([^<]+?)</td>'
	tr = re.compile(regx).findall(html)
	tr = eval(str(tr).replace('&nbsp;',' '))

	if not tr:
		return 0

	_rslt = []

	for date, file, size, seed, leech in tr:
		tr = Torrent()
		if int(seed) >= minseed:
			tr.title = urllib.unquote(file.split(';name=')[-1].replace('+',' '))
			tr.seed = seed
			tr.file = 'torrent://%s' % ( file )
			tr.size = size
			tr.leech = leech
			tr.date = date
			tr.site = 'reactor'
			_rslt.append(tr)

	return _rslt

