import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from investments.models import *

CSV_PATH_PRODUCTS = "investment.csv"

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    for row in data_reader:
        if not Grade.objects.filter(name = row[1]).exists:
            grade = Grade.objects.create(name = row[1])
        else:
            grade = Grade.objects.get(name = row[1])
        
        if not RepaymentType.objects.filter(name = row[2]):
            repayment_type = RepaymentType.objects.create(name = row[2])
        else:
            repayment_type = RepaymentType.objects.get(name = row[2])
        
        security = Security.objects.create(
            address                = row[3], 
            completion_date        = row[4], 
            supply_area            = row[5], 
            household              = row[6], 
            exclusive_private_area = row[7], 
            lease_status           = row[8], 
            latitude               = row[9], 
            longitude              = row[10]
        )

        if not LoanType.objects.filter(name = row[11]).exists:
            loan_type = LoanType.objects.create(name = row[11])
        else:
            loan_type = LoanType.objects.get(name = row[11])

        borrower_information = BorrowerInformation.objects.create(
            credit_score      = row[12], 
            income_type       = row[13], 
            income            = row[14], 
            card_usage_amount = row[15], 
            loan_amount       = row[16], 
            is_overdue        = row[17], 
            overdue_tax       = row[18]
        )

        investment_detail = InvestmentDetail.objects.create(
            loan_type            = loan_type, 
            evaluation_price     = row[20], 
            repayment_day        = row[21], 
            priority_bond_amount = row[22], 
            bidding_rate         = row[23]
        )

        investment = Investment.objects.create(
            name           = row[24], 
            grade          = grade, 
            duration       = row[26], 
            repayment_type = repayment_type, 
            return_rate    = row[27], 
            target_amount  = row[28], 
            current_amount = row[29], 
            detail         = investment_detail,
            security       = security, 
            borrower       = borrower_information
        )

        image = Image.objects.create(
            url       = row[33], 
            investment = investment
        )
