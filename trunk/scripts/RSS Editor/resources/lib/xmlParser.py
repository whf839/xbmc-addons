import os
import xbmc
from xml.dom.minidom import parse, Document, _write_data, Node, Element

def writexml(self, writer, indent="", addindent="", newl=""):
    #credit: http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace/
    writer.write(indent+"<" + self.tagName)
    attrs = self._get_attributes()
    a_names = attrs.keys()
    a_names.sort()
    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        _write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
          and self.childNodes[0].nodeType == Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s"%(newl))
        for node in self.childNodes:
            node.writexml(writer,indent+addindent,addindent,newl)
        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
    else:
        writer.write("/>%s"%(newl))

# monkey patch to fix whitespace issues with toprettyxml
Element.writexml = writexml

class XMLParser:
    def __init__(self):
        self.RssFeedsPath = 'special://userdata/RssFeeds.xml'
        sane = self.checkRssFeedPathSanity()
        if sane: 
            self.feedsTree = parse(self.RssFeedsPath)
            self.feedsList = self.getCurrentRssFeeds()
        else:
            self.feedsList = False

    def checkRssFeedPathSanity(self):
        if os.path.isfile(self.RssFeedsPath):
            if not os.path.getsize(self.RssFeedsPath):
                return False
        else:
            return False
        return True
        
    def getCurrentRssFeeds(self):
        feedsList = dict()
        sets = self.feedsTree.getElementsByTagName('set')
        for i, s in enumerate(sets):
            feedsList['set'+str(i+1)] = list()
            feeds = s.getElementsByTagName('feed')
            for feed in feeds:
                feedsList['set'+str(i+1)].append({'url':feed.firstChild.toxml(), 'updateinterval':feed.attributes['updateinterval'].value})
        return feedsList

    def formXml(self):
        #create the document
        doc = Document()
        #create root element
        rssfeedsTag = doc.createElement('rssfeeds')
        doc.appendChild(rssfeedsTag)
        #create comments
        c1Tag = doc.createComment('RSS feeds. To have multiple feeds, just add a feed to the set. You can also have multiple sets.')
        c2Tag = doc.createComment('To use different sets in your skin, each must be called from skin with a unique id.')
        rssfeedsTag.appendChild(c1Tag)
        rssfeedsTag.appendChild(c2Tag)
        #since dicts aren't ordered, the keys need to be copied to a list then sorted them before creating the elements
        fl = list()
        for setNum in self.feedsList.keys():
            fl.append(setNum)
        fl.sort()
        #create set elements
        for setNum in fl:
            setTag = doc.createElement('set')
            setTag.setAttribute('id', setNum[3:])
            rssfeedsTag.appendChild(setTag)
            #create feed elements
            for feed in self.feedsList[setNum]:
                feedTag = doc.createElement('feed')
                feedTag.setAttribute('updateinterval', feed['updateinterval'])
                feedUrl = doc.createTextNode(feed['url'])
                feedTag.appendChild(feedUrl)
                setTag.appendChild(feedTag)
        return doc.toprettyxml(indent = '  ', encoding = 'UTF-8')

    def writeXmlToFile(self):
        print '[SCRIPT] RSS Ticker --> writing to %s' % (self.RssFeedsPath)
        xml = self.formXml()
        #hack for standalone attribute, minidom doesn't support DOM3
        xmlHeaderEnd = xml.find('?>')
        xml = xml[:xmlHeaderEnd]+' standalone="yes"'+xml[xmlHeaderEnd:]
        try:
            RssFeedsFile = open(self.RssFeedsPath, 'w')
            RssFeedsFile.write(xml)
            RssFeedsFile.close()
            print '[SCRIPT] RSS Ticker --> write success'
            self.refreshFeed()
        except IOError, error:
            print '[SCRIPT] RSS Ticker --> write failed', error
    
    def refreshFeed(self):
        #This probably makes more sense in the GUI class, but fuck it
        currentRev = int(xbmc.getInfoLabel('System.BuildVersion')[-5:])
        minRev = 21930
        if currentRev >= minRev:
            xbmc.executebuiltin('refreshrss()')
        else:
            xbmcgui.Dialog().ok(getLS(48), getLS(49))
