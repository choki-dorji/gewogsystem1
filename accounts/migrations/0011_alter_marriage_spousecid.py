# Generated by Django 4.1 on 2022-11-14 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_delete_childdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marriage',
            name='Spousecid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.userdata'),
        ),
    ]