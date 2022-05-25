# Generated by Django 2.2 on 2022-05-25 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_api', '0003_auto_20220525_0938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messageitem',
            old_name='recipient',
            new_name='recipient_id',
        ),
        migrations.RemoveField(
            model_name='messageitem',
            name='sender',
        ),
        migrations.AddField(
            model_name='messageitem',
            name='sender_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]