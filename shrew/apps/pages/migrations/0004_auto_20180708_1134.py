# Generated by Django 2.0.7 on 2018-07-08 11:34

from django.db import migrations, models
import shrew.apps.pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=shrew.apps.pages.models.Attachment.upload_folder),
        ),
    ]