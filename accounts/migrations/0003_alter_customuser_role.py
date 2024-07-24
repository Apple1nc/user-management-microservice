# Generated by Django 5.0.6 on 2024-07-20 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'User'), ('shop owner', 'Shopowner')], default='user', max_length=20, null=True),
        ),
    ]
