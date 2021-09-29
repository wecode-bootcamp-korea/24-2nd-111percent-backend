from investments.models import Investment
from django.db import models

from core.models import TimeStamp


class Bank(models.Model):
    class DefaultBank(models.IntegerChoices):
        NH_BANK = 2

    name = models.CharField(max_length=32)

    class Meta:
        db_table = "banks"


class Deposit(models.Model):
    withdrawal_account = models.CharField(max_length=32)
    withdrawal_bank    = models.ForeignKey(Bank, related_name="deposit_withdrawal" ,on_delete=models.PROTECT)
    deposit_account    = models.CharField(max_length=32, unique=True)
    deposit_bank       = models.ForeignKey(Bank, related_name="deposit", on_delete=models.PROTECT)
    balance            = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "deposit"


class TransactionType(models.Model):
    class Type(models.IntegerChoices):
        PAYMENT    = 1
        DEPOSIT    = 2
        WITHDRAWAL = 3
        INVESTMENT = 4

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
    user            = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "repayments"

class InvestmentState(models.Model):
    class State(models.IntegerChoices):
        INVESTING = 1
        COMPLETE  = 2
        LOSS      = 3
    
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "investment_states"


class RepaymentState(models.Model):
    class State(models.IntegerChoices):
        NORMAL  = 1
        DELAY   = 2
        OVERDUE = 3
    
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "repayment_states"


class Portfolio(models.Model):
    user             = models.ForeignKey("users.User", on_delete=models.CASCADE)
    investment       = models.ForeignKey("investments.Investment", on_delete=models.CASCADE)
    amounts          = models.PositiveIntegerField()
    investment_state = models.ForeignKey(InvestmentState, on_delete=models.PROTECT)
    repayment_state  = models.ForeignKey(RepaymentState, on_delete=models.PROTECT)

    class Meta:
        db_table = "portfolios"
