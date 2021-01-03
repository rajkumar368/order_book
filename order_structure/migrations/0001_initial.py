# Generated by Django 2.2.5 on 2021-01-03 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('dttime', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_id', models.CharField(max_length=100)),
                ('side', models.CharField(choices=[('B', 'Buy_Side'), ('S', 'Sell_Side')], max_length=1)),
                ('order_type', models.CharField(choices=[('MO', 'Market Order'), ('LO', 'Limit Order'), ('So', 'Stop Order')], max_length=2)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('R', 'Rejected')], max_length=1)),
                ('Qty', models.IntegerField(default=0)),
                ('discription', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('product_type', models.CharField(choices=[('I', 'Intraday'), ('D', 'Delivery')], max_length=1)),
                ('ltp', models.IntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_structure.Order')),
            ],
        ),
    ]