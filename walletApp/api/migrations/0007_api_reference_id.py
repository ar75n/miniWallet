# Generated by Django 3.1.3 on 2020-11-05 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201105_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='api',
            name='reference_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
