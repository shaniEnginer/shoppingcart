# Generated by Django 3.0.4 on 2020-05-01 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20200501_0722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='chatergory',
            new_name='catergory',
        ),
    ]