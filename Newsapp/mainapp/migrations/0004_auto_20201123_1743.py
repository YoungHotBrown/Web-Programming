# Generated by Django 3.1.1 on 2020-11-23 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20201121_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='interest_tag',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
