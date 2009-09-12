import tbp_scraper
import xbmcgui
from xbmc import Language
from os import getcwd

#enable localization
getLS = Language(getcwd()).getLocalizedString

class GUI(xbmcgui.WindowXML):
    #BASE URL(S)
    TBPHOME = 'http://www.boston.com/bigpicture/'
    #Label Controls
    CONTROL_MAIN_IMAGE = 100
    #Label Actions
    ACTION_PREVIOUS_MENU = [9]
    ACTION_SHOW_INFO = [11]
    ACTION_EXIT_SCRIPT = [10, 13]

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self, *args, **kwargs)
        self.tbp = tbp_scraper.TBP()
    
    def onInit(self):
        self.getControl(1).setLabel(getLS(32000))
        self.getControl(2).setLabel(getLS(32001))
        self.showAlbums(self.TBPHOME)
        
    def onFocus(self, controlId):
        pass
    
    def onAction(self, action):
        if action in self.ACTION_SHOW_INFO:
            self.toggleInfo()
        elif action in self.ACTION_PREVIOUS_MENU:
            if self.getProperty('type') == 'album': #exit the script
                self.close()
            elif self.getProperty('type') == 'photo': #return to previous album
                self.showAlbums(self.TBPHOME)
        elif action in self.ACTION_EXIT_SCRIPT:
            self.close()

    def onClick(self, controlId):
        if controlId == self.CONTROL_MAIN_IMAGE:
            if self.getProperty('type') == 'album':
                self.showPhotos()
            elif self.getProperty('type') == 'photo':
                self.toggleInfo() 
    
    def getProperty(self, property, controlId=CONTROL_MAIN_IMAGE):
        """Returns a property of the selected item or "Default" if the call is made too early"""
        return self.getControl(controlId).getSelectedItem().getProperty(property)

    def toggleInfo(self):
        selectedControl = self.getControl(self.CONTROL_MAIN_IMAGE)
        if self.getProperty('showInfo') == 'false':
            for i in range(selectedControl.size()):
                selectedControl.getListItem(i).setProperty('showInfo', 'true')
        else:
            for i in range(selectedControl.size()):
                selectedControl.getListItem(i).setProperty('showInfo','false')
            
    def showPhotos(self): #the order is significant!
        link = self.getProperty('link')
        self.getControl(self.CONTROL_MAIN_IMAGE).reset() #Clear the old list of albums.
        self.tbp.getPhotos(link) # Get a list of photos from the link.
        self.showItems(self.tbp.photos, 'photo')
        
    def showAlbums(self, albumUrl):
        self.getControl(self.CONTROL_MAIN_IMAGE).reset() #This is necessary when returning from photos.
        self.tbp.getAlbums(albumUrl)
        self.showItems(self.tbp.albums, 'album')
    
    def showItems(self, itemSet, type):
        total = len(itemSet)
        for i, item in enumerate(itemSet):
            item['showInfo'] = 'true'
            item['type'] = type #TODO move this to scraper?
            item['title'] = item['title'] + ' (%s/%s)' % (i+1,total)
            self.addListItem(self.CONTROL_MAIN_IMAGE, item)
    
    def addListItem(self, controlId, properties):
        li = xbmcgui.ListItem(label=properties['title'].upper(), label2=properties['description'], iconImage=properties['pic'])
        for p in properties.keys():
            li.setProperty(p, properties[p])
        self.getControl(controlId).addItem(li)