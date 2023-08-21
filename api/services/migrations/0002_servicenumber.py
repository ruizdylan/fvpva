# Generated by Django 4.2.1 on 2023-05-20 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_countries_is_deleted'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.BigIntegerField(blank=True, db_column='CreatedBy', default=0, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='CreatedOn')),
                ('modified_by', models.BigIntegerField(blank=True, db_column='ModifiedBy', default=0, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, db_column='ModifiedOn')),
                ('number', models.TextField(db_column='Number', default=None, null=True)),
                ('price', models.FloatField(db_column='Price', default=0, null=True)),
                ('is_active', models.BooleanField(db_column='IsActive', default=True)),
                ('is_deleted', models.BooleanField(db_column='IsDeleted', default=False)),
                ('country', models.ForeignKey(db_column='CountryId', on_delete=django.db.models.deletion.CASCADE, related_name='country_service', to='main.countries')),
                ('service', models.ForeignKey(db_column='ServiceId', on_delete=django.db.models.deletion.CASCADE, related_name='number_service', to='services.services')),
            ],
            options={
                'db_table': 'Services_Number',
            },
        ),
    ]