"""
    Manager for XBMC's RSS Ticker
    by rwparris2
"""
import xbmc
import xbmcgui
import os

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


