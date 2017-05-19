from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    post_about,
    post_contact,
    success,
    archive,
    )

urlpatterns = [
    url(r'^$',post_list, name='list'),
    url(r'^archive/$',archive, name='archive'),
    url(r'^success/$',success, name='success'),
    url(r'^create/$',post_create, name='create'),
    url(r'^about/$',post_about, name='about'),
    url(r'^contact/$',post_contact, name='contact'),
    url(r'^(?P<slug>[\w-]+)/$',post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$',post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$',post_delete, name='delete'),

]
