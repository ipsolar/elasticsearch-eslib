# -*- coding: utf-8 -*-

import unittest
from eslib.procs import HtmlRemover

class TestHtmlRemover(unittest.TestCase):

    def test_str(self):
        dirty = '<a href="http://blabla.com/bla">Lady &amp; Landstrykeren</a>'

        p = HtmlRemover()
        cleaned = p._clean(dirty)
        print "D=", dirty
        print "C=", cleaned

        self.assertTrue(cleaned == "Lady & Landstrykeren")

    def test_unicode(self):
        dirty = u'<a href="http://blabla.com/bla">Lady &amp; Landstrykeren</a>'

        p = HtmlRemover()
        cleaned = p._clean(dirty)
        print "D=", dirty
        print "C=", cleaned

        self.assertTrue(cleaned == u"Lady & Landstrykeren")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
