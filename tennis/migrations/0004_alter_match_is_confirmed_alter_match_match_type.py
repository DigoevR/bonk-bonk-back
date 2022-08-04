# Generated by Django 4.0 on 2022-08-04 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tennis', '0003_match_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='is_confirmed',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='match_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Best of 1'), (3, 'Best of 3'), (5, 'Best of 5')], db_index=True),
        ),
    ]