# Generated by Django 4.2.1 on 2023-05-27 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_userwallet_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(db_column='OrderId', default=None, max_length=255, null=True),
        ),
    ]
