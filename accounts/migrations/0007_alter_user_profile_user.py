# Generated by Django 5.0.6 on 2024-09-20 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_user',
            field=models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Image '),
        ),
    ]
