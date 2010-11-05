import urllib,urllib2,re
from BeautifulSoup import BeautifulSoup
import xbmcplugin,xbmcgui
from datetime import datetime,timedelta

class JournaalItem:
	_itemUrl=""
	_caption=""
	_image=""
	_flv=""
	
	def __init__(self,url,caption,image):
		self._itemUrl=url
		self._caption=caption
		self._image=image
			
	def get_Caption(self):
		return self._caption
	
	Caption = property(get_Caption)

	def get_Image(self):
		return self._image
	
	Image = property(get_Image)
	
	def get_Flv(self):
		if (self._flv==""):
			request = urllib2.Request(self._itemUrl)
			request.add_header('User-Agent',BASE_URL)
			response = urllib2.urlopen(request)
			soup = BeautifulSoup(response.read())
			response.close()
			script =  soup.find("script",type="text/javascript",text=re.compile("file:"))
			flashxml_link = re.search("file:\s'(.*?)'",script).group(1)
			self._flv = self.__FlvFromXml(flashxml_link)
		return self._flv
			
	def __FlvFromXml(self,url):
		request = urllib2.Request(url)
		request.add_header('User-Agent',BASE_URL)
		response = urllib2.urlopen(request)
		soup = BeautifulSoup(response.read())
		response.close()
	
		return soup.find("location").string
		
	Flv = property(get_Flv)

class JournaalIndex:
	_url = ""
	def __init__(self,url):
		self._url = url
	
	def Retrieve(self):
		request = urllib2.Request(url)
		request.add_header('User-Agent',USER_AGENT)
		response = urllib2.urlopen(request)
		soup = BeautifulSoup(response.read())
		response.close()
		
		#Retrieve the 'article' div.	
		article = soup.find("div",id="article")

		#Retrieve the items within the 'article' div. (li)
		items = article.findAll("li")
		#print len(items)
		
		col_JItems =[]
		
		for item in items:
			#For each item in the article retrieve the image, caption and link.
			link = BASE_SERVER + item.find("a").get("href")
			caption = item.find("a").string
			image = item.find("img").get("src")
			
			#Create new JournaalItem object
			ji = JournaalItem(link,caption,image)
			col_JItems.append(ji)
		
		return col_JItems

def CreateFolders():
	today = datetime.now()
	day = timedelta(days=1)
	for i in range(0, MAX_PREV_DAYS):
		record = (today-(day*i)).strftime("%Y-%m-%d")
		url = BASE_URL + "pagina/1/datum/" + record + "/"
		if (i==0):
			addDir("Vandaag",url,1,"")
		else:
			addDir(record,url,1,"")
			
def CreateIndex(url):
	JIndex = JournaalIndex(url)
	colJournaal = JIndex.Retrieve()
	for Journaal in colJournaal:
		addLink(Journaal.Caption,Journaal.Flv,Journaal.Image,len(colJournaal))
		
def addLink(name,url,iconimage,total):
	retval=True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	retval = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return retval

def addDir(name,url,mode,iconimage):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
	retval = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	retval = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return retval

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
					params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
							param[splitparams[0]]=splitparams[1]
                                
	return param


#Try to get parameters from the XBMC parent.	
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

BASE_SERVER = 'http://nos.nl'
BASE_URL = BASE_SERVER + '/nieuws/video-en-audio/journaal/'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3'
MAX_PREV_DAYS = 7

if mode==None or url==None or len(url)<1:
	#Create the folder index (based on date)
	CreateFolders()
       
elif mode==1:
	#Create the item index (based on current list items per date)
	CreateIndex(url)
        
#elif mode==2:
        #print ""+url
        #VIDEOLINKS(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))