# Generated by Django 2.2.3 on 2019-09-26 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizacao', '0003_trabalhofogao_trabalhogeladeira'),
    ]

    operations = [
        migrations.AddField(
            model_name='geladeira',
            name='numGeladeira',
            field=models.IntegerField(default=0),
        ),
    ]
