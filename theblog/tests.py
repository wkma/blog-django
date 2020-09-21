from django.test import TestCase

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings.develop")# project_name 项目名称
django.setup()
from theblog.models import Post,Category
posts = Post.objects.all().select_related('category')
for post in posts:
    print(post.category)
list=Category.objects.filter(name="宇轩")
print(list)