# Generated by Django 3.0.6 on 2020-09-11 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0002_auto_20200723_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_html',
            field=models.TextField(blank=True, editable=False, verbose_name='正文html代码'),
        ),
    ]