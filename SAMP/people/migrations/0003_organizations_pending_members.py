# Generated by Django 2.2.3 on 2019-07-16 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20190716_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizations',
            name='pending_members',
            field=models.ManyToManyField(related_name='organization_pending_members', to='people.User_info'),
        ),
    ]
