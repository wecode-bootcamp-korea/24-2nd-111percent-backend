import json
import unittest

from .models import *
from django.test import TestCase, Client

class InvestmentListTest(TestCase):
    def setUp(self):
        Grade.objects.create(
            id   = 1,
            name = "A+"
        )

        RepaymentType.objects.create(
            id   = 1,
            name = "만기일시"
        )

        Security.objects.create(
            id                     = 1,
            address                = "경기도 김포시",
            completion_date        = "2012년 5월",
            supply_area            = 153.2,
            household              = 465,
            exclusive_private_area = 122.61,
            lease_status           = "본인거주", 
            latitude               = 0.0,
            longitude              = 0.0
        )

        LoanType.objects.create(
            id   = 1,
            name = "부동산 담보 대출"
        )

        BorrowerInformation.objects.create(
            id                = 1,
            credit_score      = 664,
            income_type       = "근로소득",
            income            = 1740000,
            card_usage_amount = 780000,
            loan_amount       = 400000000,
            is_overdue        = "해당 없음",
            overdue_tax       = 0
        )

        InvestmentDetail.objects.create(
            id                   = 1,
            evaluation_price     = 600000000,
            repayment_day        = 25,
            priority_bond_amount = 400000000,
            loan_type_id         = 1,
            bidding_rate         = 103.9
        )

        Investment.objects.create(
            id                = 1,
            name              = "주거안정 406호",
            duration          = 12,
            return_rate       = 8.9,
            target_amount     = 80000000,
            current_amount    = 3600000, 
            borrower_id       = 1,
            detail_id         = 1,
            grade_id          = 1,
            repayment_type_id = 1, 
            security_id       = 1
            )

        Image.objects.create(
            id            = 1,
            url           = "https://landthumb-phinf.pstatic.net/20180418_34/apt_realimage_1524029420450ve1VX_JPEG/d77afbe77d89d520cedebb25ba54c610.jpg?type=m1024",
            investment_id = 1
        )
    
    def tearDown(self):
        Image.objects.all().delete()
        Investment.objects.all().delete()
        InvestmentDetail.objects.all().delete()
        BorrowerInformation.objects.all().delete()
        LoanType.objects.all().delete()
        Security.objects.all().delete()
        RepaymentType.objects.all().delete()
        Grade.objects.all().delete()
    
    def test_success_investmentlist_view_get_method(self):
        client   = Client()
        response = client.get('/investments/listview')
        
        self.assertEqual(response.json(), 
            {"investments" :
                [{
                    'id'               : 1,
                    'name'             : "주거안정 406호",
                    'return_rate'      : 8.9,
                    'duration'         : 12,
                    'target_amount'    : 80000000,
                    'grade'            : "A+",
                    'image'            : "https://landthumb-phinf.pstatic.net/20180418_34/apt_realimage_1524029420450ve1VX_JPEG/d77afbe77d89d520cedebb25ba54c610.jpg?type=m1024",
                    'recrutement_rate' : 4
                }],
            }
        )
        
        self.assertEqual(response.status_code, 200)

    def test_wrong_request_investmentlist_view_get_method(self):
        client   = Client()
        response = client.get('/investment/listview')

        self.assertEqual(response.status_code, 404)


class InvestmentListErrorTest(TestCase):
    def setUp(self):
        Grade.objects.create()
    
    def test_empty_data_investmentlist_view_get_method(self):
        client   = Client()
        response = client.get('/investments/listview')

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json(), {'MESSAGE' : 'INVESTMENTS_DOES_NOT_EXISTS'})


