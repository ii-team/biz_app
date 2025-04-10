# Generated by Django 5.0.4 on 2025-04-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Biz_a', '0003_organization_active_alter_organization_pdf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='company_logo',
            field=models.FileField(blank=True, null=True, upload_to='static/profile_images/'),
        ),
        migrations.AddField(
            model_name='organization',
            name='short_desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
