# Generated by Django 2.2.4 on 2019-11-30 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20191118_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentvalue',
            options={'ordering': ('id',)},
        ),
    ]