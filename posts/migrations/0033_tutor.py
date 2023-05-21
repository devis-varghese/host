# Generated by Django 4.1.3 on 2023-02-28 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0032_remove_enrolledstudents_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='media/profile_pic')),
                ('resume', models.FileField(blank=True, null=True, upload_to='media/certificate')),
                ('mobile', models.CharField(max_length=20)),
                ('Country', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]