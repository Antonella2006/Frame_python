# Generated by Django 5.1.5 on 2025-01-30 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voitures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
