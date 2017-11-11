#!/usr/bin/python
# -*- coding: utf-8 -*-

# licence GPL 2
# copyright easyw

from __future__ import print_function
# This must be the first statement before other statements.
# You may only put a quoted or triple quoted string, 
# Python comments, other future statements, or blank lines before the __future__ line.


__version__='1.2.2'

import codecs
import re,os, sys

import urllib2
import ssl

try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__

def print(*args, **kwargs):
    """My custom print() function."""
    # Adding new arguments to the print function signature 
    # is probably a bad idea.
    # Instead consider testing if custom argument keywords
    # are present in kwargs
    for arg in args:
        _consoleText.AppendText(str(arg)+' ')

    if not kwargs.get('noreturn',None):
        _consoleText.AppendText('\n')
    # __builtin__.print('My overridden print() function!')
    # return __builtin__.print(*args, **kwargs)


import pcbnew
import wx


def FindWindowByTitle(title,startwindow=None):
    """UI convenience function to find the GUI window by the beginning of its title.
       If startwindow is unspecified, search from the top level windows."""
    if startwindow is None:
        startwindow = wx.GetTopLevelWindows()
    window = filter(lambda w: w.GetTitle().startswith(title), startwindow)
    if len(window) != 1:
        raise Exception("Cannot find %s window from title."%title)        
    return window[0]

def FindWindowByName(name,startwindow=None):
    """UI convenience function to find the GUI window by the beginning of its name.
       If startwindow is unspecified, search from the top level windows."""
    if startwindow is None:
        startwindow = wx.GetTopLevelWindows()
    window = filter(lambda w: w.Name.startswith(name), startwindow)
    if len(window) != 1:
        raise Exception("Cannot find %s window from name."%name)
    return window[0]


class aplugin(pcbnew.ActionPlugin):
    """implements ActionPlugin"""
    def __init__(self):
        self.defaults()
        
    def defaults(self):
        self.name = "Update 3d Model Library"
        self.category = "Library"
        self.description = "Update pcb referenced 3d libraries."
    # def Run(self,event):
        # _consoleText = FindWindowByName("text",
        # startwindow=FindWindowByName("KicadFrame").GetChildren())
        
        # _consoleText.AppendText("Instance Hello!")

instance = aplugin()
_pcbnewWindow = None
_consoleText = None
kicad_ver = None
def InstallMenuItem():
    """The main function to run when imported. Creates the menu
       and a variety of variables pointing to the graphic windows needed
       later in the code."""
    global instance, _pcbnewWindow, _consoleText, kicad_ver
    MenuItemName = instance.name # "Update 3d Model Library"
    _pcbnewWindow = FindWindowByTitle("Pcbnew")
    _consoleText = FindWindowByName("text",
        startwindow=FindWindowByName("KicadFrame").GetChildren())
    #_consoleText.AppendText("Starting Run()...\n")
    menuBar = _pcbnewWindow.MenuBar
    # add the menu item under Tools menu
    
    toolsMenu = menuBar.GetMenu(menuBar.FindMenu("Tools"))
    existingItem = toolsMenu.FindItem("External Plugins")
    # If the External Plugins menu exists, then this was loaded as an ActionScript
    if existingItem != -1:
        kicad_ver = 5 # or nightly
        return
    else:
        kicad_ver = 4
    
    existingItem = toolsMenu.FindItem(MenuItemName)
    if existingItem != -1:
        _consoleText.AppendText("Deleting existing menuitem.\n")
        toolsMenu.Delete(existingItem)
    MenuItem = toolsMenu.Append(wx.ID_ANY, MenuItemName)
    
    if hasattr(instance,'Run'):
        run = instance.Run
    else:
        run = Run
    breturn = _pcbnewWindow.Bind(wx.EVT_MENU, run, MenuItem)
    # _id = wx.NewId()
    # subMenuObject.Append(_id, title, statustext)
    # wx.EVT_MENU(self, _id, action)
    _consoleText.AppendText('Bind returned:%s'%str(breturn))
    _consoleText.AppendText('Finished Installation')
    

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


KISYS3DMOD=ur"C:\KiCad-stable\share\kicad\modules\packages3d"
KISYS3DMOD=ur"C:\Program Files (x86)\KiCad\share\kicad\modules\packages3d1"
KISYS3DMOD=KISYS3DMOD.replace('\\','/')

global fileOut

fileOut=ur"log-3Dmodels.txt"
fileOut=fileOut.replace('\\','/')

filename=ur"C:\Temp\blinky-dev.kicad_pcb"
filename=filename.replace('\\','/')


# import argparse

