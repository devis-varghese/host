# Generated by Django 4.1.3 on 2023-03-19 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0043_post_assigned_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='assigned_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tutors', to='posts.post'),
        ),
    ]
