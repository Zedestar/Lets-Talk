# Generated by Django 5.0.4 on 2024-04-23 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_post_author_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.profile'),
        ),
    ]
