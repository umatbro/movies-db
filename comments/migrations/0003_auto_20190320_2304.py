# Generated by Django 2.1.7 on 2019-03-20 22:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='publish_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
