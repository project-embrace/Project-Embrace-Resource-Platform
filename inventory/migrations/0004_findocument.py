# Generated by Django 2.2.4 on 2019-11-18 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0003_auto_20190909_1621'),
        ('inventory', '0003_auto_20191118_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('document_file', models.FileField(max_length=5000, upload_to=inventory.models.document_path)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=64)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_uploaded++', to=settings.AUTH_USER_MODEL)),
                ('shared_to', models.ManyToManyField(related_name='_findocument_shared_to_+', to=settings.AUTH_USER_MODEL)),
                ('teams', models.ManyToManyField(related_name='_findocument_teams_+', to='teams.Teams')),
            ],
            options={
                'ordering': ('-created_on',),
            },
        ),
    ]