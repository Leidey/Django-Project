from django.conf.urls import url
from django.contrib import admin


#from . import views
from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    post_about,
    post_contact,
    #home,
    #login,
    #logout,
    #registration,
    #logout_page,
    success,
    archive,
    )


urlpatterns = [
    url(r'^$',post_list, name='list'),
    #url(r'^home/$',home, name='home'),
    url(r'^archive/$',archive, name='archive'),
    #url(r'^login/$',login, name='login'),
    #url(r'^logout/$',logout, name='logout'),
    #url(r'^logout_page/$',logout_page, name='logout_page'),
    #url(r'^registration/$',registration, name='registration'),
    url(r'^success/$',success, name='success'),
    url(r'^create/$',post_create, name='create'),
    url(r'^about/$',post_about, name='about'),
    url(r'^contact/$',post_contact, name='contact'),
    url(r'^(?P<slug>[\w-]+)/$',post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$',post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$',post_delete, name='delete'),
   
]
