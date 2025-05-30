# Generated by Django 5.1.4 on 2024-12-21 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Inconnu', max_length=150)),
                ('email', models.EmailField(default='no_email@mail.com', max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('image', models.ImageField(default='no_image', upload_to='images')),
                ('matricule', models.CharField(max_length=22, null=True, unique=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='user.role')),
            ],
        ),
    ]
