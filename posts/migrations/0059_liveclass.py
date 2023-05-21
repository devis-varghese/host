# Generated by Django 4.1.3 on 2023-03-29 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0058_delete_liveclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='live_classes', to='posts.post')),
            ],
        ),
    ]