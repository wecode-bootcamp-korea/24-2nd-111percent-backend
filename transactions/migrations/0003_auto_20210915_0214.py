# Generated by Django 3.2.7 on 2021-09-15 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
