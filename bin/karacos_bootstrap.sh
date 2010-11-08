#!/bin/sh
############################################################################################
#    KaraCos-Desktop - web platform engine client for desktop users - http://karacos.org/
#    Copyright (C) 2009-2010  Nicolas Karageuzian
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################################
DIR=`dirname $0`
cd $DIR/..
KARACOS_HOME=`pwd`
cd $KARACOS_HOME/bin

export PYTHONPATH=$KARACOS_HOME/lib/python:$PYTHONPATH
/usr/bin/python2.6 $KARACOS_HOME/py/karacos_bootstrap.py