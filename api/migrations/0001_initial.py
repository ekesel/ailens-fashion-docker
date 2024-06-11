# Generated by Django 4.2.13 on 2024-06-11 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='outfit/')),
                ('binary_code', models.CharField(blank=True, max_length=1000, null=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.client')),
            ],
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('Time', 'Time'), ('Per Req', 'Per Req'), ('Bulk Buy', 'Bulk Buy')], max_length=100)),
                ('start_dt', models.DateTimeField(blank=True, null=True)),
                ('end_dt', models.DateTimeField(blank=True, null=True)),
                ('req_allowed', models.IntegerField(blank=True, null=True)),
                ('price', models.CharField(blank=True, max_length=1000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.client')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('over_spend_charge', models.CharField(blank=True, max_length=1000, null=True)),
                ('billed_amount', models.CharField(blank=True, max_length=1000, null=True)),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.billing')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.client')),
            ],
        ),
    ]