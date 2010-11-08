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
"""
from threading import Thread
import DesktopUI
import os
DesktopUI = DesktopUI.DesktopUI



class Config(object):
    class __Config(dict):
        def __init__(self):
            dict.__init__(self)
    instance = None
    def __new__(cls):
        print "new"
        if not cls.instance:
            cls.instance = Config.__Config()
            cls.instance['proxy'] = None
        return cls.instance
        
    def __getitem__(self, attr):
        return Config.instance[attr]

    def __setitem__(self, attr, val):
        Config.instance[attr] = val

try:
    import utils.client.ssh
    ssh = utils.client.ssh
except:
    print "ssh lib dependency is missing"

class DesktopThread(Thread):
    def __init__ (self,rootdir):
        Thread.__init__(self)
        Config()['rootdir'] = rootdir
        import utils.logger
        self.log = utils.logger.get_logger(self.__class__.__name__)
        Config()['tmpdir'] = os.path.join(rootdir,'temp')
        if not os.path.exists(Config()['tmpdir']):
            os.makedirs(Config()['tmpdir'])
    def run(self):
        app = DesktopUI(None,self)
        app.title('KaraCos Desktop')
        app.mainloop()
