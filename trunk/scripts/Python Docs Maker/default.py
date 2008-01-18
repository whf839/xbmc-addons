import os
import xbmcgui
import xbmcplugin
import pydoc

dialog = xbmcgui.DialogProgress()
dialog.create('Python Docs Maker', 'Creating html pages in \\web\\python\\')

def makeDocDir():
  try:
    os.mkdir('q:\\web\\python')
  except:
    pass

makeDocDir()    
doc = pydoc.HTMLDoc()

f = open('Q:\\web\\python\\xbmc.html', 'w')
f.write(doc.document(xbmc))
f.close()
dialog.update(33)

f = open('Q:\\web\\python\\xbmcplugin.html', 'w')
f.write(doc.document(xbmcplugin))
f.close()
dialog.update(67)

f = open('Q:\\web\\python\\xbmcgui.html', 'w')
f.write(doc.document(xbmcgui))
f.close()

dialog.update(100)
dialog.close()