class InvestmentDetailTest(TestCase):
    def setUp(self):
        Grade.objects.create(
            id   = 1,
            name = "A+"
        )

        RepaymentType.objects.create(
            id   = 1,
            name = "만기일시"
        )

        Security.objects.create(
            id                     = 1,
            address                = "경기도 김포시",
            completion_date        = "2012년 5월",
            supply_area            = 153.2,
            household              = 465,
            exclusive_private_area = 122.61,
            lease_status           = "본인거주", 
            latitude               = 37.33,
            longitude              = 126.59
        )

        LoanType.objects.create(
            id   = 1,
            name = "부동산 담보 대출"
        )

        BorrowerInformation.objects.create(
            id                = 1,
            credit_score      = 664,
            income_type       = "근로소득",
            income            = 1740000,
            card_usage_amount = 780000,
            loan_amount       = 400000000,
            is_overdue        = "해당 없음",
            overdue_tax       = 0
        )

        InvestmentDetail.objects.create(
            id                   = 1,
            evaluation_price     = 600000000,
            repayment_day        = 25,
            priority_bond_amount = 400000000,
            loan_type_id         = 1,
            bidding_rate         = 103.9
        )

        Investment.objects.create(
            id                = 1,
            name              = "주거안정 406호 김포 장기동 한강현대성우오스타",
            duration          = 12,
            return_rate       = 8.9,
            target_amount     = 80000000,
            current_amount    = 3600000, 
            borrower_id       = 1,
            detail_id         = 1,
            grade_id          = 1,
            repayment_type_id = 1, 
            security_id       = 1
            )

        Image.objects.create(
            id            = 1,
            url           = "https://landthumb-phinf.pstatic.net/20180418_34/apt_realimage_1524029420450ve1VX_JPEG/d77afbe77d89d520cedebb25ba54c610.jpg?type=m1024",
            investment_id = 1
        )
    
    def tearDown(self):
        Image.objects.all().delete()
        Investment.objects.all().delete()
        InvestmentDetail.objects.all().delete()
        BorrowerInformation.objects.all().delete()
        LoanType.objects.all().delete()
        Security.objects.all().delete()
        RepaymentType.objects.all().delete()
        Grade.objects.all().delete()

    def test_success_investmentdetail_view_get_method(self):
        client   = Client()
        response = client.get('/investments/1')
        
        self.assertEqual(response.json(), 
            {

                "image_list": ["https://landthumb-phinf.pstatic.net/20180418_34/apt_realimage_1524029420450ve1VX_JPEG/d77afbe77d89d520cedebb25ba54c610.jpg?type=m1024"],
                "id": 1,
                "name": "주거안정 406호 김포 장기동 한강현대성우오스타",
                "grade": "A+",
                "return_rate": 8.9,
                "duration": 12,
                "repayment_types": "만기일시",
                "current_ammount": 3600000,
                "target_amount": 80000000,
                "recrutement_rate": 4,
                "LTV": 80.0,
                "repayment_day": 25,
                "loan_type": "부동산 담보 대출",
                "evaluation_price": 600000000,
                "priority_bond_amount": 400000000,
                "security_surcharge": 120000000,
                "bidding_rate": 103.9,
                "expected_recovery": 61940000000.0,
                "address": "경기도 김포시",
                "completion_date": "2012년 5월",
                "household": 465,
                "supply_area": 153.2,
                "exclusive_private_area": 122.61,
                "lease_status": "본인거주",
                "latitude": 37.33,
                "longitude": 126.59,
                "credit_score": 664,
                "income_type": "근로소득",
                "income": 1740000,
                "card_usage_amount": 780000,
                "loan_amount": 400000000,
                "is_overdue": "해당 없음",
                "overdue_tax": 0
                }
            )
        self.assertEqual(response.status_code, 200)

    def test_wrong_request_investmentlist_view_get_method(self):
        client   = Client()
        response = client.get('/investment/listview')

        self.assertEqual(response.status_code, 404)

class InvestmentDetailErrorTest(TestCase):
    def setUp(self):
        Grade.objects.create()
    
    def test_empty_data_investmentdetail_view_get_method(self):
        client   = Client()
        response = client.get('/investments/1')

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json(), {'MESSAGE' : 'NOT_FOUND'})
