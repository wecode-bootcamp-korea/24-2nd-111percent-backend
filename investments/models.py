from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "grades"


class RepaymentType(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = "repayment_types"


class Security(models.Model):
    address                = models.CharField(max_length=128)
    completion_date        = models.CharField(max_length=32)
    supply_area            = models.FloatField()
    household              = models.PositiveSmallIntegerField()
    exclusive_private_area = models.FloatField()
    lease_status           = models.CharField(max_length=16)
    latitude               = models.FloatField(default=0.0)
    longitude              = models.FloatField(default=0.0)

    class Meta:
        db_table = "securities"


class LoanType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "loan_types"


class InvestmentDetail(models.Model):
    loan_type            = models.ForeignKey(LoanType, on_delete=models.PROTECT)
    evaluation_price     = models.PositiveBigIntegerField()
    repayment_day        = models.PositiveSmallIntegerField()
    priority_bond_amount = models.PositiveIntegerField()

    class Meta:
        db_table = "investment_details"


class BorrowerInformation(models.Model):
    credit_score      = models.PositiveSmallIntegerField()
    income_type       = models.CharField(max_length=32)
    income            = models.PositiveIntegerField()
    card_usage_amount = models.PositiveIntegerField()
    loan_amount       = models.PositiveIntegerField(null=True)
    is_overdue        = models.CharField(max_length=32, null=True)
    overdue_tax       = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = "borrower_informations"


class Investment(models.Model):
    name           = models.CharField(max_length=64)
    grade          = models.ForeignKey(Grade, on_delete=models.PROTECT)
    duration       = models.PositiveSmallIntegerField()
    repayment_type = models.ForeignKey(RepaymentType, on_delete=models.PROTECT)
    return_rate    = models.FloatField()
    target_amount  = models.IntegerField()
    current_amount = models.IntegerField()
    detail         = models.ForeignKey(InvestmentDetail, on_delete=models.CASCADE)
    security       = models.ForeignKey(Security, on_delete=models.PROTECT)
    borrower       = models.ForeignKey(BorrowerInformation, on_delete=models.PROTECT)

    class Meta:
        db_table = "investments"


class Image(models.Model):
    url        = models.URLField(max_length=256)
    investment = models.IntegerField()

    class Meta:
        db_table = "images"
