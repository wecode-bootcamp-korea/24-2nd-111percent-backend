# Generated by Django 3.2.7 on 2021-09-14 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('investments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'banks',
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawal_account', models.CharField(max_length=32)),
                ('deposit_account', models.CharField(max_length=32)),
                ('balance', models.PositiveBigIntegerField()),
            ],
            options={
                'db_table': 'deposit',
            },
        ),
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repayment_count', models.PositiveSmallIntegerField()),
                ('principal', models.PositiveIntegerField()),
                ('interest', models.PositiveIntegerField()),
                ('tax', models.PositiveIntegerField()),
                ('charge', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'repayments',
            },
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'transaction_types',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('information', models.CharField(max_length=64)),
                ('amounts', models.PositiveIntegerField()),
                ('deposit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.deposit')),
                ('investment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='investments.investment')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transactions.transactiontype')),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
    ]