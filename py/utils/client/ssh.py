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
import paramiko
import socket
from paramiko.ssh_exception import SSHException, BadHostKeyException
from paramiko.transport import Transport
from paramiko.resource import ResourceManager
import getpass
from utils.client.http import Connection,HttpProxyConnection
from utils import tunnel
import ssl
SSH_PORT = 22
import desktop


class SSHClient(paramiko.SSHClient):
    """
    Subclassing paramiko sshclient to add proxy via feature
    """
    def connect(self, hostname, port=SSH_PORT, username=None, password=None, pkey=None,
                key_filename=None, timeout=None, allow_agent=True, look_for_keys=True):
        """
        
        """
        sock = None
        if not desktop.Config()['proxy']:
            for (family, socktype, proto, canonname, sockaddr) in socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                if socktype == socket.SOCK_STREAM:
                    af = family
                    addr = sockaddr
                    break
            else:
                raise SSHException('No suitable address family for %s' % hostname)
            sock = socket.socket(af, socket.SOCK_STREAM)
            if timeout is not None:
                try:
                    sock.settimeout(timeout)
                except:
                    pass
            sock.connect(addr)
        else:
            proxy_connexion = HttpProxyConnection((hostname,port),[desktop.Config()['proxy']['proxy'], desktop.Config()['proxy']['proxy_port']])
            
            #conn = HttpProxyConnection((hostname,port),(desktop.Config()['proxy']['proxy'], desktop.Config()['proxy']['proxy_port']))
            proxy_connexion.establish()
            sock = proxy_connexion.socket
            if sock == None:
                raise Exception("Erreur RESEAU")
            #self.sock = ssl.wrap_socket(sock)
            #sock = ssl.wrap_socket(proxy_connexion.socket,do_handshake_on_connect=False)
            #sock = proxy_connexion.socket
            #sock.connect((hostname,port))
            
        t = self._transport = Transport(sock)
        t.banner_timeout = 180
        if self._log_channel is not None:
            t.set_log_channel(self._log_channel)
        t.start_client()
        ResourceManager.register(self, t)

        server_key = t.get_remote_server_key()
        keytype = server_key.get_name()

        if port == SSH_PORT:
            server_hostkey_name = hostname
        else:
            server_hostkey_name = "[%s]:%d" % (hostname, port)
        our_server_key = self._system_host_keys.get(server_hostkey_name, {}).get(keytype, None)
        if our_server_key is None:
            our_server_key = self._host_keys.get(server_hostkey_name, {}).get(keytype, None)
        if our_server_key is None:
            # will raise exception if the key is rejected; let that fall out
            self._policy.missing_host_key(self, server_hostkey_name, server_key)
            # if the callback returns, assume the key is ok
            our_server_key = server_key

        if server_key != our_server_key:
            raise BadHostKeyException(hostname, server_key, our_server_key)

        if username is None:
            username = getpass.getuser()

        if key_filename is None:
            key_filenames = []
        elif isinstance(key_filename, (str, unicode)):
            key_filenames = [ key_filename ]
        else:
            key_filenames = key_filename
        self._auth(username, password, pkey, key_filenames, allow_agent, look_for_keys)