# -*- coding: utf-8 -*-

"""
eslib.web
~~~~~~~~~~

Module containing operations against web servers and on web content.
"""


__all__ = ("WebGetter",)


import requests
import eslib, eslib.time
import datetime


class WebGetter(object):
    def __init__(self, max_size=-1, content_types=None):
        self.content_types = content_types or ["text/plain", "text/html", "text/xml", "application/xml"]
        self.max_size = 1024*1024 # 1 MB
        if max_size > 0: self.max_size = max_size

    def get(self, url, index=None, doctype=None, **kwargs):
        # Fetch web page
        try:
            res = requests.get(url, verify=False)
        except:
            msg = "URL failed: %s" % url
            raise IOError(msg)
        if not res.ok:
            msg = "URL not ok, status_code=%s for URL: %s" % (res.status_code, url)
            raise IOError(msg)

        # Verify allowed content type
        content_type = (res.headers.get("content-type") or "").split(";")[0]
        if not content_type in self.content_types:
            msg = "Skipping web page with content type '%s', URL: %s" % (content_type, url)
            raise ValueError(msg)

        # Size check with reported content size
        if self.max_size > 0:
            size = int(res.headers.get("content-length") or -1)
            if size > 0 and size > self.max_size:
                msg = "Skipping too large web page (%s), URL: %s" % (eslib.debug.byteSizeString(size, 2), url)
                raise ValueError(msg)

        # Extract vitals from web result
        id = url # res.url
        encoding = res.encoding
        content = res.text # TODO: Convert to UTF-8 right away if pure text? Or how to tell Elasticsearch about encoding?

        # Repeat size check with actual content size
        if self.max_size > 0:
            size = len(content)
            if size > self.max_size:
                msg = "Skipping too large web page (%s), URL: %s" % (eslib.debug.byteSizeString(size, 2), url)
                raise ValueError(msg)

        # Create ES document from web page
        body = {"content": content, "content_type": content_type, "encoding": encoding}
        webdoc = eslib.createdoc(body, index, doctype, id)

        # Additional fields...
        created_at = datetime.datetime.utcnow()
        if "created_at" in kwargs:
            eslib.putfield(body, "created_at", kwargs["created_at"])
        eslib.putfield(body, "created_at", eslib.time.date2iso(created_at))

        return webdoc