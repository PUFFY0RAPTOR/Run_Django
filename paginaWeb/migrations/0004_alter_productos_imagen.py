# Generated by Django 4.0.6 on 2022-10-11 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginaWeb', '0003_productos_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(default='RUN/imagProductos/default.png', upload_to='RUN/imagProductos'),
        ),
    ]
