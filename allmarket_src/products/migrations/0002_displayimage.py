# Generated by Django 3.2.8 on 2021-10-29 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider1', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('slider1a', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('slider2', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('slider2a', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('slider3', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('slider3a', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('advertise1', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('advertise2', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('advertise3', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display1', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display2', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display3', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display4', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display5', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display6', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display7', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display8', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display9', models.ImageField(blank=True, null=True, upload_to='Display_images')),
                ('display0', models.ImageField(blank=True, null=True, upload_to='Display_images')),
            ],
        ),
    ]
