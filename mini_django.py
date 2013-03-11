"""
Django in single file with model and admin. Based on:-

http://fahhem.com/blog/2011/10/django-models-without-apps-or-everything-django-truly-in-a-single-file/

I found it here : https://gist.github.com/k4ml/2221909
"""
import sys
from os import path as osp

def rel_path(*p): return osp.normpath(osp.join(rel_path.path, *p))
rel_path.path = osp.abspath(osp.dirname(__file__))
this = osp.splitext(osp.basename(__file__))[0]
this_module = lambda thisfile: osp.splitext(osp.basename(thisfile))[0]

def configure(**new_settings):
    from django.conf import settings
    SETTINGS = dict(
        SITE_ID=1,
        DATABASES = {},
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        ROOT_URLCONF = this
    )
    SETTINGS['TEMPLATE_DIRS'] = (rel_path()+'/templates'),
    SETTINGS['DATABASES']={
        'default':{
            'ENGINE':'django.db.backends.sqlite3',
            'NAME':rel_path('db')
        }
    }

    SETTINGS['INSTALLED_APPS'] = (
        'django.contrib.contenttypes',
    )

    SETTINGS.update(**new_settings)

    if not settings.configured:
        settings.configure(**SETTINGS)


from django.conf.urls.defaults import patterns, url, include

urlpatterns = None
def run(urls, this_file, module_name, settings=None):
    from django.db import models
    global urlpatterns
    urlpatterns = patterns('', *urls)
    this = this_module(this_file)

    # override get_app to work with us
    get_app_orig = models.get_app
    def get_app(app_label,*a, **kw):
        if app_label == this_module(this_file):
            return sys.modules[module_name]
        return get_app_orig(app_label, *a, **kw)
    models.get_app = get_app

    models.loading.cache.app_store[type(this+'.models',(),{'__file__': this_file})] = this

    from django.core import management
    management.execute_from_command_line()
