# Generated by Django 2.2.6 on 2019-11-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodactivity',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='备注'),
        ),
    ]
