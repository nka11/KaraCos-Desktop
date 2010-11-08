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
import os
import ConfigParser
from utils.client.http import UrlHandler
import desktop
import utils
import tarfile,shutil
import zipfile

class DepsManager():
    """
    Dependencies downloader and installer
    """
    def __init__(self, conf_filename):
        self.log = utils.logger.get_logger(self.__class__.__name__)
        self.config = ConfigParser.RawConfigParser()
        self.config.read(conf_filename)
        self.urlhandler = UrlHandler()
    
    def check_dependency(self,dependency):
        """
        """
    
    def install_dependency(self,dependency):
        """
        """
        self.get_dependency(dependency)
        if self.config.get(dependency, 'archive_type')  == 'python-noarch':
            self.install_python(dependency)
        elif self.config.get(dependency, 'archive_type')  == 'python-arch':
            ""#if
            if os.name in ['nt']:
                self.install_arch_win32(dependency)
                  
    def get_dependency(self,dependency):
        url = None
        if self.config.get(dependency, 'archive_type')  == 'python-noarch':
            url = self.config.get(dependency, 'archive_url') 
        elif self.config.get(dependency, 'archive_type')  == 'python-arch':
            if os.name in ['nt']:
                url = self.config.get(dependency, 'archive_url_win32')
        
        self.log.info("Getting %s at %s" % (dependency,url))
        response = self.urlhandler.processRequest("GET", url)
        self.log.debug(response.getheaders())
        filename = os.path.join(desktop.Config()['tmpdir'],dependency)
        file = open(filename, 'wb')
        file.write(response.read())
        file.flush() 
        file.close()
        
    def install_python(self,dependency):
        filename = os.path.join(desktop.Config()['tmpdir'],dependency)
        if tarfile.is_tarfile(filename):
            self.log.debug("%s is a tarfile" % filename)
            ardir = self.config.get(dependency, 'archive_dir')
            pylibdir = self.config.get(dependency, 'archive_pylib')
            deptar = tarfile.open(filename)
            deptar.extractall(path=desktop.Config()['tmpdir'])
            srcdir = os.path.join(desktop.Config()['tmpdir'],ardir,pylibdir)
            destdir = os.path.join(desktop.Config()['rootdir'],'lib','python',self.config.get(dependency, 'py_dest'))
            shutil.copytree(srcdir, destdir)
    
    def install_arch_win32(self,dependency):
        ""
        filename = os.path.join(desktop.Config()['tmpdir'],dependency)
        if zipfile.is_zipfile(filename):
            ""
            filezip = zipfile.ZipFile(filename)
            filezip.extractall(desktop.Config()['tmpdir'])
            if self.config.has_option(dependency, 'installer_win32'):
                execdir = os.path.join(desktop.Config()['tmpdir'],self.config.get(dependency, 'installer_win32'))
                os.system(execdir)
            
        
            