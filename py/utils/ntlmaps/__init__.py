import sys
from threading import Thread
import server, config, config_affairs
#--------------------------------------------------------------
# config affairs
# look for default config name in lib/config.py
class Proxy(Thread):
    def __init__ (self,confdir):
        Thread.__init__(self)
        self.confdir = confdir
        self.conf = config.read_config(config.findConfigFileNameInArgv(sys.argv,self.confdir))
    
        self.conf['GENERAL']['VERSION'] = '0.9.9.0.1'
        
        #--------------------------------------------------------------
        print 'NTLM authorization Proxy Server v%s' % self.conf['GENERAL']['VERSION']
        print 'Copyright (C) 2001-2004 by Dmitry Rozmanov and others.'
        
        
        #print self.config
    def run(self):

        self.config = config_affairs.arrange(self.conf)
        print "PARENT_PROXY : %s : %s \n" % (self.config['GENERAL']['PARENT_PROXY'],self.config['GENERAL']['PARENT_PROXY_PORT'])
        
        self.serv = server.AuthProxyServer(self.config)
        self.serv.run()

    def stop_server(self):
        self.serv.stop_proxy()