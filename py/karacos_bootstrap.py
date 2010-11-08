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

import os, sys
import desktop

KcRoot = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
print os.path.split(os.path.abspath(__file__))
print "KaraCos Desktop is starting on %s" % os.name
print "KaraCosRoot = %s" % KcRoot
sys.path.append(os.path.join(KcRoot,'py'))
sys.path.append(os.path.join(KcRoot,'lib','python'))
os.environ['KaraCosRoot'] = KcRoot

if __name__ == '__main__':
    import setup
    thread = desktop.DesktopThread(KcRoot)
    thread.start()
    
    