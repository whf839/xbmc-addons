# -*- coding: cp1252 -*-

__plugin__ = "Tv Shack"
__author__ = "voinage"
__url__ = "http://code.google.com/p/voinage-xbmc-plugins/"
__date__ = "11.01.2010"
__version__ = "r3"

import urllib, urllib2, re, xbmcplugin, xbmcgui, os, sys

COOKIEFILE = os.path.join(os.getcwd(), 'cookies.lwp')
print "Cookiefile=" + COOKIEFILE

def AZ(url):
        res = []
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	res.append((url, "0-9"))
	for a in alphabet:
		res.append((url, a))
	for url, name in res:
                addDir(name, url, 1, "")

#Coolblaze-xbmc forums.

def ajoin(arr):
	strtest = ''
	for num in range(len(arr)):
		strtest = strtest + str(arr[num])
	return strtest

def asplit(mystring):
	arr = []
	for num in range(len(mystring)):
		arr.append(mystring[num])
	return arr

def decrypt(str1, key1, key2):

	__reg1 = []
	__reg3 = 0
	while (__reg3 < len(str1)):
		__reg0 = str1[__reg3]
		holder = __reg0
		if (holder == "0"):
			__reg1.append("0000")
		else:
			if (__reg0 == "1"):
				__reg1.append("0001")
			else:
				if (__reg0 == "2"):
					__reg1.append("0010")
				else:
					if (__reg0 == "3"):
						__reg1.append("0011")
					else:
						if (__reg0 == "4"):
							__reg1.append("0100")
						else:
							if (__reg0 == "5"):
								__reg1.append("0101")
							else:
								if (__reg0 == "6"):
									__reg1.append("0110")
								else:
									if (__reg0 == "7"):
										__reg1.append("0111")
									else:
										if (__reg0 == "8"):
											__reg1.append("1000")
										else:
											if (__reg0 == "9"):
												__reg1.append("1001")
											else:
												if (__reg0 == "a"):
													__reg1.append("1010")
												else:
													if (__reg0 == "b"):
														__reg1.append("1011")
													else:
														if (__reg0 == "c"):
															__reg1.append("1100")
														else:
															if (__reg0 == "d"):
																__reg1.append("1101")
															else:
																if (__reg0 == "e"):
																	__reg1.append("1110")
																else:
																	if (__reg0 == "f"):
																		__reg1.append("1111")

		__reg3 = __reg3 + 1

	mtstr = ajoin(__reg1)
	__reg1 = asplit(mtstr)
	__reg6 = []
	__reg3 = 0
	while (__reg3 < 384):

		key1 = (int(key1) * 11 + 77213) % 81371
		key2 = (int(key2) * 17 + 92717) % 192811
		__reg6.append((int(key1) + int(key2)) % 128)
		__reg3 = __reg3 + 1

	__reg3 = 256
	while (__reg3 >= 0):

		__reg5 = __reg6[__reg3]
		__reg4 = __reg3 % 128
		__reg8 = __reg1[__reg5]
		__reg1[__reg5] = __reg1[__reg4]
		__reg1[__reg4] = __reg8
		__reg3 = __reg3 - 1

	__reg3 = 0
	while (__reg3 < 128):

		__reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
		__reg3 = __reg3 + 1

	__reg12 = ajoin(__reg1)
	__reg7 = []
	__reg3 = 0
	while (__reg3 < len(__reg12)):

		__reg9 = __reg12[__reg3:__reg3 + 4]
		__reg7.append(__reg9)
		__reg3 = __reg3 + 4


	__reg2 = []
	__reg3 = 0
	while (__reg3 < len(__reg7)):
		__reg0 = __reg7[__reg3]
		holder2 = __reg0

		if (holder2 == "0000"):
			__reg2.append("0")
		else:
			if (__reg0 == "0001"):
				__reg2.append("1")
			else:
				if (__reg0 == "0010"):
					__reg2.append("2")
				else:
					if (__reg0 == "0011"):
						__reg2.append("3")
					else:
						if (__reg0 == "0100"):
							__reg2.append("4")
						else:
							if (__reg0 == "0101"):
								__reg2.append("5")
							else:
								if (__reg0 == "0110"):
									__reg2.append("6")
								else:
									if (__reg0 == "0111"):
										__reg2.append("7")
									else:
										if (__reg0 == "1000"):
											__reg2.append("8")
										else:
											if (__reg0 == "1001"):
												__reg2.append("9")
											else:
												if (__reg0 == "1010"):
													__reg2.append("a")
												else:
													if (__reg0 == "1011"):
														__reg2.append("b")
													else:
														if (__reg0 == "1100"):
															__reg2.append("c")
														else:
															if (__reg0 == "1101"):
																__reg2.append("d")
															else:
																if (__reg0 == "1110"):
																	__reg2.append("e")
																else:
																	if (__reg0 == "1111"):
																		__reg2.append("f")

		__reg3 = __reg3 + 1

	endstr = ajoin(__reg2)
	return endstr
