from django.views import View
from django.http import JsonResponse

from .models import Investment

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
