＃博客-基于django
环境python3.7.7，django3.0.7，mysql。

使用django+mysql+bootstrap等技术创建的博客，目前可以登录后台写博客，普通前端可以看到。还有未完善的功能和未优化的地方。

使用说明：pip install -r requirements.txt安装依赖环境。可以连接自己的数据库迁移数据库后，使用python manage.py makemigrations
生成迁移文件，再使用python manage.py migrate将数据表迁移完成。
然后使用python manage.py creatsuperuser创建超级管理员登录后台，可以简单使用。
许多功能待完善