#tv alacarta meg section. _cheers saved time.
def Megavideo(mega):
	xbmc.output("Megavideo")
	modoPremium = xbmcplugin.getSetting("megavideopremium")
	xbmc.output("modoPremium=" + modoPremium)

	if modoPremium == "false":
		movielink = getlowurl(mega)
	else:
		movielink = gethighurl(mega)

def gethighurl(code):
	xbmc.output("Use premium mode")
	megavideocookie = xbmcplugin.getSetting("megavideocookie")
	xbmc.output("megavideocookie=#" + megavideocookie + "#")
	xbmc.output("Averiguando cookie...")
	megavideologin = xbmcplugin.getSetting("megavideouser")
	xbmc.output("megavideouser=#" + megavideologin + "#")
	megavideopassword = xbmcplugin.getSetting("megavideopassword")
	xbmc.output("megavideopassword=#" + megavideopassword + "#")
	megavideocookie = GetMegavideoUser(megavideologin, megavideopassword)
	xbmc.output("megavideocookie=#" + megavideocookie + "#")
	req = urllib2.Request("http://www.megavideo.com/xml/player_login.php?u=" + megavideocookie + "&v=" + code)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	patronvideos = 'downloadurl="([^"]+)"'
	matches = re.compile(patronvideos, re.DOTALL).findall(urllib2.urlopen(req).read())
	addLink('Premium Megavideo File', matches[0].replace("%3A", ":").replace("%2F", "/").replace("%20", " "), '')

def getlowurl(code):
	xbmc.output("Use normal mode")
	req = urllib2.Request("http://www.megavideo.com/xml/videolink.php?v=" + code)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
	req.add_header('Referer', 'http://www.megavideo.com/')
	page = urllib2.urlopen(req);response = page.read();page.close()
	errort = re.compile(' errortext="(.+?)"').findall(response)
	movielink = ""
	if len(errort) <= 0:
		s = re.compile(' s="(.+?)"').findall(response)
		k1 = re.compile(' k1="(.+?)"').findall(response)
		k2 = re.compile(' k2="(.+?)"').findall(response)
		un = re.compile(' un="(.+?)"').findall(response)
	addLink('Standard Megavideo File', "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv", '')

