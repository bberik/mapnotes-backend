# Generated by Django 4.2.4 on 2023-08-20 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_node_body_delete_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='is_expanded',
            field=models.BooleanField(default=True),
        ),
    ]
