# Generated by Django 4.0.2 on 2022-06-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operational',
            name='title',
            field=models.CharField(max_length=10),
        ),
    ]
