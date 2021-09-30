import json

from django.test import TestCase, Client

from transactions.models import (
    Deposit,
    TransactionType,
    Deposit,
    Bank,
    InvestmentState,
    RepaymentState,
    Portfolio,
)

from transactions.models import Deposit, TransactionType, Deposit, Bank, Transaction

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

        InvestmentState.objects.create(id=1, name="투자중")

        RepaymentState.objects.create(id=1, name="정상")


    def tearDown(self):
        TransactionType.objects.all().delete()
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
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
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
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
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
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
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
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
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
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
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
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfF"
        }
        response = client.post(
            "/transactions/invest/1",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_TOKEN"})


class DepositTransition(TestCase):
    def setUp(self):
        Bank.objects.create(id=2, name="농협은행")

        Deposit.objects.create(
            id=1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=2,
            deposit_account="444-555-666",
            deposit_bank_id=2,
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

        TransactionType.objects.create(id=2, name="입금")

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()

    def test_deposit_transaction_post_success(self):
        client = Client()
        deposit_amounts = {"amounts": 300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/deposit",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 201)

    def test_deposit_transaction_post_invalid_input(self):
        client = Client()
        deposit_amounts = {"amounts": -300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/deposit",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT"})

    def test_deposit_transaction_post_type_error(self):
        client = Client()
        deposit_amounts = {"amounts": "300000"}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/deposit",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "TYPE_ERROR"})

    def test_deposit_transaction_post_key_error(self):
        client = Client()
        deposit_amounts = {"amount": 300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/deposit",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_deposit_transaction_post_invalid_token(self):
        client = Client()
        invest_amount = {"amounts": 300000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfF"
        }
        response = client.post(
            "/transactions/deposit",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_TOKEN"})


class PortfolioTest(TestCase):
    maxDiff = None

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

        InvestmentState.objects.bulk_create(
            [
                InvestmentState(id=1, name="투자중"),
                InvestmentState(id=2, name="투자완료"),
                InvestmentState(id=3, name="손실"),
            ]
        )

        RepaymentState.objects.bulk_create(
            [
                RepaymentState(id=1, name="정상"),
                RepaymentState(id=2, name="상환지연"),
                RepaymentState(id=3, name="연체"),
            ]
        )

        Portfolio.objects.create(
            id=1,
            user_id=2,
            investment_id=1,
            amounts=600000,
            investment_state_id=1,
            repayment_state_id=1,
        )

    def tearDown(self):
        Portfolio.objects.all().delete()
        RepaymentState.objects.all().delete()
        InvestmentState.objects.all().delete()
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

    def test_portfolio_get_success(self):
        client = Client()
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.get(
            "/transactions/portfolio", content_type="application/json", **header
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "results": {
                    "deposit_information": {
                        "withdrawal_account": "농협은행111-222-333",
                        "deposit_account": "농협은행444-555-666",
                        "deposit_balance": 300000,
                        "gross_investment_limit": 29400000,
                        "real_estate_investment_limit": 9400000,
                    },
                    "investment_general_infomation": {
                        "rate_of_return": 8.9,
                        "assets": 900000,
                        "cumulative_profit": None,
                    },
                    "investment_current_condition": {
                        "investing_amount": 600000,
                        "invest_completed_amount": None,
                        "loss_amount": None,
                        "investing_normal_amount": 600000,
                        "investing_delay_amount": None,
                        "investing_overdue_amount": None,
                    },
                    "portfolio_current_condition": {
                        "grade": {
                            "A": 600000,
                            "B": None,
                            "C": None,
                            "D": None,
                        },
                        "return_rate": {
                            "8_under": None,
                            "8_over_or_equal": 600000,
                            "10_over_or_equal": None,
                            "12_over_or_equal": None,
                        },
                    },
                }
            },
        )

    def test_portfolio_get_invalid_token(self):
        client = Client()
        header = {
            "HTTP_Authorization": "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0._fleYhEIx5512GwejJ70cid7blXOsKEmcbf5zeHBHtA"
        }
        response = client.get(
            "/transactions/portfolio", content_type="application/json", **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_TOKEN"})


class TransactionInformationTest(TestCase):
    def setUp(self):
        Bank.objects.create(id=2, name="농협은행")

        Deposit.objects.create(
            id                =1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=2,
            deposit_account   ="444-555-666",
            deposit_bank_id   =2,
            balance           =300000,
        )

        User.objects.create(
            id          =2,
            name        ="무현",
            email       ="example@naver.com",
            phone_number="010-2222-4444",
            password    ="1234dfsdflker@!",
            deposit_id  =1,
        )
        TransactionType.objects.create(
            id  =4,
            name="투자"
        )

        Transaction.objects.create(
            id         =1,
            type_id    =4,
            information="주거안정 406호",
            amounts    =100000,
            deposit_id =1,
            user_id    =2,
        )

    def tearDown(self):
        Transaction.objects.all().delete()
        TransactionType.objects.all().delete()
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()

    def test_transaction_information_get_success(self):
        client = Client()
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.get('/transactions/transaction', content_type="application/json", **header)
        transaction = Transaction.objects.get(id=1)
        
        self.assertEqual(response.json(), 
            {"transactions" :
                [{
                    'created_time' : transaction.created_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
                    'type'         : "투자",
                    'information'  : "주거안정 406호",
                    'amounts'      : 100000,
                }],
            }
        )
        
        self.assertEqual(response.status_code, 200)

class WithdrawalTest(TestCase):
    def setUp(self):
        TransactionType.objects.create(id=3, name="출금")

        Bank.objects.create(id=2, name="농협은행")

        Deposit.objects.create(
            id=1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=2,
            deposit_account="444-555-666",
            deposit_bank_id=2,
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

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        TransactionType.objects.all().delete()

    def test_withdrawal_post_success(self):
        client = Client()
        deposit_amounts = {"amounts": 100000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 201)

    def test_withdrawal_post_invalid_input(self):
        client = Client()
        deposit_amounts = {"amounts": -100000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT"})

    def test_withdrawal_post_exceed_input(self):
        client = Client()
        deposit_amounts = {"amounts": 1000000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "WRONG_REQUEST"})

    def test_withdrawal_post_type_error(self):
        client = Client()
        deposit_amounts = {"amounts": "100000"}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "TYPE_ERROR"})

    def test_withdrawal_post_key_error(self):
        client = Client()
        deposit_amounts = {"amount": 100000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfFg"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(deposit_amounts),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_withdrawal_post_invalid_token(self):
        client = Client()
        invest_amount = {"amounts": 100000}
        header = {
            "HTTP_Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.G9SKGv3338DXgNWbuVLZ8n3NZHHbo8VQtr3lp_8UfF"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(invest_amount),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_TOKEN"})