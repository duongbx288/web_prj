# Generated by Django 3.2.8 on 2021-11-11 04:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('NormalUser', '0002_auto_20211111_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaldeclaration',
            name='declarationTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 11, 4, 52, 55, 523037, tzinfo=utc)),
        ),
    ]