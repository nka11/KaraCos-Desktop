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
import socket
import ssl
import httplib
import urllib
import desktop
from string import split

class Connection:  # generic tcp connection wrapper
    def __init__(self, server):
        self.socket = None
        self.server = server
        import utils.logger
        self.log = utils.logger.get_logger(self.__class__.__name__)

    def establish(self):
        if self.socket == None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(None)
            server = (self.server[0], int(self.server[1]))
            s.connect(server)
            self.socket = s
        return self.socket

    def send_data(self, buf):
        return self.socket.send(buf)

    def receive_data(self, bufsize):
        return self.socket.recv(bufsize)

    def send_data_all(self, buf):
        total = len(buf)
        sent = 0
        while sent < total:
            sent = sent + self.send_data(buf[sent:])
        return sent

    def send_data_line(self, line):
        ###print "C:" + line #XXX
        return self.send_data_all(line) + self.send_data_all('\r\n')

    def receive_data_line(self):
        cnt = 0
        buf = ''
        while 1:
            in_byte = self.receive_data(1)
            if in_byte == '':
                return None
            if in_byte == '\r':
                cnt = 1
            elif in_byte == '\n' and cnt == 1:
                cnt = 2
            else:
                cnt = 0
            buf = buf + in_byte
            if cnt == 2:
                #self.log.info("B:%s" % buf) #XXX
                return buf

    def break_(self):
        self.socket.shutdown(2)
        self.socket.close()
        self.socket = None

class HttpProxyConnection(Connection):  # http tunnelling
    def __init__(self, server, proxy):
        Connection.__init__(self, server)
        self.proxy = proxy
        

    def establish(self):
        tmp = self.server
        self.server = self.proxy
        try:
            Connection.establish(self)
        finally:
            self.server = tmp

        connect_str = 'CONNECT ' + self.server[0] \
            + ':' + str(self.server[1]) \
            + ' HTTP/1.0\r\n'
        self.log.info("S:%s" % connect_str)
        self.send_data_all(connect_str)
        self.send_data_all('User-Agent: KaraCos\r\n')
        self.send_data_all('Host: ' + self.server[0] + '\r\n')
        self.send_data_all('\r\n')

        status = -1
        while 1:
            buf = self.receive_data_line()
            self.log.info("ESTABLISH: %s" % buf)
            if status == -1:
                resp = split(buf, ' ', 2)
                if len(resp) > 1:
                    status = int(resp[1])
                else:
                    status = 0
            if buf == '\r\n':
                break

        if status != 200:
            self.socket = None
        return self.socket
HTTPConnection = httplib.HTTPConnection

class HTTPSConnection(httplib.HTTPSConnection):
    # httplib.HTTPSConnection with proxy support
    def __init__(self, host, port = None, key_file = None, cert_file = None,
                 strict = None, http_proxy = None):
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file,
                                         strict)
        self.http_proxy = http_proxy

    def connect(self):
        if self.http_proxy:
            conn = HttpProxyConnection((self.host, self.port), self.http_proxy)
            conn.establish()
            sock = conn.socket
            #self.sock = httplib.FakeSocket(sock, ssl)
            #ssl = socket.ssl(sock, self.key_file, self.cert_file)
            self.sock = ssl.wrap_socket(sock)
            
        else:
            httplib.HTTPSConnection.connect(self)

class UrlHandler():
    http_timeout = 15
    proxy_host = None
    proxy_port = None
    
    def __init__(self,http_timeout=None,proxy_host=None,proxy_port=None):
        try:
            self.http_timeout = float(http_timeout)
        except:
            pass
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        
    
    def processRequest(self,method=None,url=None,data="",headers={}):
        conf = desktop.Config()
        if not conf['proxy']:
            self.proxy_host = None
            self.proxy_port = None
        else:
            self.proxy_host = conf['proxy']['proxy']
            self.proxy_port = conf['proxy']['proxy_port']
        socket.setdefaulttimeout(self.http_timeout)
        (protocol,resource) = urllib.splittype(url)
        (hostport,path) = urllib.splithost(resource)
        connexion = None
        if protocol.lower() == "http":
            (host,port) = urllib.splitnport(hostport, 80)
            import httplib
            if self.proxy_host != None and self.proxy_port != None :
                connexion = HTTPConnection(self.proxy_host, self.proxy_port, timeout=self.http_timeout)
                path = url
            else:
                connexion = HTTPConnection(host, port, timeout=self.http_timeout)
        elif protocol.lower() == "https" :
            (host,port) = urllib.splitnport(hostport, 443)
            connexion = HTTPSConnection(host, port)
            if self.proxy_host != None and self.proxy_port != None :
                connexion.http_proxy = [self.proxy_host,
                                        self.proxy_port]
        else:
            assert False, "Unhandled Protocol, please use HTTP or HTTPS"
        
            
        connexion.connect()
        connexion.request(method, path, body=data, headers=headers)
        response = connexion.getresponse()
        
        return response