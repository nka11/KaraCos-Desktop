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
from ProxySetup import ProxySetup
from DepsUI import DepsUI
from SshUi import SshUi
class ToolBar(Tkinter.Frame):
    def __init__(self,parent):
        """
        """
        Tkinter.Frame.__init__(self,parent)
        import utils.logger
        self.log = utils.logger.get_logger(self.__class__.__name__)
        self.parent = parent
        self.thread = parent.thread
        self.active = None
        self.initialize()

    def initialize(self):
        """
        """
        self.grid()
        colid = 0
        self.proxybutton = Tkinter.Button(self, text="Proxy [OFF]", width=10, command=self.proxy_setup)
        self.proxybutton.grid(column=colid,row=0)
        colid += 1
        self.depsbutton = Tkinter.Button(self, text="Dependencies", width=10, command=self.dependencies)
        self.depsbutton.grid(column=colid,row=0)
        colid += 1
        self.sshbutton = Tkinter.Button(self, text="ssh", width=10, command=self.ssh_tunnel)
        self.sshbutton.grid(column=colid,row=0)

    def proxy_setup(self,*args,**kw):
        """
        """
        if self.active:
            self.active.grid_forget()
        self.active = ProxySetup(self.parent.content)
        self.active.grid(column=0,row=0)

    def dependencies(self,*args,**kw):
        """
        """
        if self.active:
            self.active.grid_forget()
        self.active = DepsUI(self.parent.content)
        self.active.grid(column=0,row=0)
    def ssh_tunnel(self):
        ""
        if self.active:
            self.active.grid_forget()
        self.active = SshUi(self.parent.content)
        self.active.grid(column=0,row=0)