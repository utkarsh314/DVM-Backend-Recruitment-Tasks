# Generated by Django 4.0 on 2022-07-24 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('posts', '0004_reportedpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='reported',
        ),
        migrations.AddField(
            model_name='post',
            name='reports',
            field=models.ManyToManyField(to='users.Profile'),
        ),
    ]
