# Generated by Django 3.2.18 on 2023-10-28 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20231028_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gadget',
            name='status',
        ),
    ]