def GetMegavideoUser(login, password):
	xbmc.output("GetMegavideoUser")
	# ---------------------------------------
	#  Inicializa la librería de las cookies
	# ---------------------------------------
	ficherocookies = COOKIEFILE
	# the path and filename to save your cookies in

	cj = None
	ClientCookie = None
	cookielib = None

	# Let's see if cookielib is available
	try:
		import cookielib
	except ImportError:
		# If importing cookielib fails
		# let's try ClientCookie
		try:
			import ClientCookie
		except ImportError:
			# ClientCookie isn't available either
			urlopen = urllib2.urlopen
			Request = urllib2.Request
		else:
			# imported ClientCookie
			urlopen = ClientCookie.urlopen
			Request = ClientCookie.Request
			cj = ClientCookie.LWPCookieJar()

	else:
		# importing cookielib worked
		urlopen = urllib2.urlopen
		Request = urllib2.Request
		cj = cookielib.LWPCookieJar()
		# This is a subclass of FileCookieJar
		# that has useful load and save methods

	# ---------------------------------
	# Instala las cookies
	# ---------------------------------

	if cj is not None:
	# we successfully imported
	# one of the two cookie handling modules

		if os.path.isfile(ficherocookies):
			# if we have a cookie file already saved
			# then load the cookies into the Cookie Jar
			cj.load(ficherocookies)

		# Now we need to get our Cookie Jar
		# installed in the opener;
		# for fetching URLs
		if cookielib is not None:
			# if we use cookielib
			# then we get the HTTPCookieProcessor
			# and install the opener in urllib2
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			urllib2.install_opener(opener)

		else:
			# if we use ClientCookie
			# then we get the HTTPCookieProcessor
			# and install the opener in ClientCookie
			opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
			ClientCookie.install_opener(opener)

	#print "-------------------------------------------------------"
	url = "http://www.megavideo.com/?s=signup"
	#print url
	#print "-------------------------------------------------------"
	theurl = url
	# an example url that sets a cookie,
	# try different urls here and see the cookie collection you can make !

	txdata = "action=login&cnext=&snext=&touser=&user=&nickname=" + login + "&password=" + password
	# if we were making a POST type request,
	# we could encode a dictionary of values here,
	# using urllib.urlencode(somedict)

	txheaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
				  'Referer':'http://www.megavideo.com/?s=signup'}
	# fake a user agent, some websites (like google) don't like automated exploration

	req = Request(theurl, txdata, txheaders)
	handle = urlopen(req)
	cj.save(ficherocookies)                     # save the cookies again    

	data = handle.read()
	xbmc.output("----------------------")
	xbmc.output("Respuesta de Megavideo")
	xbmc.output("----------------------")
	xbmc.output(data)
	xbmc.output("----------------------")
	handle.close()

	cookiedatafile = open(ficherocookies, 'r')
	cookiedata = cookiedatafile.read()
	cookiedatafile.close();

	xbmc.output("----------------------")
	xbmc.output("Cookies despues")
	xbmc.output("----------------------")
	xbmc.output(cookiedata)
	xbmc.output("----------------------")

	patronvideos = 'user="([^"]+)"'
	matches = re.compile(patronvideos, re.DOTALL).findall(cookiedata)
	if len(matches) == 0:
		patronvideos = 'user=([^\;]+);'
		matches = re.compile(patronvideos, re.DOTALL).findall(cookiedata)

	return matches[0]

def CATS():
        req = urllib2.Request('http://tvshack.net/channels')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
        response = urllib2.urlopen(req).read()
        lexus = re.compile('<div class="channels-link"><a href="(.+?)">(.+?)</a></div>').findall(response)
        for ref, name in lexus:
                if not name.find('ovies') > 0:
                        addDir(name, ref, 1, "")

        addDir("Search", 'http://tvshack.net', 6, "http://www.mergeleftmarketing.com/vsImages/Information/Images%20for%20Consultation/Search.jpg")
        addDir("Movies", 'http://tvshack.net/movies/', 8, "")


def INDEX(url, name):
        if url.find('/movies') > 0:
                alph = []
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                link = urllib2.urlopen(req).read()
                clean = re.sub('&eacute;', 'ea', link)
                clean2 = re.sub('&amp;', '&', clean)
                clean3 = re.sub('&quot;', '', clean2)
                clean4 = re.sub('&nbsp;<font class=".+?">.+?</font>', '', clean3)
                clean5 = re.sub('<font class="new-updated">Updated!</font>', '', clean4);clean6 = re.sub('<font class="new-new">New!</font>', '', clean5)
                clean7 = re.sub('&#x22;', '', clean6)
                bits = re.compile('<li><a href="(.+?)">(.+?)<span').findall(clean7)
                for i in range(0, len(bits)):
                        if bits[i][1][:1].isdigit() == True and name == "0-9":
                                alph.append(bits[i])

                        elif bits[i][1][:1] == name:
                                alph.append(bits[i])
                for url, name in alph:
                        if url.find('movies') > 0:
                                addDir(name, url, 2, "")
                        if url.find('/documentaries/') > 0:
                                addDir(name, url, 3, "")
                        if url.find('/anime/') > 0:
                                addDir(name, url, 4, "")
                        if url.find('/comedy/') > 0:
                                addDir(name, url, 3, "")
                        if url.find('/music/') > 0:
                                addDir(name, url, 4, "")
                        if url.find('tv/') > 0:
                                addDir(name, url, 4, "")


        else:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                link = urllib2.urlopen(req).read()
                clean = re.sub('&eacute;', 'ea', link)
                clean2 = re.sub('&amp;', '&', clean)
                clean3 = re.sub('&quot;', '', clean2)
                clean4 = re.sub('&nbsp;<font class=".+?">.+?</font>', '', clean3)
                clean5 = re.sub('<font class="new-updated">Updated!</font>', '', clean4);clean6 = re.sub('<font class="new-new">New!</font>', '', clean5)
                clean7 = re.sub('&#x22;', '', clean6)
                match = re.compile('<li><a href="(.+?)">(.+?)<span').findall(clean7)
                for url, name in match:
                        if url.find('movies') > 0:
                                addDir(name, url, 2, "")
                        if url.find('/documentaries/') > 0:
                                addDir(name, url, 3, "")
                        if url.find('/anime/') > 0:
                                addDir(name, url, 4, "")
                        if url.find('/comedy/') > 0:
                                addDir(name, url, 3, "")
                        if url.find('/music/') > 0:
                                addDir(name, url, 4, "")
                        if url.find('tv/') > 0:
                                addDir(name, url, 4, "")


