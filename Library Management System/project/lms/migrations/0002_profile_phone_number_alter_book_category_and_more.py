# Generated by Django 5.0.6 on 2024-06-03 01:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default=' ', max_length=30),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Economy', 'Economy'), ('Litrature', 'Litrature'), ('Social Science', 'Social Science'), ('Religion', 'Religion'), ('Information Technology', 'Information Technology'), ('Management', 'Management'), ('Arts', 'Arts'), ('Phsycology', 'Phsycology'), ('General', 'General'), ('Physics', 'Physics'), ('Science', 'Science')], max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
