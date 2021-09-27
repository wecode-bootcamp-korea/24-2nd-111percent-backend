import json

from django.test import TestCase, Client

from transactions.models import Deposit, TransactionType, Deposit, Bank
from investments.models import (
    Grade,
    RepaymentType,
    LoanType,
    Security,
    BorrowerInformation,
    InvestmentDetail,
    Investment,
)
from users.models import User


class InvestTransactionTest(TestCase):
    def setUp(self):
        Grade.objects.create(id=1, name="A+")
        RepaymentType.objects.create(id=1, name="만기일시")
        LoanType.objects.create(id=1, name="부동산 담보 대출")

        Security.objects.create(
            id=1,
            address="경기도 김포시",
            completion_date="2012년 5월",
            supply_area=153.20,
            household=465,
            exclusive_private_area=122.61,
            lease_status="본인거주",
        )

        BorrowerInformation.objects.create(
            id=1,
            credit_score=664,
            income_type="근로소득",
            income=1740000,
            card_usage_amount=780000,
            loan_amount=400000000,
            is_overdue="해당 없음",
        )

        InvestmentDetail.objects.create(
            id=1,
            loan_type_id=1,
            evaluation_price=600000000,
            repayment_day=25,
            priority_bond_amount=400000000,
        )

        Investment.objects.create(
            id=1,
            name="주거안정 406호",
            grade_id=1,
            duration=12,
            repayment_type_id=1,
            return_rate=8.9,
            target_amount=80000000,
            current_amount=3600000,
            detail_id=1,
            security_id=1,
            borrower_id=1,
        )

        Bank.objects.create(id=1, name="농협은행")

        Deposit.objects.create(
            id=1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=1,
            deposit_account="444-555-666",
            deposit_bank_id=1,
            balance=300000,
        )

        User.objects.create(
            id=2,
            name="무현",
            email="example@naver.com",
            phone_number="010-2222-4444",
            password="1234dfsdflker@!",
            deposit_id=1,
        )

        TransactionType.objects.create(id=4, name="투자")

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        Investment.objects.all().delete()
        InvestmentDetail.objects.all().delete()
        BorrowerInformation.objects.all().delete()
        Security.objects.all().delete()
        LoanType.objects.all().delete()
        RepaymentType.objects.all().delete()
        Grade.objects.all().delete()

    def test_invest_transaction_post_success(self):
        client = Client()
        invest_amount = {"amounts": 300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.post(
            "/transactions/invest/1",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_invest_transaction_post_invalid_input(self):
        client = Client()
        invest_amount = {"amounts": -300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.post(
            "/transactions/invest/1",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT"})

    def test_invest_transaction_post_invalid_investment_id(self):
        client = Client()
        invest_amount = {"amounts": 300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.post(
            "/transactions/invest/2",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "INVALID_INVESTMENT_ID"})

    def test_invest_transaction_post_invalid_type(self):
        client = Client()
        invest_amount = {"amounts": "300000"}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.post(
            "/transactions/invest/1",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "TYPE_ERROR"})

    def test_invest_transaction_post_invalid_keys(self):
        client = Client()
        invest_amount = {"amount": 300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.post(
            "/transactions/invest/1",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_invest_transaction_post_invalid_token(self):
        client = Client()
        invest_amount = {"amounts": 300000}
        header = {
            "HTTP_Authorization": "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.post(
            "/transactions/invest/1",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_TOKEN"})
