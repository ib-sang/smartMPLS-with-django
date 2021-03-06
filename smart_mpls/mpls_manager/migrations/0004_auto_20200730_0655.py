# Generated by Django 3.0.6 on 2020-07-30 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpls_manager', '0003_auto_20200729_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.CharField(blank=True, choices=[('firewall', 'Firewall'), ('router', 'Router'), ('switch', 'Switch')], default='router', max_length=30),
        ),
        migrations.AlterField(
            model_name='device',
            name='plateform',
            field=models.CharField(blank=True, choices=[('cisco_ios', 'CISCO IOS'), ('cisco_iosxe', 'CISCO IOS XE')], default='cisco_ios', max_length=30),
        ),
        migrations.CreateModel(
            name='Pseudowire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('encapsulation', models.CharField(blank=True, choices=[('mpls1', 'MPLS 1'), ('mpls', 'MPLS')], default='mpls', max_length=30)),
                ('routers', models.ManyToManyField(blank=True, related_name='device_pseu', to='mpls_manager.Device')),
            ],
        ),
    ]
