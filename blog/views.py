from django.shortcuts import render
from blog.models import Category,Post
from config.models import SideBar
from django.views.generic import ListView
from django.db.models import Q,F

from datetime import date
from django.core.cache import cache
# Create your views here.


# 这个类是用来搞友链的 看看到底是个啥
class CommonViewMixin:
    def get_content_data(self, **kwargs):
        context = super(CommonViewMixin, self).get_content_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class PostListView(ListView):
    queryset = []
    paginate_by = 4
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

    def __init__(self):
        super(PostListView, self).__init__()
        self.tag = None
        self.category = None
        self.owner = None

    def get(self, request, category_id=None, tag_id=None, owner_id=None, *args, **kwargs):
        if tag_id:
            self.queryset, self.tag = Post.get_by_tag(tag_id)
        else:
            if category_id:
                self.queryset, self.category = Post.get_by_category(category_id)
            elif owner_id:
                self.queryset, self.owner = Post.get_by_owner(owner_id)
            else:
                self.queryset = Post.latest_posts()
        return super(PostListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(PostListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return qs.filter(Q(title__icontains=search) | Q(category__name__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'category': self.category,
            'tag': self.tag,
            'owner': self.owner,
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        if self.request.GET.get('search'):
            context.update({
                'keyword': self.request.GET.get('search'),
            })
        return context


# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     else:
#         if category_id:
#             post_list, category = Post.get_by_category(category_id)
#         else:
#             post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    handle_visited(request, post_id)
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


def handle_visited(request, post_id):
    increase_pv = False
    increase_uv = False
    uid = request.uid
    pv_key = 'pv:%s:%s' % (uid, request.path)
    uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), request.path)
    if not cache.get(pv_key):
        increase_pv = True
        cache.set(pv_key, 1, 1*60)
    if not cache.get(uv_key):
        increase_uv = True
        cache.set(uv_key, 1, 24*60*60)
    if increase_uv and increase_pv:
        Post.objects.filter(pk=post_id).update(pv=F('pv') + 1, uv=F('uv') + 1)
    elif increase_pv:
        Post.objects.filter(pk=post_id).update(pv=F('pv') + 1)
    elif increase_uv:
        Post.objects.filter(pk=post_id).update(uv=F('uv') + 1)
