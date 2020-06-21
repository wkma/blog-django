from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time')
    fields = ('name', 'status', 'is_nav')

    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(CategoryAdmin,self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'creat_time', 'operator', 'post_count'
    ]
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    action_on_top = True
    action_on_bottom = True

    #编辑页面
    save_on_top = True

    fields = (
        ('category', 'title'),
        'description',
        'status',
        'content',
        'tags',
    )

    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:theblog_post_change', args=(obj.id,))
        )
    operator.short_description = "操作"

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def __str__(self):
        return self.name

