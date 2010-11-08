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
import utils.ntlmaps
import desktop

class ProxySetup(Tkinter.Frame):
    def __init__(self,parent):
        """
        """
        Tkinter.Frame.__init__(self,parent)
        self.parent = parent
        self.thread = parent.thread
        self.toolbar = parent.toolbar
        
        self.initialize()
        
    def initialize(self):
        """
        """
        self.grid()
        rowid = 0
        self.useproxyvar = Tkinter.BooleanVar()
        self.useproxy = Tkinter.Checkbutton(self, text="Use proxy", variable=self.useproxyvar)
        self.useproxy.grid(column=0,row=rowid,sticky='EW')
        rowid += 1
        
        proxylabel = Tkinter.Label(self,text="Proxy Host",anchor="w")
        proxylabel.grid(column=0,row=rowid,sticky='EW')
        self.proxyentryvar = Tkinter.StringVar()
        self.proxyentry = Tkinter.Entry(self,textvariable=self.proxyentryvar)
        self.proxyentry.grid(column=1,row=rowid,sticky='EW')
        self.proxyentry.bind("<Return>", self.OnPressEnter)
        
        rowid += 1
        proxyportlabel = Tkinter.Label(self,text="Proxy Host",anchor="w")
        proxyportlabel.grid(column=0,row=rowid,sticky='EW')
        self.proxyportvar = Tkinter.StringVar()
        self.proxyportentry = Tkinter.Entry(self,textvariable=self.proxyportvar)
        self.proxyportentry.grid(column=1,row=rowid,sticky='EW')
        self.proxyportentry.bind("<Return>", self.OnPressEnter)
        
        rowid += 1
        self.usentlmvar = Tkinter.BooleanVar()
        self.usentlm = Tkinter.Checkbutton(self, text="Use NTLM", variable=self.usentlmvar)
        self.usentlm.grid(column=0,row=rowid,sticky='EW')
        
        rowid += 1
        
        domainlabel = Tkinter.Label(self,text="domain",anchor="w")
        domainlabel.grid(column=0,row=rowid,sticky='EW')
        self.domainvar = Tkinter.StringVar()
        self.domainentry = Tkinter.Entry(self,textvariable=self.domainvar)
        self.domainentry.grid(column=1,row=rowid,sticky='EW')
        self.domainentry.bind("<Return>", self.OnPressEnter)
        rowid += 1
        userlabel = Tkinter.Label(self,text="username",anchor="w")
        userlabel.grid(column=0,row=rowid,sticky='EW')
        self.uservar = Tkinter.StringVar()
        self.userentry = Tkinter.Entry(self,textvariable=self.uservar)
        self.userentry.grid(column=1,row=rowid,sticky='EW')
        self.userentry.bind("<Return>", self.OnPressEnter)
        rowid += 1
        passwordlabel = Tkinter.Label(self,text="password",anchor="w")
        passwordlabel.grid(column=0,row=rowid,sticky='EW')
        self.passwordvar = Tkinter.StringVar()
        self.passwordentry = Tkinter.Entry(self,textvariable=self.passwordvar,show="*")
        self.passwordentry.grid(column=1,row=rowid,sticky='EW')
        self.passwordentry.bind("<Return>", self.OnPressEnter)
        rowid += 1
        button_text = "Start Proxy"
        if self.is_proxy_started():
            button_text ="Stop Proxy" 
        self.toggleButton = Tkinter.Button(self, text=button_text, width=10, command=self.OnPressToggle)
        self.toggleButton.grid(column=0,row=rowid)
        
        
    def is_proxy_started(self):
        __is_proxy_started__ = False
        if 'proxy' in self.thread.__dict__:
            if self.thread.proxy != None:
                assert isinstance(self.thread.proxy,utils.ntlmaps.Proxy)
                if self.thread.proxy.is_alive():
                    __is_proxy_started__ = True 
        return __is_proxy_started__
    
    def OnPressEnter(self,*args,**kw):
        """
        """
    
    def OnPressToggle(self,*args,**kw):
        
        if self.is_proxy_started():
            self.stop_ntlmProxy()
            self.toggleButton.config(text="Start Proxy")
            self.toolbar.proxybutton.config(text="Proxy [OFF]")
        else:
            if self.useproxyvar.get():
                self.start_ntlmProxy()
                self.toggleButton.config(text="Stop Proxy")
                self.toolbar.proxybutton.config(text="Proxy [ON]")
        
    
    
    
    def start_ntlmProxy(self,*args,**kw):
        import utils.ntlmaps
        conf = desktop.Config()
        if self.useproxyvar.get():
            if self.usentlmvar.get() :
                self.thread.proxy = utils.ntlmaps.Proxy(os.path.join(conf['rootdir'],'py','desktop','conf'))
                self.thread.proxy.conf['GENERAL']['PARENT_PROXY'] = self.proxyentryvar.get()
                self.thread.proxy.conf['GENERAL']['PARENT_PROXY_PORT'] = int(self.proxyportvar.get())
                self.thread.proxy.conf['NTLM_AUTH']['NT_DOMAIN'] = self.domainvar.get()
                self.thread.proxy.conf['NTLM_AUTH']['USER'] = self.uservar.get()
                self.thread.proxy.conf['NTLM_AUTH']['PASSWORD'] = self.passwordvar.get()
            
                conf['proxy'] = {'proxy': 'localhost',
                                 'proxy_port':self.thread.proxy.conf['GENERAL']['LISTEN_PORT'],
                                 }
                self.thread.proxy.start()
                print conf
            else:
                conf['proxy'] = {'proxy': self.proxyentryvar.get(),
                                 'proxy_port':self.proxyportvar.get(),
                                 }
        
    def stop_ntlmProxy(self,*args,**kw):
        self.thread.proxy.stop_server()
        conf = desktop.Config()
        conf['proxy'] = False
        
        print conf