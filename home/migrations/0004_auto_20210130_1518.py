# Generated by Django 3.1.4 on 2021-01-30 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210130_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='discription',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]