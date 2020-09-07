"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from typeidea.custom_site import custom_site

from blog.views import post_detail, PostListView
from config.views import LinkListView
from comment.views import CommentView

urlpatterns = [
    # 处理添加评论
    url(r'^comment/$', CommentView.as_view(), name='add_comment'),
    # 友链
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^$', PostListView.as_view(), name='index'),
    url(r'^owner/(?P<owner_id>\d+)/$', PostListView.as_view(), name='owner_list'),
    url(r'^category/(?P<category_id>\d+)/$', PostListView.as_view(), name='category_list'),
    url(r'^tag/(?P<tag_id>\d+)/$', PostListView.as_view(), name='tag_list'),

    url(r'^post/(?P<post_id>\d+).html$', post_detail, name='post_detail'),


    url(r'^super_admin/', admin.site.urls, name='super_admin'),

    url(r'^admin/', custom_site.urls, name='admin'),
]
