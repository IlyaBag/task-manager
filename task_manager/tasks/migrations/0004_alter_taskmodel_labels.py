# Generated by Django 4.2.6 on 2023-12-24 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0003_remove_labelmodel_tasks'),
        ('tasks', '0003_taskmodel_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='labels',
            field=models.ManyToManyField(to='labels.labelmodel', verbose_name='Labels'),
        ),
    ]