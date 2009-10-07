import urllib
import os
import sys
import xbmc
import xbmcgui

#enable localization
getLS = xbmc.Language(os.getcwd()).getLocalizedString
scriptName = sys.modules['__main__'].__scriptname__

class Download:

    def __init__(self, photos, downloadPath):
        self.pDialog = xbmcgui.DialogProgress()
        self.pDialog.create(getLS(32000))
        downloadPath = xbmc.translatePath(downloadPath)

        for i, photo in enumerate(photos):
            self.url = photo['pic']
            #unicode causes problems here, convert to standard str
            self.filename = str(self.url.split('/')[-1])
            foldername = str(self.url.split('/')[-2])
            self.fullDownloadPath = os.path.join(downloadPath, foldername, self.filename)
            print '[%s] %s : Attempting to download %s of %s' % (scriptName, __name__, i+1, len(photos))
            print '[%s] %s --> %s\n' %  (scriptName, self.url, self.fullDownloadPath)

            if self.checkPath(downloadPath, foldername, self.filename):
                try:
                    re = urllib.urlretrieve(self.url, self.fullDownloadPath, reporthook = self.showdlProgress)
                    print '[%s] Download Success!' % (scriptName)
                except IOError, e:
                    print e
                    self.pDialog.close()
                    dialog = xbmcgui.Dialog()
                    dialog.ok('Error', str(i)+' of '+str(len(photos))+'\n'+self.url, e.__str__())
                    break
                if self.pDialog.iscanceled():
                    self.pDialog.close()
                    break
        #close the progress dialog
        self.pDialog.close()

    def showdlProgress(self, count, blockSize, totalSize):
        percent = int(count*blockSize*100/totalSize)
        self.pDialog.update(percent, '%s %s' % (getLS(32023), self.url), '%s %s' % (getLS(32024), self.fullDownloadPath))
    
    def checkPath(self, path, folder, filename):
        if os.path.isdir(path):
            if os.path.isdir(os.path.join(path, folder)):
                if os.path.isfile(os.path.join(path, folder, filename)):
                    if not os.path.getsize(os.path.join(path, folder, filename))>0:
                        return True #overwrite empty files, #skip others.
                else:
                    return True
            else:
                os.mkdir(os.path.join(path, folder))
                self.checkPath(path, folder, filename) #check again after creating directory
