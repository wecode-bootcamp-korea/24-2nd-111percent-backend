from django.views import View
from django.http import JsonResponse

from .models import Investment, Image


class InvestmentListView(View):
    def get(self, request):
        if not Investment.objects.exists():
            return JsonResponse({'MESSAGE' : 'INVESTMENTS_DOES_NOT_EXISTS'}, status = 404)

        investments = Investment.objects.prefetch_related("image_set").all()

        return JsonResponse({"investments" : [
            {
                "id"               : investment.id,
                "name"             : investment.name,
                "return_rate"      : investment.return_rate,
                "duration"         : investment.duration,
                "target_amount"    : investment.target_amount,
                "grade"            : investment.grade.name,
                "image"            : investment.image_set.all().first().url,
                "recrutement_rate" : int(investment.current_amount/investment.target_amount*100)
            } for investment in investments]}, status = 200)


class InvestmentDetailView(View):
    def get(self, request, investment_id):
        if not Investment.objects.filter(id = investment_id).exists():
            return JsonResponse({'MESSAGE' : 'NOT_FOUND'}, status = 404)

        investment = Investment.objects.select_related("grade", "repayment_type", "detail", "security", "borrower").prefetch_related("image_set").get(id = investment_id)
        images = investment.image_set.all()

        return JsonResponse(
            {
                "image_list"             : [image.url for image in images], 
                "id"                     : investment.id,
                "name"                   : investment.name,
                "grade"                  : investment.grade.name,
                "return_rate"            : investment.return_rate,
                "duration"               : investment.duration,
                "repayment_types"        : investment.repayment_type.name, 
                "current_amount"         : investment.current_amount, 
                "target_amount"          : investment.target_amount,
                "recrutement_rate"       : int(investment.current_amount/investment.target_amount*100), 
                "LTV"                    : round(((investment.target_amount + investment.detail.priority_bond_amount)/investment.detail.evaluation_price)*100, 2), 
                "repayment_day"          : investment.detail.repayment_day, 
                "loan_type"              : investment.detail.loan_type.name, 
                "evaluation_price"       : investment.detail.evaluation_price, 
                "priority_bond_amount"   : investment.detail.priority_bond_amount, 
                "security_surcharge"     : (investment.detail.evaluation_price - investment.detail.priority_bond_amount - investment.target_amount), 
                "bidding_rate"           : investment.detail.bidding_rate, 
                "expected_recovery"      : (investment.detail.evaluation_price * investment.detail.bidding_rate) - investment.detail.priority_bond_amount, 
                "address"                : investment.security.address, 
                "completion_date"        : investment.security.completion_date, 
                "household"              : investment.security.household, 
                "supply_area"            : investment.security.supply_area, 
                "exclusive_private_area" : investment.security.exclusive_private_area, 
                "lease_status"           : investment.security.lease_status, 
                "latitude"               : investment.security.latitude, 
                "longitude"              : investment.security.longitude, 
                "credit_score"           : investment.borrower.credit_score, 
                "income_type"            : investment.borrower.income_type, 
                "income"                 : investment.borrower.income, 
                "card_usage_amount"      : investment.borrower.card_usage_amount, 
                "loan_amount"            : investment.borrower.loan_amount, 
                "is_overdue"             : investment.borrower.is_overdue, 
                "overdue_tax"            : investment.borrower.overdue_tax
            }, status = 200)
