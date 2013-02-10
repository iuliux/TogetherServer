"""
    Copyright (C) 2008 Benjamin O'Steen

    This file is part of python-fedoracommons.

    python-fedoracommons is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    python-fedoracommons is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with python-fedoracommons.  If not, see <http://www.gnu.org/licenses/>.
"""

__license__ = 'GPL http://www.gnu.org/licenses/gpl.txt'
__author__ = "Benjamin O'Steen <bosteen@gmail.com>"
__version__ = '0.1'

import httplib2
import urlparse
import urllib


class ConnectionError(Exception):
    def __str__(self):
        return "Connection failed"


class Connection:
    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url
        self.username = username

        self.url = urlparse.urlparse(base_url)

        (scheme, netloc, path, query, fragment) = urlparse.urlsplit(base_url)

        self.scheme = scheme
        self.host = netloc
        self.path = path

        # Create Http class with support for Digest HTTP Authentication, if necessary
        self.h = httplib2.Http(".cache")
        self.h.follow_all_redirects = True
        if username and password:
            self.h.add_credentials(username, password)

    def request_get(self, resource, args=None, headers={}):
        return self.request(resource, "get", args, headers=headers)

    def request_delete(self, resource, args=None, headers={}):
        return self.request(resource, "delete", args, headers=headers)

    def request_head(self, resource, args=None, headers={}):
        return self.request(resource, "head", args, headers=headers)

    def request_post(self, resource, args=None, body=None, headers={}):
        return self.request(resource, "post", args, body=body, headers=headers)

    def request_put(self, resource, args=None, body=None, headers={}):
        return self.request(resource, "put", args, body=body, headers=headers)

    def request(self, resource, method="get", args=None, body=None, headers={}):
        path = resource
        headers['User-Agent'] = 'Basic Agent'

        if body:
            if not headers.get('Content-Type', None):
                headers['Content-Type'] = 'text/xml'
            headers['Content-Length'] = str(len(body))
        else:
            if 'Content-Length' in headers:
                del headers['Content-Length']

            headers['Content-Type'] = 'text/plain'

            if args:
                if method == "get":
                    path += u"?" + urllib.urlencode(args)
                elif method == "put" or method == "post":
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'
                    body = urllib.urlencode(args)

        request_path = []
        # Normalise the / in the url path
        if self.path != "/":
            if self.path.endswith('/'):
                request_path.append(self.path[:-1])
            else:
                request_path.append(self.path)
            if path.startswith('/'):
                request_path.append(path[1:])
            else:
                request_path.append(path)

        resp, content = self.h.request(u"%s://%s%s" % (self.scheme, self.host, u'/'.join(request_path)), method.upper(), body=body, headers=headers)
        # TODO trust the return encoding type in the decode?
        return {u'headers': resp, u'body': content.decode('UTF-8')}
