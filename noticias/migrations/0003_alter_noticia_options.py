# Generated by Django 4.0.3 on 2022-04-06 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_alter_noticia_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticia',
            options={'ordering': ['-data_noticia']},
        ),
    ]
