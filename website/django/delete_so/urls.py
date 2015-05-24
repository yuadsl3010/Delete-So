"""delete_so URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from View.index import *
from View.json import *
from View.secret import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', init_delete_so),
    url(r'^search.html$', do_search),
    url(r'^json/refresh_ds_comments/$', refresh_ds_comments),
    url(r'^json/refresh_main_page_view/$', refresh_main_page_view),
    url(r'^json/get_search_results/$', get_search_results),
    url(r'^json/get_spider_speed/$', get_spider_speed),
    url(r'^secret/add_black/$', add_black),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

