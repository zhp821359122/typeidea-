# from django.contrib.syndication.views import Feed
# from django.urls import reverse
# from django.utils.feedgenerator import Rss201rev2Feed
# from .models import Post
#
# class LatestPostFeed(Feed):
#     feed_type = Rss201rev2Feed
#     title = 'Typeidea Blog System'
#     link = '/rss'
#     description = 'typeidea is a blog system power by django'
#
#     def items(self):
#         return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]
#     def item_title(self, item):
#         return item.title
#     def item_description(self, item):
