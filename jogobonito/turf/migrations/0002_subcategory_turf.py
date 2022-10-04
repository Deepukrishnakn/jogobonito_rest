# Generated by Django 4.1 on 2022-08-28 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turf.category')),
            ],
        ),
        migrations.CreateModel(
            name='Turf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turf_name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='photos/products')),
                ('image1', models.ImageField(upload_to='photos/products')),
                ('image2', models.ImageField(upload_to='photos/products')),
                ('image3', models.ImageField(upload_to='photos/products')),
                ('is_available', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('SubCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turf.subcategory')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turf.category')),
            ],
        ),
    ]
