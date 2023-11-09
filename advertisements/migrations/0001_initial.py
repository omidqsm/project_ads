# Generated by Django 4.2.7 on 2023-11-09 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('text', models.CharField(max_length=1000)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('text', models.CharField(max_length=1000)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='advertisements.advertisement')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='comment',
            constraint=models.UniqueConstraint(fields=('advertisement', 'owner'), name='user_ad_uq'),
        ),
    ]