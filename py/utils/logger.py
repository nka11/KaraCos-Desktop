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

__license__ = 'GPL'
import logging.config , traceback

import sys, os
import new
import desktop
logconfigfile = os.path.join(desktop.Config()['rootdir'],"py","desktop","conf","logging.conf")

logging.config.fileConfig(logconfigfile)


LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

def get_level(level_def):
    try:
        level_name = level_def
        level = LEVELS.get(level_name, logging.NOTSET)
        return level
        #logging.basicConfig(level=level)
    except:
        logging.critical(sys.exc_info())



def get_logger(logger,conf=None):
    """
    initialize KaraCos Logger
    """
    _logger = logging.getLogger(logger)
    if "log_exc" not in _logger.__dict__:
        def log_exc(self,exc_info,level='info'):
            #print 'Level %s: %s' % (level, get_level(level))
            exceptionType, exceptionValue,exceptionTraceback = exc_info
            msg = 'raised %s : %s \n %s' % (exceptionType, exceptionValue,traceback.format_tb(exceptionTraceback))
            _logger.log(get_level(level),msg)
        _logger.log_exc = new.instancemethod(log_exc, logger.__class__)
        _logger.debug("Logger Initialization successful")
    return _logger