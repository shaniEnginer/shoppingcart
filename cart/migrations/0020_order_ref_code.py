# Generated by Django 3.0.4 on 2020-05-09 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0019_auto_20200509_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
