from django.shortcuts import render, HttpResponse
from blog.views import CommonViewMixin
from django.views.generic import ListView
from .models import Link
# Create your views here.

# 这个类是处理友链的


class LinkListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'


def links(request):
    return HttpResponse('links')