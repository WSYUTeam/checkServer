#!/usr/bin/python
#-*-coding:utf-8 -*-

import sys
import urllib
import re
from spyne import Application, rpc, ServiceBase
from spyne import Integer, Unicode, Array, ComplexModel  
from spyne.protocol.soap import Soap11  
from spyne.server.wsgi import WsgiApplication  
from wsgiref.simple_server import make_server



URL_REG = re.compile(r'(http://[^/\\]+)', re.I)
IMG_REG = re.compile(r'<img[^>]*?src=([\'"])([^\1]*?)\1', re.I)


class SomeSampleServices(ServiceBase):

    @rpc(Unicode, _returns=Unicode)
    def make_project(self, name):
        url = 'http://oa.wsyu.edu.cn:8080/edoas2/tip_api.jsp?name=%s' % name
        global URL_REG, IMG_REG
        m = URL_REG.match(url)
        if not m:
            print '[Error]Invalid URL: ', url
            return
        return urllib.urlopen(url).read()


    
if __name__ == "__main__":
    soap_app = Application([SomeSampleServices],  
                           'OAUnreadServices',
                           in_protocol=Soap11(validator="lxml"),  
                           out_protocol=Soap11())  
    wsgi_app = WsgiApplication(soap_app)  
    server = make_server('0.0.0.0', 5001, wsgi_app)
  
    sys.exit(server.serve_forever())
