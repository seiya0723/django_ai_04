# Generated by Django 3.1.2 on 2021-05-15 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('illust', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='mime',
            field=models.TextField(default='', verbose_name='MIMEタイプ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='design',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='file/thumbnail/', verbose_name='サムネイル'),
        ),
    ]
