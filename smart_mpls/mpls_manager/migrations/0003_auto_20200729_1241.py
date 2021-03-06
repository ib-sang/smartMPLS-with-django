# Generated by Django 3.0.6 on 2020-07-29 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpls_manager', '0002_auto_20200729_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='protocol',
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(blank=True, choices=[('switch', 'Switch'), ('router', 'Router'), ('firewall', 'Firewall')], default='router', max_length=30),
        ),
        migrations.AlterField(
            model_name='device',
            name='plateform',
            field=models.CharField(blank=True, choices=[('cisco_iosxe', 'CISCO IOS XE'), ('cisco_ios', 'CISCO IOS')], default='cisco_ios', max_length=30),
        ),
    ]