def ALTERNATE(url, name):

        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                link = urllib2.urlopen(req).read()
        except:
                req = urllib2.Request("http://tvshack.net%s" % url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                link = urllib2.urlopen(req).read()

        clean = re.sub('&eacute;', 'ea', link);clean2 = re.sub('&amp;', '&', clean)
        clean3 = re.sub('&quot;', '', clean2);clean4 = re.sub('&nbsp;<font class=".+?">.+?</font>', '', clean3)
        alt = re.compile('<h3>Alternate links</h3>.(.+?)</ul>', re.DOTALL).findall(clean4)
        altlink = re.compile('<li><a href="(.+?)"><img src="(.+?)" />').findall(str(alt))
        for url, thumb in altlink:
                addDir(name, url, 3, thumb)

def PART(url, name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
        link = urllib2.urlopen(req).read()
        part = re.compile('<a href="javascript:changevid.(.+?).;"').findall(link)
        idtag = re.compile('http://tvshack.net/report_video/(.+?)/(.+?)/","report"').findall(link)
        for pnumb in part:
                addDir('%s Part-%s' % ((name, pnumb)), 'http://tvshack.net/video_load/%s/%s/%s/' % ((idtag[0][0], idtag[0][1], pnumb)), 5, '')

def EPS(url, name):
        try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                link = urllib2.urlopen(req).read()
        except:
                req = urllib2.Request("http://tvshack.net%s" % url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                clean4 = urllib2.urlopen(req).read()

        match = re.compile('<li><a href="(.+?)">(.+?)</a><a href=""><span>.+?</span></a>').findall(clean4)
        if len(match) < 1:
                match = re.compile('<a href="(.+?)">(.+?)<span>').findall(clean4)
        for url, name in match:
                season = re.compile('http://tvshack.net/.+?/.+?/(.+?)/episode_.+?/').findall(url)
                try:
                        addDir(season[0] + ' - ' + name, url, 2, '')
                except:
                        addDir(name, url, 2, '')
def SEARCH():
        keyb = xbmc.Keyboard('', 'Search TV Shack')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode = urllib.quote(search)
                req = urllib2.Request('http://tvshack.net/search/' + encode)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
                clean = re.sub('&eacute;', 'ea', link)
                clean2 = re.sub('&amp;', '&', clean)
                clean3 = re.sub('&quot;', '', clean2)
                clean4 = re.sub('&nbsp;<font class=".+?">.+?</font>', '', clean3)
                clean5 = re.sub('<font class="new-updated">Updated!</font>', '', clean4);clean6 = re.sub('<font class="new-new">New!</font>', '', clean5)
                match = re.compile('<li><a href="(.+?)">.+?<strong>(.+?)</strong></a>').findall(clean6)
                for url, name in match:
                        if url.find('/movies/') > 0:
                                addDir(name, url, 2, "")
                        if url.find('/documentaries/') > 0:
                                addDir(name, url, 3, "")
                        if url.find('/anime/') > 0:
                                addDir(name, url, 4, "")
                        if url.find('/comedy/') > 0:
                                addDir(name, url, 3, "")
                        if url.find('/music/') > 0:
                                addDir(name, url, 4, "")
                        if url.find('/tv/') > 0:
                                addDir(name, url, 4, "")


def VIDLINK(url, name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
        req.add_header('X-Requested-With', 'XMLHttpRequest')
        link = urllib2.urlopen(req).read()
        tweety = re.compile('flashvars="file=(.+?)&type=flv').findall(link)
        try:
                addLink(name, tweety[0] + '?.flv', '')
        except:
                try:
                        i = 0
                        bit = re.compile('<iframe src="(.+?)"').findall(link)
                        req = urllib2.Request(bit[0])
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                        page = urllib2.urlopen(req);response = page.read();page.close()
                        Id = re.compile("'VideoIDS','(.+?)'").findall(response)
                        youku = "http://clipnabber.com/gethint.php?mode=1&url=http://v.youku.com/v_show/id_" + Id[0] + "%3Ddothtml&sid=223287746064192186603"
                        req = urllib2.Request(youku)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                        page = urllib2.urlopen(req);response = page.read();page.close()
                        match = re.compile('<a href=(.+?)><strong>(.+?)</strong>').findall(response)
                        for url, name in match:
                                addLink(name, url, '')
                except IndexError:
                        try:
                                mega = re.compile('<param name="movie" value="http://www.megavideo.com/v/(.+?)">').findall(link)
                                mega[0] = mega[0][0:8]
                                Megavideo(mega[0])
                        except IndexError: pass
                        try:
                                bit = re.compile('src="(.+?)">').findall(link)
                                req = urllib2.Request(bit[0])
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3')
                                page = urllib2.urlopen(req);response = page.read();page.close()
                                Mov = re.compile('<embed type="video/divx" src="(.+?)"').findall(response)
                                addLink(name, Mov[0], '')
                        except: pass


def get_params():
        param = []
        paramstring = sys.argv[2]
        if len(paramstring) >= 2:
                params = sys.argv[2]
                cleanedparams = params.replace('?', '')
                if (params[len(params) - 1] == '/'):
                        params = params[0:len(params) - 2]
                pairsofparams = cleanedparams.split('&')
                param = {}
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]

        return param


def addLink(name, url, thumbnail):
        ok = True
        def Download(url, dest):
                dp = xbmcgui.DialogProgress()
                dp.create("Tv-shack Download", "Downloading File", url)
                urllib.urlretrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, url, dp))
        def _pbhook(numblocks, blocksize, filesize, url=None, dp=None):
                try:
                        percent = min((numblocks * blocksize * 100) / filesize, 100)
                        print percent
                        dp.update(percent)
                except:
                        percent = 100
                        dp.update(percent)
                if dp.iscanceled():
                        dp.close()
        if xbmcplugin.getSetting("Download Flv") == "true":
                dialog = xbmcgui.Dialog()
                path = dialog.browse(3, 'Choose Download Directory', 'files', '', False, False, '')
                Download(url, path + name + '.flv')
        liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        return ok

def addDir(name, url, mode, thumbnail):

        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo(type="Video", infoLabels={ "Title": name })
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok

params = get_params()
url = None
name = None
mode = None
try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass
print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
if mode == None or url == None or len(url) < 1:
        print "categories"
        CATS()
elif mode == 1:
        print "INDEX OF LINKS : " + url
        INDEX(url, name)
elif mode == 2:
        print "ALTERNATE VIDEO SOURCES: " + url
        ALTERNATE(url, name)
elif mode == 3:
        print "PARTS OF VIDEO: " + url
        PART(url, name)
elif mode == 4:
        print "EPISODES : " + url
        EPS(url, name)
elif mode == 5:
        print "VIDLINKS : " + url
        VIDLINK(url, name)
elif mode == 6:
        print "SEARCH  :" + url
        SEARCH()
elif mode == 7:
        print "LATEST  :" + url
        RSS(url)
elif mode == 8:
        print "LATEST  :" + url
        AZ(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
