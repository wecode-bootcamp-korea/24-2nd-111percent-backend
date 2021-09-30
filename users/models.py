from django.db import models


class User(models.Model):
    name         = models.CharField(max_length=32, null=True)
    email        = models.CharField(max_length=64, unique=True)
    phone_number = models.CharField(max_length=32, null=True)
    password     = models.CharField(max_length=128, null=True)
    deposit      = models.ForeignKey("transactions.Deposit", null=True, on_delete=models.PROTECT)
    kakao_id     = models.BigIntegerField(null=True)

    class Meta:
        db_table = "users"
