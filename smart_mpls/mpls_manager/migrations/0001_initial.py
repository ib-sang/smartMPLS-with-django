# Generated by Django 3.0.6 on 2020-07-26 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('host', models.CharField(max_length=70)),
                ('device_type', models.CharField(blank=True, choices=[('switch', 'Switch'), ('router', 'Router'), ('firewall', 'Firewall')], default='router', max_length=30)),
                ('plateform', models.CharField(blank=True, choices=[('cisco_ios', 'CISCO IOS'), ('cisco_iosxe', 'CISCO IOS XE')], default='cisco_ios', max_length=30)),
                ('management', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mpls_manager.Access')),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ingress', models.BooleanField(default=False)),
                ('egress', models.BooleanField(default=False)),
                ('backbone', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Topologies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vrf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rd', models.CharField(max_length=255)),
                ('routeImport', models.CharField(max_length=255)),
                ('routeExport', models.CharField(max_length=255)),
                ('devices', models.ManyToManyField(blank=True, related_name='device', to='mpls_manager.Device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='topology_ref',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mpls_manager.Topologies'),
        ),
    ]