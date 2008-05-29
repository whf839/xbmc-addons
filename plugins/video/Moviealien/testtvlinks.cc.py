import urllib,re,urllib2


res=[]
f=urllib.urlopen("http://www.moviealien.com/play.php?v=v619569zxaKAG7q&s=veo")
a=f.read()
f.close()
p=re.compile(r'<embed src="http://www.veoh.com\/.+?.swf\?permalinkId=(.+?)\&id=.+?player=videodetailsembedded&videoAutoPlay=0"')
match=p.findall(a)
for a in match:
   res.append(a)
        
        
   
