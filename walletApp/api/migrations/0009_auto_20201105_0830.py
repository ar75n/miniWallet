# Generated by Django 3.1.3 on 2020-11-05 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20201105_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='api',
            name='deposited_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='api',
            name='withdrawn_by',
            field=models.CharField(max_length=100, null=True),
        ),
    ]