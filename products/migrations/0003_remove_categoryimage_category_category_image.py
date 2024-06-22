# Generated by Django 4.2.11 on 2024-05-17 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_categoryimage_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="categoryimage",
            name="category",
        ),
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="products.categoryimage",
            ),
        ),
    ]