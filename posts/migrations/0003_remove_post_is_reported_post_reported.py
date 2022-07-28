# Generated by Django 4.0 on 2022-07-18 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_edited_post_is_reported'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_reported',
        ),
        migrations.AddField(
            model_name='post',
            name='reported',
            field=models.PositiveIntegerField(default=False),
        ),
    ]
