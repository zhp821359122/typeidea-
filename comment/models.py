from django.db import models
from blog.models import Post

# Create your models here.


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    # target = models.ForeignKey(Post, verbose_name='评论目标')
    # 将评论目标换成CharField 里面存储被评论目标的网址 扩大评论范围
    target = models.CharField(max_length=100, verbose_name='评论目标')
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    website = models.URLField(verbose_name='网站')
    content = models.CharField(max_length=2000, verbose_name='内容')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    @classmethod
    def get_by_target(cls, target):
        '''

        :param target: 根据target来返回该target的所有评论
        :return:
        '''
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)


