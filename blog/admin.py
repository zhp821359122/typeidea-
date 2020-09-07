from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from blog.adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from blog.models import Tag,Post,Category
# Register your models here.
class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        # print(Category.objects.filter(owner=request.user).values('id', 'name'))
        # print(Category.objects.filter(owner=request.user).values_list('id', 'name'))
        # print(Category.objects.filter(owner=request.user).values_list('name'))
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status','owner',
        'created_time','operator',
    ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    # list_filter = ['category']
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        })
    )
    # filter_horizontal = ('tag',)
    # filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}"> 编辑 </a>',
            reverse('cus_admin:blog_post_change', args = (obj.id,))
        )
    operator.short_description = '操作'


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time','post_count')
    fields = ('name', 'status', 'is_nav',)
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'



@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')