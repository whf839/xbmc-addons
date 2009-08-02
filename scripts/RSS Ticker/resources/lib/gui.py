"""
    Manager for XBMC's RSS Ticker
    by rwparris2
"""
import xbmc
import xbmcgui
import os
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

#enable localization
getLS = xbmc.Language(os.getcwd()).getLocalizedString

class GUI(xbmcgui.WindowXMLDialog):
    ACTION_CANCEL_DIALOG = (9, 10,)

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)

    def onInit(self):
        self.parser = XMLParser()
        if not self.parser.feedsList:
            xbmcgui.Dialog().ok(getLS(40)+'RssFeeds.xml', 'RssFeeds.xml'+getLS(41), getLS(42), getLS(43))
            self.closeDialog()
        self.setNum = 'set1'
        self.showDialog()

    def showDialog(self):
        self.getControl(2).setLabel(getLS(0)) #Header
        self.getControl(11).setLabel(getLS(1)) #Change Set Button
        self.getControl(13).setLabel(xbmc.getLocalizedString(15019)+getLS(4)) #Add Button
        self.getControl(14).setLabel(xbmc.getLocalizedString(1210)+getLS(4)) #Remove Button
        self.updateFeedsList()
        self.setFocus(self.getControl(10))
        
    def closeDialog(self):
        self.close()

    def onClick(self, controlId):
        if controlId == 10: #List Item was clicked
            #set item
            if self.getControl(controlId).getSelectedItem().getLabel().startswith('set'):
                self.setNum = self.getControl(controlId).getSelectedItem().getLabel()
                self.updateFeedsList()
                self.getControl(13).setLabel(xbmc.getLocalizedString(15019)+getLS(4)) #Add Button
                self.getControl(14).setLabel(xbmc.getLocalizedString(1210)+getLS(4)) #Remove Button
            #feed item
            else:
                position = self.getControl(controlId).getSelectedPosition()
                oldUrl = self.parser.feedsList[self.setNum][position]['url']
                oldUpdateInterval = self.parser.feedsList[self.setNum][position]['updateinterval']
                newUrl, newUpdateInterval = self.getNewFeed(oldUrl, oldUpdateInterval)
                if newUrl:
                    self.parser.feedsList[self.setNum][position] = {'url':newUrl, 'updateinterval':newUpdateInterval}
                self.updateFeedsList()
        elif controlId == 11: #Change Set Button
            self.setNum = self.updateSetsList()
            #TODO: FIGURE OUT HOW TO ADD IT BACK
            #self.removeControl(self.getControl(11))
            self.setFocus(self.getControl(10))
            self.getControl(13).setLabel(xbmc.getLocalizedString(15019)+getLS(5)) #Add Button
            self.getControl(14).setLabel(xbmc.getLocalizedString(1210)+getLS(5)) #Remove Button
            xbmcgui.Dialog().ok(getLS(20), getLS(21), getLS(22), getLS(23))
        elif controlId == 13: #Add Button
            if self.getControl(10).getSelectedItem().getLabel().startswith('set'):
                self.getNewSet()
                self.updateSetsList()
            else:
                newUrl, newUpdateInterval = self.getNewFeed()
                if newUrl:
                    self.parser.feedsList[self.setNum].append({'url':newUrl, 'updateinterval':newUpdateInterval})
                self.updateFeedsList()
        elif controlId == 14: #Remove Button
            if self.getControl(10).getSelectedItem().getLabel().startswith('set'):
                self.removeSet()
                self.updateSetsList()
            else:
                self.removeFeed()
                self.updateFeedsList()
        elif controlId == 18: #OK Button
            self.parser.writeXmlToFile()
            self.closeDialog()
        elif controlId == 19: #Cancel Button
            self.closeDialog()
            
    def onAction(self, action):
        if action in self.ACTION_CANCEL_DIALOG:
            self.closeDialog()
            
    def onFocus(self, controlId):
        pass
        
    def getNewSet(self):
        #find highest numbered set, then add 1
        setNumList = list()
        for setNum in self.parser.feedsList.keys():
            setNumList.append(int(setNum[3:]))
        newSetNum = 'set'+str(max(setNumList)+1)
        self.parser.feedsList[newSetNum] = [{'url':'http://', 'updateinterval':'30'}]
    
    def removeSet(self):
        setNum = self.getControl(10).getSelectedItem().getLabel()
        if setNum == 'set1':
            if xbmcgui.Dialog().yesno(getLS(45), getLS(46), getLS(47)):
                self.parser.feedsList[setNum] = [{'url':'http://feeds.feedburner.com/xbmc', 'updateinterval':'30'}]
        else:
            del self.parser.feedsList[setNum]
    
    def updateSetsList(self):
        self.getControl(10).reset()
        for setNum in self.parser.feedsList.keys():
            self.getControl(10).addItem(setNum)
            self.getControl(3).setLabel(getLS(24))
    
    def removeFeed(self):
        position = self.getControl(10).getSelectedPosition()
        self.parser.feedsList[self.setNum].remove(self.parser.feedsList[self.setNum][position])
        #add empty feed if last one is deleted
        if len(self.parser.feedsList[self.setNum]) < 1:
            self.parser.feedsList[self.setNum] = [{'url':'http://', 'updateinterval':'30'}]
        
    def getNewFeed(self, url = 'http://', newUpdateInterval = '30'):
        kb = xbmc.Keyboard(url, getLS(12), False)
        kb.doModal()
        if kb.isConfirmed():
            newUrl = kb.getText()
            newUpdateInterval = xbmcgui.Dialog().numeric(0, getLS(13), newUpdateInterval)
        else:
            newUrl = None
        return newUrl, newUpdateInterval
    
    def updateFeedsList(self):
        self.getControl(10).reset()
        for feed in self.parser.feedsList[self.setNum]:
            self.getControl(10).addItem(feed['url'])
        if self.setNum == 'set1':
            self.getControl(3).setLabel(getLS(14) % (''))
        else:
            self.getControl(3).setLabel(getLS(14) % ('('+self.setNum+')'))

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

