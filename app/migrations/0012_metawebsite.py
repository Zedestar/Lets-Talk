# Generated by Django 5.0.4 on 2024-04-24 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_post_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('about', models.TextField()),
            ],
        ),
    ]
