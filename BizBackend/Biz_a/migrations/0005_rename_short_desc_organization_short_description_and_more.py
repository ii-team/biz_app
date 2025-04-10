# Generated by Django 5.0.4 on 2025-04-10 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Biz_a', '0004_organization_company_logo_organization_short_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='short_desc',
            new_name='short_description',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='pdf',
        ),
        migrations.AddField(
            model_name='organization',
            name='company_banner',
            field=models.FileField(blank=True, null=True, upload_to='static/company_banners/'),
        ),
        migrations.AddField(
            model_name='organization',
            name='iiealra_index_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='company_logo',
            field=models.FileField(blank=True, null=True, upload_to='static/company_logos/'),
        ),
    ]
