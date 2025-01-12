# Generated by Django 4.2.11 on 2024-05-17 02:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_alter_category_image_alter_categoryimage_src"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="count",
            field=models.IntegerField(
                default=0,
                validators=[django.core.validators.MinValueValidator],
                verbose_name="Count",
            ),
        ),
    ]
