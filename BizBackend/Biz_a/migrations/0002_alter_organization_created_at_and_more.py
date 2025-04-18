# Generated by Django 5.1.7 on 2025-03-30 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Biz_a', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='linkedin',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='organization',
            name='responsible_person',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='webpage',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
