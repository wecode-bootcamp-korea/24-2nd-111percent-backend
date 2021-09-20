import json

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from transactions.models import Transaction, TransactionType, Bank
from investments.models  import Investment
from core.utils          import login_decorator


class InvestTransactionView(View):
    @login_decorator
    def post(self, request, investment_id):
        try:
            data = json.loads(request.body)

            if data["amounts"] <= 0:
                return JsonResponse({"message": "INVALID_INPUT"}, status=400)

            if not Investment.objects.filter(id=investment_id).exists():
                return JsonResponse({"message": "INVALID_INVESTMENT_ID"}, status=404)

            investment = Investment.objects.get(id=investment_id)
            user = request.user
            deposit = user.deposit

            investment_amount = data["amounts"]

            with transaction.atomic():
                Transaction.objects.create(
                    type_id    =TransactionType.Type.INVESTMENT.value,
                    information=investment.name,
                    amounts    =investment_amount,
                    deposit    =deposit,
                    user       =user,
                    investment =investment,
                )

                deposit.balance -= investment_amount
                deposit.save()

                investment.current_amount += investment_amount
                investment.save()

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class DepositTransactionView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            deposit = request.user.deposit

            if data["amounts"] <= 0:
                return JsonResponse({"message": "INVALID_INPUT"}, status=400)

            with transaction.atomic():
                Transaction.objects.create(
                    type_id=TransactionType.Type.DEPOSIT.value,
                    information=Bank.objects.get(
                        id=Bank.DefaultBank.NH_BANK.value
                    ).name,
                    amounts=data["amounts"],
                    deposit=deposit,
                    user=request.user,
                )

                deposit.balance += data["amounts"]
                deposit.save()

            return JsonResponse(
                {"message": "SUCCESS", "deposit_balance": deposit.balance}, status=201
            )

        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
