# Generated by Django 4.1.3 on 2022-11-07 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_telegram', '0002_botconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botconfig',
            name='id',
            field=models.TextField(editable=False, primary_key=True, serialize=False),
        ),
    ]
