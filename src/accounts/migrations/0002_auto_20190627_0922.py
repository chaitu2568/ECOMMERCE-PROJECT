# Generated by Django 2.2.1 on 2019-06-27 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guestemail',
            old_name='email',
            new_name='Email',
        ),
    ]
