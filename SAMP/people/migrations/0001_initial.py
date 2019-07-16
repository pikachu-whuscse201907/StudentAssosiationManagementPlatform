# Generated by Django 2.2.3 on 2019-07-16 02:15

from django.db import migrations, models
import django.db.models.deletion
import people.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClubPronounces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('create_date', models.DateTimeField()),
                ('content', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pswd', models.CharField(max_length=256)),
                ('cookie_id', models.CharField(max_length=256, null=True)),
                ('cookie_create_time', models.DateTimeField(blank=True, null=True)),
                ('cookie_expire', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motto', models.CharField(default='', max_length=100)),
                ('gender', models.IntegerField(choices=[(0, 'UNKNOWN'), (1, 'MALE'), (2, 'FEMALE')], default=0)),
                ('birth_date', models.DateTimeField(null=True)),
                ('profile', models.ImageField(default='default_user_logo.jpg', upload_to=people.models.user_logo_path)),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('organization_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('org_logo', models.ImageField(default='default_org_logo.jpg', upload_to=people.models.org_logo_path)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='organization_creator', to='people.User_info')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_master', to='people.User_info')),
                ('members', models.ManyToManyField(related_name='organization_members', to='people.User_info')),
                ('pronounces', models.ManyToManyField(related_name='organization_pronounces', to='people.ClubPronounces')),
            ],
        ),
        migrations.AddField(
            model_name='clubpronounces',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clubpronounce_publisher', to='people.User_info'),
        ),
    ]