"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from django.contrib.auth import views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

import myapp.forms
from myapp.forms import LoginForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^myapp/', include("myapp.urls", namespace='myapp')),
    # url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm},name='login'),
    # url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': LoginForm},name='login'),
    url(r'^logout/$', logout, {'next_page': '/login'}, name='logout'),

    # url(r'^login/$', 'myapp.views.login'),
    # url(r'^logout/$', 'myapp.views.logout'),
    # url(r'^auth/$', 'myapp.views.auth_view'),
    # url(r'^loggedin/$', 'myapp.views.loggedin'),
    # url(r'^invalid/$', 'myapp.views.invalid_login'),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)