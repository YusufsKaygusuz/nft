# Generated by Django 5.1 on 2024-09-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcweb', '0002_topusers_alter_exploreitem_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=100)),
                ('banner_image', models.ImageField(upload_to='collection_banners/')),
                ('avatar_image', models.ImageField(upload_to='collection_avatars/')),
                ('erc_code', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
