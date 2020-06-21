from .base import *  #NOQA

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#配置使用mysql
    'default':{
        'ENGINE': 'django.db.backends.mysql',  #数据库产品
        'NAME': "dj_blog",  #数据库名
        'HOST': "127.0.0.1",  #主机地址，本地使用localhost，生产环境为实际主机IP
        "PORT": "3306",  #端口
        "USER": "wang",  #用户名
        "PASSWORD": "123",  #密码
    }
}