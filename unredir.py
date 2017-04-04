# -*- coding:utf-8 -*-
import urllib2
class UnFollowRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_301 = http_error_303 = http_error_307 = http_error_302
