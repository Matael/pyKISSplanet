"""
This use mini_django.py, sort of micro framework based on django.
"""

import mini_django
mini_django.configure()

from django.db import models
from django.shortcuts import render_to_response, redirect
import feedparser as fp
from md5 import md5

# -- Models --

class Link(models.Model):
    """
    Link Class : handle new links in/out the db

    title : article title
    url : article url
    source : source url
    checksum : md5(title+source)
    """

    title = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    source = models.CharField(max_length=300)
    checksum = models.CharField(max_length=300)

    def __unicode__(self):
        return self.title+' @ '+self.source

    class Meta:
        app_label = mini_django.this_module(__file__)
    __module__ = mini_django.this_module(__file__)


# -- Views --

class Fetcher:
    """
    Simple fectcher for RSS feed
    """

    def __init__(self, sources=None):
        """ init """

        # add sources if specified
        if sources!=None:
            self.add_source(sources)


    def add_source(self, sources):
        """ Add source(s) to sourcelist """

        if type(sources)!=type(list()):
            sources = [sources]

        for i in sources:
            if type(i) != str:
                raise TypeError("sources must be strings")
                return 1

        self.sourcelist = sources

    def process_all(self):
        """ Get new content for each source """

        for source_url in self.sourcelist:

            feed = fp.parse(source_url)
            feed = feed['entries']

            for article in feed:
                checksum = md5(article['title'].encode('utf8')+source_url).hexdigest()

                if not Link.objects.filter(checksum=checksum):

                    l  = Link(
                        source=source_url,
                        title=article['title'].encode('utf8'),
                        url=article['link'].encode('utf8'),
                        checksum=checksum
                    )
                    l.save()

                else:
                    print("Link already present, skipping.")

            # except:
            #     print("Problem occured, skipping source : "+source_url)


def index(request):
    """ main page """

    links = Link.objects.all()

    return render_to_response("index.html", {'links': links})


def refresh(request, slist=None):
    """ refresh page, not template : just code :) """
    if not slist:
        slist = _get_list()

    f = Fetcher(sources=slist)
    f.process_all()
    return redirect('index')


def _get_list(filename='sourcelist'):
    """ helper to get sourcelist """

    with open(filename, 'r') as sourcelist:
        return sourcelist.readlines()

# -- URLs --


urls = (
    (r'^$', index),
    (r'^refresh/?$', refresh),
)

# -- run --

if __name__ == '__main__':
    mini_django.run(urls, __file__, __name__)
