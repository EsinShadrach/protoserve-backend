# Generated by Django 4.1.2 on 2023-05-27 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_school_name_education_name_delete_person'),
    ]

    operations = [
        migrations.RenameField(
            model_name='education',
            old_name='name',
            new_name='school_name',
        ),
    ]
