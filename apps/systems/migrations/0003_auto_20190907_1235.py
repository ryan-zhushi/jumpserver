# Generated by Django 2.1.7 on 2019-09-07 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('systems', '0002_auto_20190907_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='systems', to='systems.Department', verbose_name='Department'),
        ),
    ]
