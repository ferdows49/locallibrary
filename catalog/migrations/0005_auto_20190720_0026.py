# Generated by Django 2.2.3 on 2019-07-19 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_book_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['first_name', 'last_name']},
        ),
    ]
