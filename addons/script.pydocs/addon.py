## PyDocs & PyPredefs Printer

import os
import resources.lib.pydoc as pydoc
import resources.lib.pypredefcom as pypredefcomp
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs


class DocsPrinter:

    def __init__(self):
        # get Addon object
        self.Addon = xbmcaddon.Addon(id="script.pydocs")
        # get user preferences
        self.doc_path = self.Addon.getSetting("doc_path")
        self.include_pydocs = (self.Addon.getSetting("include_pydocs") == "true")
        self.include_pypredefs = (self.Addon.getSetting("include_pypredefs") == "true")

    def print_docs(self):
        # get location if none set
        if (not self.doc_path):
            self.doc_path = self._get_browse_dialog(self.doc_path, self.Addon.getLocalizedString(30110))
        # if a valid doc_path create docs
        if (self.doc_path):
            # show feedback
            pDialog = xbmcgui.DialogProgress()
            pDialog.create(self.Addon.getAddonInfo("Name"))
            # set the doc_path setting in case the browse dialog was used
            self.Addon.setSetting("doc_path", self.doc_path)
            # modules
            modules = [ "xbmc", "xbmcgui", "xbmcplugin", "xbmcaddon", "xbmcvfs" ]
            # enumerate thru and print our help docs
            for count, module in enumerate(modules):
                # include PyDocs
                if (self.include_pydocs):
                    # set correct path
                    _path = self._make_path(module, u"PyDocs", u".html")
                    # only need to print doc if we have a valid dir
                    if (_path is not None):
                        # update dialog
                        pDialog.update(count * (100 / len(modules)), self.Addon.getLocalizedString(30711).format(msg="{module}.html PyDoc".format(module=module)), self.Addon.getLocalizedString(30712).format(msg=_path))
                        try:
                            # get our document object
                            doc = pydoc.HTMLDoc()
                            # print document
                            open(_path, "w").write(doc.document(eval(module)))
                        except Exception as error:
                            # oops
                            xbmc.log("An error occurred saving {module}.html PyDoc! ({error})".format(module=module, error=error), xbmc.LOGERROR)

                # include PyPredefs
                if (self.include_pypredefs):
                    # set correct path
                    _path = _path = self._make_path(module, u"PyPredefs", u".pypredef")
                    # only need to print doc if we have a valid dir
                    if (_path is not None):
                        # update dialog
                        pDialog.update(count * (100 / len(modules)), self.Addon.getLocalizedString(30711).format(msg="{module}.pypredef PyPredef".format(module=module)), self.Addon.getLocalizedString(30712).format(msg=_path))
                        try:
                            # get our file object
                            predefcomf = open(_path, "w")
                            # print document
                            pypredefcomp.pypredefmodule(predefcomf, eval(module))
                            # close file
                            predefcomf.close();
                        except Exception as error:
                            # oops
                            xbmc.log("An error occurred saving {module}.pypredef PyPredef! ({error})".format(module=module, error=error), xbmc.LOGERROR)

            #close dialog
            pDialog.update(100)
            pDialog.close()

    def _make_path(self, module, doc_type, ext):
        # set correct path
        _path = xbmc.validatePath(xbmc.translatePath(os.path.join(self.doc_path, doc_type))).decode("UTF-8")
        try:
            # make dir if it doesn't exist
            if (not xbmcvfs.exists(_path)):
                xbmcvfs.mkdir(_path)
        except:
            # oops
            xbmc.log("An error occurred making dir for {path}! ({error})".format(module=module, error=error), xbmc.LOGERROR)
            return None
        else:
            # return full filepath
            return os.path.join(_path, u"{module}{ext}".format(module=module, ext=ext))

    def _get_browse_dialog(self, default="", heading="", dlg_type=3, shares="files", mask="", use_thumbs=False, treat_as_folder=False):
        """
            shows a browse dialog and returns a value
            - 0 : ShowAndGetDirectory
            - 1 : ShowAndGetFile
            - 2 : ShowAndGetImage
            - 3 : ShowAndGetWriteableDirectory
        """
        dialog = xbmcgui.Dialog()
        value = dialog.browse(dlg_type, heading, shares, mask, use_thumbs, treat_as_folder, default)
        return value


if (__name__ == "__main__"):
    # print the documents
    DocsPrinter().print_docs()
