import urllib
import urllib2
from BeautifulSoup    import BeautifulStoneSoup

u = urllib2.urlopen('http://api.cheezburger.com/xml/category/Cats/lol/random/20')
d = u.read()
u.close()

soup = BeautifulStoneSoup(d)

for s in soup.findAll('picture'):
 print s.title.string
 print s.fulltext.string
 print s.lolimageurl.string
