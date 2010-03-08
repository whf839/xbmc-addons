# orginal comment:
        # reversed napi 0.16.3.1
        # by gim,krzynio,dosiu,hash 2oo8.
        # last modified: 6-I-2oo8
        # 4pc0h f0rc3
        # POZDRAWIAMY NASZYCH FANOW!

import md5
import sys,urllib,os
import xbmc,xbmcgui
import shutil

def f(z):
        idx = [ 0xe, 0x3,  0x6, 0x8, 0x2 ]
        mul = [   2,   2,    5,   4,   3 ]
        add = [   0, 0xd, 0x10, 0xb, 0x5 ]

        b = []
        for i in xrange(len(idx)):
                a = add[i]
                m = mul[i]
                i = idx[i]

                t = a + int(z[i], 16)
                v = int(z[t:t+2], 16)
                b.append( ("%x" % (v*m))[-1] )

        return ''.join(b)

def Download(path):
        dp = xbmcgui.DialogProgress()
        dp.create("xnapi" )
        dp.update( 50, "Searching for subtitles...", " ", " " )
        
        d = md5.new();
        subtitlesCustomPath =  xbmc.executehttpapi('GetGuiSetting(3;subtitles.custompath)').replace("<li>", "")
        d.update(open(path,"rb").read(10485760))
        
        arch=xbmc.translatePath( os.path.join( "special://userdata/", "napisy.txt"))
        str = "http://napiprojekt.pl/unit_napisy/dl.php?l=PL&f="+d.hexdigest()+"&t="+f(d.hexdigest())+"&v=dreambox&kolejka=false&nick=&pass=&napios="+os.name
        subs=urllib.urlopen(str).read()

        if (subs[0:4]=='NPc0'):
                xbmcgui.Dialog().ok( "xnapi","No subtitles found.")
        else:
			file(arch,"wb").write(subs)
			if subtitlesCustomPath == "":                   #save in movie directory
				if (path[0:6]=="""rar://"""):              # playing rar file
					filename=(os.path.join((os.path.split(os.path.split(urllib.url2pathname(path))[0])[0])[6:],(os.path.split(path)[1])[:-3]+'txt'))#.replace('/','\\')
                                #remove rar://, get directory outside archive, add playing file name 
				else:
					filename=path[:-3]+'txt'
			else:
				filename=os.path.join(subtitlesCustomPath,os.path.split(urllib.url2pathname(path))[1][:-3]+'txt')
			if os.path.isfile(filename) == True:       # there already were subs
				filename=filename[:-4]+'-xnapi.txt'
				if os.path.isfile(filename) == True:
					dp.update( 75, "Replacing old subtitles...", " ", " " )
			shutil.copyfile(arch,filename)
	xbmcgui.Dialog().ok( "xnapi", "Subtitles extracted to: \n" +  os.path.dirname(filename))

