from django.db import models

from core.models import TimeStamp


class Bank(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "banks"


class Deposit(models.Model):
    withdrawal_account = models.CharField(max_length=32)
    withdrawal_bank    = models.ForeignKey(Bank, related_name="deposit_withdrawal" ,on_delete=models.PROTECT)
    deposit_account    = models.CharField(max_length=32)
    deposit_bank       = models.ForeignKey(Bank, related_name="deposit", on_delete=models.PROTECT)
    balance            = models.PositiveBigIntegerField()

    class Meta:
        db_table = "deposit"


class TransactionType(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "transaction_types"


class Transaction(TimeStamp):
    type        = models.ForeignKey(TransactionType, null=True, on_delete=models.SET_NULL)
    information = models.CharField(max_length=64)
    amounts     = models.PositiveIntegerField()
    deposit     = models.ForeignKey(Deposit, on_delete=models.PROTECT)
    user        = models.ForeignKey("users.User", on_delete=models.CASCADE)
    investment  = models.ForeignKey(
        "investments.Investment", null=True, on_delete=models.SET_NULL
    )

    class Meta:
        db_table = "transactions"


class Repayment(models.Model):
    transaction     = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    repayment_count = models.PositiveSmallIntegerField()
    principal       = models.PositiveIntegerField()
    interest        = models.PositiveIntegerField()
    tax             = models.PositiveIntegerField()
    charge          = models.PositiveIntegerField()

    class Meta:
        db_table = "repayments"
