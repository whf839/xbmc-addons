import os
from xml.dom.minidom import parse, Document, _write_data, Node, Element

try:
    import xbmc
    import xbmcgui
except:
    xbmc = None


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
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            node.writexml(writer, indent+addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))

# monkey patch to fix whitespace issues with toprettyxml
Element.writexml = writexml


class XMLParser:

    def __init__(self):
        if xbmc:
            self.RssFeedsPath = 'special://userdata/RssFeeds.xml'
        else:
            self.RssFeedsPath = r'C:\Documents and Settings\Xerox\Application Data\XBMC\userdata\RssFeeds.xml'
        sane = self.checkRssFeedPathSanity()
        if sane:
            self.feedsTree = parse(self.RssFeedsPath)
            self.feedsList = self.getCurrentRssFeeds()
        else:
            self.feedsList = False
            print '[SCRIPT] RSS Editor --> Could not open ' + self.RssFeedsPath +'. Either the file does not exist, or its\
                size is zero.'

    def checkRssFeedPathSanity(self):
        if os.path.isfile(self.RssFeedsPath):
            #If the filesize is zero, the parsing will fail.  XBMC creates 
            if os.path.getsize(self.RssFeedsPath):
                return True

    def getCurrentRssFeeds(self):
        feedsList = dict()
        sets = self.feedsTree.getElementsByTagName('set')
        for s in sets:
            setName = 'set'+s.attributes["id"].value
            feedsList[setName] = {'feedslist':list(), 'attrs':dict()}
            #get attrs
            for attrib in s.attributes.keys():
                feedsList[setName]['attrs'][attrib] = s.attributes[attrib].value
            #get feedslist
            feeds = s.getElementsByTagName('feed')
            for feed in feeds:
                feedsList[setName]['feedslist'].append({'url':feed.firstChild.toxml(), 'updateinterval':feed.attributes['updateinterval'].value})
        return feedsList

    def formXml(self):
        """Form the XML to be written to RssFeeds.xml"""
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
        for setNum in sorted(self.feedsList.keys()):
            #create sets
            setTag = doc.createElement('set')
            #create attributes
            setTag.setAttribute('id', self.feedsList[setNum]['attrs']['id'])
            setTag.setAttribute('rtl', self.feedsList[setNum]['attrs']['rtl'])
            rssfeedsTag.appendChild(setTag)
            #create feed elements
            for feed in self.feedsList[setNum]['feedslist']:
                feedTag = doc.createElement('feed')
                feedTag.setAttribute('updateinterval', feed['updateinterval'])
                feedUrl = doc.createTextNode(feed['url'])
                feedTag.appendChild(feedUrl)
                setTag.appendChild(feedTag)
        return doc.toprettyxml(indent = '  ', encoding = 'UTF-8')

    def writeXmlToFile(self):
        print '[SCRIPT] RSS Editor --> writing to %s' % (self.RssFeedsPath)
        xml = self.formXml()
        #hack for standalone attribute, minidom doesn't support DOM3
        xmlHeaderEnd = xml.find('?>')
        xml = xml[:xmlHeaderEnd]+' standalone="yes"'+xml[xmlHeaderEnd:]
        try:
            RssFeedsFile = open(self.RssFeedsPath, 'w')
            RssFeedsFile.write(xml)
            RssFeedsFile.close()
            print '[SCRIPT] RSS Editor --> write success'
            self.refreshFeed()
        except IOError, error:
            print '[SCRIPT] RSS Editor --> write failed', error

    def refreshFeed(self):
        """Refresh XBMC's rss feed so changes can be seen immediately"""
        #TODO: after next stable is released, remove the minversion check.
        if xbmc:
            currentRev = int(xbmc.getInfoLabel('System.BuildVersion')[-5:])
            minRev = 21930
            if currentRev >= minRev:
                xbmc.executebuiltin('refreshrss()')
            else:
                xbmcgui.Dialog().ok(getLS(48), getLS(49))
        else:
            print 'kthx'