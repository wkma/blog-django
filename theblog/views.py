from datetime import date
import logging

from django.core.cache import cache
from django.db.models import Q, F
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404

from comment.forms import CommentForm
from comment.models import Comment
from config.models import SideBar
from .models import Post, Category, Tag

logger = logging.getLogger(__name__)


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)

    def get_navs(self):
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }


class IndexView(CommonViewMixin, ListView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)\
        .select_related('owner')\
        .select_related('category')
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'theblog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """ 重写querset，根据分类过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """ 重写queryset，根据标签过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tags__id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    #queryset = Post.latest_posts
    template_name = 'theblog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form':CommentForm,
            'comment_list':Comment.get_by_target(self.request.path),
        })
        return context
    # from django.http import HttpResponse

    # from django.views.generic import ListView,DetailView
    # from django.shortcuts import get_object_or_404
    #
    #
    # from .models import Post, Tag, Category
    # from config.models import SideBar,Link
    #
    #
    # class CommonViewMixin:
    #     def get_context_data(self,**kwargs):
    #         context = super().get_context_data(**kwargs)
    #         context.update({
    #             'sidebars':SideBar.get_all(),
    #         })
    #         context.update(Category.get_navs())
    #         return context
    #     def get_sidenars(self):
    #         return SideBar.objects.filter(status=SideBar.STATUS_SHOW)
    #
    #
    # class IndexView(CommonViewMixin,ListView):
    #     queryset = Post.latest_posts
    #     paginate_by = 5
    #     context_object_name = "post_list"
    #     template_name = "theblog/list.html"
    #
    #
    # class CategoryView(IndexView):
    #     def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         category_id = self.kwargs.get('category_id')
    #         category = get_object_or_404(Category,pk=category_id)
    #         context.update({
    #             'category':category,
    #         })
    #         return context
    #
    #     def get_queryset(self):
    #         """重写queryset，根据分类过滤"""
    #         queryset = super().get_queryset()
    #         category_id = self.kwargs.get('category_id')
    #         return queryset.filter(category_id=category_id)
    #
    #
    # class TagView(IndexView):
    #     def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         tag_id = self.kwargs.get('tag_id')
    #         tag = get_object_or_404(Tag, pk=tag_id)
    #         context.update({
    #             'tag':tag,
    #         })
    #         return context
    #
    #     def get_queryset(self):
    #         """重写queryset,根据标签过滤"""
    #         queryset = super().get_queryset()
    #         tag_id = self.kwargs.get('tag_id')
    #         return queryset.filter(tag_id=tag_id)
    #
    # class PostDetailView(CommonViewMixin,DetailView):
    #     queryset = Post.latest_posts
    #     #queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    #     template_name = 'theblog/detail.html'
    #     context_object_name = 'post'
    #     pk_url_kwarg = "post_id"
    # def handle_visited(self):
    #     increase_pv = False
    #     increase_uv = False
    #     uid = self.request.uid
    #     pv_key = 'pv:%s:%s' % (uid, self.request.path)
    #     if not cache.get(pv_key):
    #         increase_pv = True
    #         cache.set(pv_key, 1, 1*60)  # 1分钟有效
    #
    #     uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
    #     if not cache.get(uv_key):
    #         increase_uv = True
    #         cache.set(uv_key, 1, 24*60*60)  # 24小时有效
    #
    #     if increase_pv and increase_uv:
    #         Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
    #     elif increase_pv:
    #         Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
    #     elif increase_uv:
    #         Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class Handler404(CommonViewMixin, TemplateView):
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


class Handler50x(CommonViewMixin, TemplateView):
    template_name = '50x.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=500)


# def post_list(request, category_id=None, tag_id=None):  #重构前
#         tag = None
#         category =None
#
#         if tag_id:
#             post_list,tag=Post.get_by_tag(tag_id)
#         elif category_id:
#             post_list,category = Post.get_by_category(category_id)
#         else:
#             post_list = Post.latest_posts
#
#         context = {
#             'category':category,
#             'tag':tag,
#             'post_list':post_list,
#             'sidebars':SideBar.get_all(),
#         }
#
#         context.update(Category.get_navs())
#         return render(request, 'theblog/list.html', context=context)
#
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post':post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'theblog/detail.html', context={'post': post})


# def post_list(request, category_id=1, tags_id=None):
#     content = 'post_list category_id={category_id}, tags_id={tags_id}'.format(
#         category_id=category_id,
#         tags_id=tags_id
#     )
#     return HttpResponse(content)

