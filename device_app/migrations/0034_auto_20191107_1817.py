# Generated by Django 2.2.4 on 2019-11-07 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_app', '0033_auto_20191107_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='country',
            field=models.CharField(max_length=265),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='region',
            field=models.CharField(max_length=265),
        ),
        migrations.AlterField(
            model_name='donor',
            name='country',
            field=models.CharField(max_length=265),
        ),
        migrations.AlterField(
            model_name='donor',
            name='region',
            field=models.CharField(max_length=265),
        ),
    ]
