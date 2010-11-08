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

class SshUi(Tkinter.Frame):
    
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
        
        sshhost = Tkinter.Label(self,text="Host",anchor="w")
        sshhost.grid(column=0,row=rowid,sticky='EW')
        self.sshhostvar = Tkinter.StringVar()
        self.hostentry = Tkinter.Entry(self,textvariable=self.sshhostvar)
        self.hostentry.grid(column=1,row=rowid,sticky='EW')
        self.hostentry.bind("<Return>", self.OnPressEnter)
        
        rowid += 1
        sshportlabel = Tkinter.Label(self,text="Port",anchor="w")
        sshportlabel.grid(column=0,row=rowid,sticky='EW')
        self.sshportvar = Tkinter.StringVar()
        self.sshportentry = Tkinter.Entry(self,textvariable=self.sshportvar)
        self.sshportentry.grid(column=1,row=rowid,sticky='EW')
        self.sshportentry.bind("<Return>", self.OnPressEnter)
        
        rowid += 1
        sshuserlabel = Tkinter.Label(self,text="Username",anchor="w")
        sshuserlabel.grid(column=0,row=rowid,sticky='EW')
        self.sshuservar = Tkinter.StringVar()
        self.sshuserentry = Tkinter.Entry(self,textvariable=self.sshuservar)
        self.sshuserentry.grid(column=1,row=rowid,sticky='EW')
        self.sshuserentry.bind("<Return>", self.OnPressEnter)
        rowid += 1
        sshpasslabel = Tkinter.Label(self,text="Port",anchor="w")
        sshpasslabel.grid(column=0,row=rowid,sticky='EW')
        self.sshpassvar = Tkinter.StringVar()
        self.sshpassentry = Tkinter.Entry(self,show="*",textvariable=self.sshpassvar)
        self.sshpassentry.grid(column=1,row=rowid,sticky='EW')
        self.sshpassentry.bind("<Return>", self.OnPressEnter)
        rowid += 1
        
        self.runbtn = Tkinter.Button(self, text="run ssh", width=10, command=self.OnPressRun)
        self.runbtn.grid(column=0,row=rowid)
        
        
   
    def OnPressEnter(self,*args,**kw):
        """
        """
    def OnPressRun(self,*args,**kw):
        """
        """
        host = self.sshhostvar.get()
        port = int(self.sshportvar.get())
        user = self.sshuservar.get()
        password = self.sshpassvar.get()
        from utils.client.ssh import SSHClient
        client = SSHClient()
        import paramiko
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, user, password)
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command("netstat -rn")
        while (1):
            out = ssh_stdout.read()
            if out != None:
                for line in out.splitlines():
                    print line


                  
