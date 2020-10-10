"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.contrib import admin

from theblog.views import(
IndexView,CategoryView,TagView,
PostDetailView,SearchView,AuthorView
)
#from theblog.views import post_list, post_detail
from config.views import LinkListView
from config import views
from comment.views import CommentView
#from blog.custom_site import custom_site


urlpatterns = [
    path('1', views.inde),
    path('',IndexView.as_view(),name='index'),
    #path('', post_list,name="index"),
    path('category/<int:category_id>/', CategoryView.as_view(),name="category-list"),
    path('tags/<int:tag_id>/', TagView.as_view(),name='tag-list'),
    path('post/<int:post_id>.html', PostDetailView.as_view(),name='post-detail'),
    path('links/', LinkListView.as_view(),name='links'),
    path('search/',SearchView.as_view(),name='search'),
    path('author/<int:owner_id>/',AuthorView.as_view(),name="author"),
    path('comment/',CommentView.as_view(),name='comment'),
    #url(r'^comment/$',CommentView.as_view(),name='comment'),
    # path('category/<int:category_id>/', post_list,name="category-list"),
    # path('tags/<int:tag_id>/', post_list,name='tag-list'),
    # path('post/<int:post_id>.html', post_detail,name='post-detail'),
    # path('links/', links,name='links'),
    #path('super_admin/', custom_site.urls,name="super-admin"),
    path('admin/', admin.site.urls),

    #url(r'li/^$', views.inde),
    #
    # url(r'admin/', admin.site.urls),
]
