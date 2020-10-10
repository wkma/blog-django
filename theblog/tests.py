from django.test import TestCase

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings.develop")# project_name 项目名称
django.setup()
from theblog.models import Post,Category
posts = Post.objects.filter()
for post in posts:
    print(post.title)
# list=Category.objects.filter(name="博文")
# print(list)