# Generated by Django 3.0.4 on 2020-05-09 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_item_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=22)),
            ],
        ),
    ]