# Generated by Django 4.2.1 on 2023-05-19 08:15

from django.db import migrations, models
import fapva.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(db_column='File', default=None, null=True, upload_to=fapva.utils.image_directory_path)),
            ],
            options={
                'db_table': 'Pro_Wears_Images',
            },
        ),
    ]