# args=sys.argv
#for a in args:
#    print(a)

    
def collect_models(fn, kv, k3d, fupd):
    """collect models from GH for the present pcb"""
    
    global fileOut
    
    overwrite=False
    if fupd=='/u':
        overwrite=True
    filename=fn
    KISYS3DMOD=k3d
    kicad_version=kv
    
    txtFile = codecs.open(filename, mode='rb', encoding='utf-8', errors='replace', buffering=1)  #test maui utf-8
    content = txtFile.readlines()
    content.append(" ")
    txtFile.close()
    data=''.join(content)
    
    model_list = re.findall(r'\(model\s+(.+?)\.wrl',data)
    #model_list = re.findall(r'\(model\s+(.+?)\.wrl',data, re.MULTILINE|re.DOTALL)
    model_list2 = re.findall(r'\(model\s+(.+?)\.WRL',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.stp',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.step',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.STP',data)
    model_list=model_list+model_list2
    model_list2 = re.findall(r'\(model\s+(.+?)\.STEP',data)
    model_list=model_list+model_list2
    
    #print(model_list)
    
    fOut=codecs.open(fileOut, mode='wb', encoding='utf-8', errors='replace', buffering=1)
    
    parsed=[]
    fOut.write(u'parsed '+str(len(model_list))+u' model(s)'+ os.linesep)
    for d in model_list:        
        found=False
        d1=d.replace('\\','/')
        #d1=d1.rstrip('/') 
        if 'KISYS3DMOD' in d1:
            d1=d1.lstrip('${KISYS3DMOD}/')
            d1=d1.lstrip('/')
        d=d1
        local=False
        #print(d1)
        if 'KIPRJMOD' in d1:
            #print('LOCAL')
            #stop
            local=True
            d1=d1.lstrip('${KIPRJMOD}')
            d1=d1.lstrip('/')
            print(d1)
        d=d1
        if d not in parsed:
            if local:
                fOut.write(d+u'.wrl'+ os.linesep)
                directory=d1
                prefix=""
            else:
                fOut.write(KISYS3DMOD+os.sep+d+u'.wrl'+ os.linesep)
                directory=KISYS3DMOD+os.sep+d1
                prefix=KISYS3DMOD+os.sep
            #print(d1)
            ##stop
            #print(d1.rfind('/'))
            #stop
            if d1.rfind('/')!=-1:
                d1=d1[0:d1.rindex('/')]
            #else:
                
            #print('d, d1, dir')
            #print(d)
            #print(d1)
            #print(directory)
            #stop
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except:
                    print('you need Administrative rights')
                    continue
            if os.path.exists(prefix+d+u'.wrl'):
                found=True
                print(u'exists '+d+u'.wrl')
                #fOut.write(d)
                #fOut.write('\n')
            if not found or overwrite:
                fileDest=prefix+d+u'.wrl'
                d1=d.replace('\\','/')
                try:
                    response = urllib2.urlopen(github_src+d1+u'.wrl', context=ctx)
                    myfile = response.read()
                    f_dest=codecs.open(fileDest, mode='wb', encoding='utf-8', errors='replace', buffering=1)
                    f_dest.write(myfile)
                    print(fileDest + ur' written')
                except:
                    print('error file not found')
                    print(github_src+d1+u'.wrl')
                    print('or you may need Administrative rights')
                #print(myfile)
                
            found=False
            if os.path.exists(prefix+d+u'.step') or os.path.exists(prefix+d+u'.STEP') or \
                                                os.path.exists(prefix+d+u'.stp') or os.path.exists(prefix+d+u'.STP'):
                print(u'exists '+d+u'.step')
                #fOut.write(d)
                #fOut.write('\n')
                found=True
            if not found or overwrite:
                fileDest=prefix+d+u'.step'
                d1=d.replace('\\','/')
                #print(github_src+d1+u'.step')
                try:
                    response = urllib2.urlopen(github_src+d1+u'.step', context=ctx)
                    myfile = response.read()
                    f_dest=codecs.open(fileDest, mode='wb', encoding='utf-8', errors='replace', buffering=1)
                    f_dest.write(myfile)
                    print(fileDest + ur' written')
                except:
                    print('error file not found')
                    print(github_src+d1+u'.step')
                    print('or you may need Administrative rights')
                #print(myfile)
                #fOut.write('\n')
            parsed.append(d)
        
    fOut.close()
    #print(model_list2)
##
kicad_ver = None
# Function to be executed when menu item is clicked.
def Run(event):
    global kicad_ver,KISYS3DMOD
    #if len(args) >= 4:
    #KISYS3DMOD=args[1]
    #kicad_ver=None #args[2]
    filename=pcbnew.GetBoard().GetFilename() # args[3]
    force_upd=None
    # if len(args) == 5:
        # force_upd=args[4]
    # print(args[1],args[2],args[3])
    if force_upd is not None:
        print()
        print('forcing download and override all 3D models')
    else:    
        print()
    if kicad_ver=='4':
        github_src=ur'https://github.com/KiCad/kicad-library/raw/master/modules/packages3d/'
        gh_base=ur'https://github.com/KiCad/kicad-library/modules/packages3d/'
    else:
        github_src=ur'https://github.com/KiCad/kicad-packages3D/raw/master/'
        gh_base=ur'https://github.com/KiCad/kicad-packages3D/'
    print()
    print('collecting packages from:')
    print(gh_base)
    print()
    
    collect_models(filename, kicad_ver, KISYS3DMOD, force_upd)


# invoke only when run as a script, not as import
if __name__ == "__main__":
    InstallMenuItem()
else:
    # The above should work (currently untested) with Action Menu
    # (KiCAD compiled with KICAD_SCRIPTING_ACTION_MENU)
    # However, in KiCAD builds without ACTION_MENU enabled, the following
    # is a workaround that allows "import kipadcheck" to enable the menu item.
    InstallMenuItem()

# register through Action Script when imported
instance.register()
#instance.Run()
