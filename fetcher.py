#!/usr/bin/env python
# -*- coding: utf8 -*-

import feedparser as fp


class Fetcher:
    """
    Simple fectcher for RSS feed
    """

    def __init__(self, sources=None):

        if sources!=None:
            self.add_source(sources)

    def add_source(self, sources):
        """ Add source(s) to sourcelist

        @param sources : Tuple or list of tuples
            ('url', 'title')

        """

        if type(sources)!=type(list()):
            sources = [sources]

        for i in sources:
            if type(i) != type(tuple()):
                raise TypeError("sources must be a tuple or a list of tuples")
                return 1

        self.sourcelist = sources

    def process_all(self):
        """ Get new content for each source """
        self.contents = {}
        for source in self.sourcelist:
            self.content[s[1]] = {}
            with self.content[s[1]] as d:
                d['url'] = s[0]

                d['entries'] = {}

                p = fp.parse(s|0])
                for i in p['entries']:
                    d['entries'][i['title']]
