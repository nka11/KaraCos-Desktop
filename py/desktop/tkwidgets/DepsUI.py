"""
    KaraCos-Desktop - web platform engine client for desktop users - http://karacos.org/
    Copyright (C) 2009-2010  Nicolas Karageuzian

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created on 26 juil. 2010

@author: KaragNi
"""
import Tkinter
import os
from setup.DepsManager import DepsManager
import desktop

class DepsUI(Tkinter.Frame):
    """
    Interface for dependencies management
    """
    
    def __init__(self,parent):
        """
        """
        Tkinter.Frame.__init__(self,parent)
        self.parent = parent
        self.thread = parent.thread
        self.toolbar = parent.toolbar
        conf_filename = os.path.join(desktop.Config()['rootdir'],'bin','py','desktop','conf','dependencies.conf')
        self.downloader = DepsManager(conf_filename) 
        
        self.initialize()
        
    def initialize(self):
        """
        """
        self.grid()
        rowid = 0
        for dependency in self.downloader.config.sections():
            dependencylabel = Tkinter.Label(self,text=dependency,anchor="w")
            dependencylabel.grid(column=0,row=rowid,sticky='EW')
            if self.downloader.config.has_option(dependency, 'archive_pylib'):
                depdir = os.path.join(desktop.Config()['rootdir'],'lib','python',self.downloader.config.get(dependency, 'py_dest'))
                if not os.path.exists(depdir):
                    button = Tkinter.Button(self, text='install python', width=10,command=self.install_python(dependency))
                    button.grid(column=1,row=rowid)
            rowid += 1
    
    def install_python(self,dependency):
        
        def install_dependency():
            print "Staring install of python dependency %s" % dependency
            self.downloader.install_dependency(dependency)
        return install_dependency
            