from urlparse import urlparse
import wx
import gui
import os
import globalVars
import treeInterceptorHandler
import configobj
import api

# from logHandler import log

class customLabels():
        
    @classmethod
    def addLabel(cls,filename,customLabelKey):
        if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "webLabels")):
            os.makedirs(os.path.join(globalVars.appArgs.configPath, "webLabels"))
        config = configobj.ConfigObj(os.path.join(globalVars.appArgs.configPath, "webLabels\%s" % filename))
        try:
            defaultCustomLabel=config[customLabelKey]
        except Exception as e:
            defaultCustomLabel=u""
        if customLabelKey:
            d = wx.TextEntryDialog(gui.mainFrame, 
            # Translators: Dialog text for 
            _("Custom Label Edit"),
            _("Custom Label"),
            defaultValue=defaultCustomLabel,
            style=wx.TE_MULTILINE|wx.OK|wx.CANCEL)
            def callback(result):
                if result == wx.ID_OK:
                    config[customLabelKey] = unicode(d.Value)
                    config.write()
            gui.runScriptModalDialog(d, callback)
        
    @classmethod
    def getFilenameFromElementDomain(cls,weblink):
        parsed_uri = urlparse( weblink )
        domain='{uri.netloc}'.format(uri=parsed_uri)
        domain=domain.replace('.','_')
        domain=domain.replace(':','_')
        domain=domain.replace('\\','_')
        filename=domain+'.ini'
        return filename
    
    @classmethod
    def getCustomLabel(cls,filename,nameAttribute):
        config = configobj.ConfigObj(os.path.join(globalVars.appArgs.configPath, "webLabels\%s" % filename))
        try:
            for k,v in config.iteritems():
                if (k==nameAttribute):
                    return v
        except Exception as e:
            pass