# Generated by Django 3.2.8 on 2021-10-26 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('code', models.CharField(default='#007bff', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img1', models.ImageField(upload_to=products.models.product_image_path)),
                ('img2', models.ImageField(blank=True, null=True, upload_to=products.models.product_image_path)),
                ('img3', models.ImageField(blank=True, null=True, upload_to=products.models.product_image_path)),
                ('img4', models.ImageField(blank=True, null=True, upload_to=products.models.product_image_path)),
                ('img5', models.ImageField(blank=True, null=True, upload_to=products.models.product_image_path)),
                ('video_link', models.URLField(blank=True, help_text='http://', max_length=500, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(null=True)),
                ('manufacturer', models.CharField(blank=True, help_text='Make/Brand/Manufacturer', max_length=120, null=True)),
                ('origin', models.CharField(blank=True, max_length=120, null=True)),
                ('condition', models.CharField(choices=[('New', 'New'), ('Used', 'Used'), ('Refurbished', 'Refurbished')], max_length=120)),
                ('product_type', models.CharField(blank=True, help_text='eg. Laptop, Engine, Building, Shirt, etc.', max_length=120, null=True)),
                ('weight', models.FloatField(blank=True, help_text='Value should be in kg', null=True)),
                ('base_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('shipping_in_city', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('shipping_in_country', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('shipping_out_country', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True)),
                ('stock_initial', models.PositiveIntegerField(default=1)),
                ('stock_remaining', models.PositiveIntegerField(default=0)),
                ('featured', models.BooleanField(default=False)),
                ('sponsored', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('is_digital', models.BooleanField(default=False)),
                ('product_info', models.TextField(blank=True, null=True)),
                ('warranty_info', models.TextField(blank=True, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('shipping_info', models.TextField(blank=True, null=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=120, unique=True)),
                ('color', models.CharField(default='#007bff', max_length=7)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='SizeVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(blank=True, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productcategory')),
            ],
            options={
                'verbose_name': 'Sub category',
                'verbose_name_plural': 'Sub categories',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_subject', models.CharField(max_length=100)),
                ('review_rating', models.CharField(choices=[('FIVESTAR', '5 Stars'), ('FOURSTAR', '4 Stars'), ('THREESTAR', '3 Stars'), ('TWOSTAR', '2 Stars'), ('ONESTAR', '1 Star')], max_length=9)),
                ('review_comment', models.TextField()),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
                'ordering': ['-pk'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='products.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, to='products.ColorVariation'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, to='products.SizeVariation'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.subcategory'),
        ),
    ]