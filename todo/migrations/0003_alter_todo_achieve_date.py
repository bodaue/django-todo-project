# Generated by Django 4.2.3 on 2023-08-03 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_remove_todo_status_todo_important_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='achieve_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата выполнения'),
        ),
    ]