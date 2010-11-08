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

import tkwidgets

class DesktopUI(Tkinter.Tk):
    '''
    classdocs
    '''


    def __init__(self,parent,thread):
        '''
        Constructor
        '''
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.thread = thread
        self.initialize()
    
    def initialize(self):
        self.grid()
        menu = Tkinter.Menu(self)
        menu.add_command(label="KaraCos-Desktop")
        self.config(menu=menu)
        self.resizable(True,False)
        self.toolbar = tkwidgets.ToolBar(self)
        self.content = Tkinter.Frame(self)
        self.content.thread = self.thread
        self.content.toolbar = self.toolbar
        self.content.grid(column=0,row=1,sticky='EW')
        self.grid_columnconfigure(0,weight=1)
    
        
    def OnPressEnter(self):
        """
        """