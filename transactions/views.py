import json

from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.db.models import Sum, Avg

from transactions.models import (
    Repayment,
    RepaymentState,
    Transaction,
    TransactionType,
    Bank,
    Portfolio,
    InvestmentState,
)
from investments.models import Investment
from core.utils import login_decorator


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

            if investment_amount > deposit.balance:
                return JsonResponse({"message": "OUT_OF_RANGE"}, status=400)

            with transaction.atomic():
                Transaction.objects.create(
                    type_id=TransactionType.Type.INVESTMENT.value,
                    information=investment.name,
                    amounts=investment_amount,
                    deposit=deposit,
                    user=user,
                    investment=investment,
                )

                portfolio, created = Portfolio.objects.get_or_create(
                    user=user,
                    investment=investment,
                    investment_state_id=InvestmentState.State.INVESTING.value,
                    repayment_state_id=RepaymentState.State.NORMAL.value,
                )

                deposit.balance -= investment_amount
                deposit.save()

                investment.current_amount += investment_amount
                investment.save()

                portfolio.amounts += investment_amount
                portfolio.save()

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


class PortfolioView(View):
    @login_decorator
    def get(self, request):
        deposit = request.user.deposit
        portfolios = Portfolio.objects.filter(user=request.user)
        repayments = Repayment.objects.filter(user=request.user)
        portfolio_investings = portfolios.filter(
            investment_state_id=InvestmentState.State.INVESTING.value
        )

        results = {
            "deposit_information": {
                "withdrawal_account": f"{deposit.withdrawal_bank.name}{deposit.withdrawal_account}",
                "deposit_account": f"{deposit.deposit_bank.name}{deposit.deposit_account}",
                "deposit_balance": deposit.balance,
                "gross_investment_limit": 30000000 - portfolios.aggregate(assets=Sum("amounts"))["assets"],
                "real_estate_investment_limit": 10000000 - portfolios.aggregate(assets=Sum("amounts"))["assets"]
            },
            "investment_general_infomation": {
                "rate_of_return": portfolios.aggregate(
                    rate_of_return=Avg("investment__return_rate")
                )["rate_of_return"],
                "assets": portfolios.aggregate(assets=Sum("amounts"))["assets"]
                + deposit.balance,
                "cumulative_profit": repayments.aggregate(
                    cumulative_profit=Sum("interest")
                )["cumulative_profit"],
            },
            "investment_current_condition": {
                "investing_amount": portfolio_investings.aggregate(
                    amounts=Sum("amounts")
                )["amounts"],
                "invest_completed_amount": portfolios.filter(
                    investment_state_id=InvestmentState.State.COMPLETE.value
                ).aggregate(amounts=Sum("amounts"))["amounts"],
                "loss_amount": portfolios.filter(
                    investment_state_id=InvestmentState.State.LOSS.value
                ).aggregate(amounts=Sum("amounts"))["amounts"],
                "investing_normal_amount": portfolio_investings.filter(
                    repayment_state_id=RepaymentState.State.NORMAL.value
                ).aggregate(amounts=Sum("amounts"))["amounts"],
                "investing_delay_amount": portfolio_investings.filter(
                    repayment_state_id=RepaymentState.State.DELAY.value
                ).aggregate(amounts=Sum("amounts"))["amounts"],
                "investing_overdue_amount": portfolio_investings.filter(
                    repayment_state_id=RepaymentState.State.OVERDUE.value
                ).aggregate(amounts=Sum("amounts"))["amounts"],
            },
            "portfolio_current_condition": {
                "grade": {
                    "A": portfolios.filter(investment__grade__name__contains="A").aggregate(amounts=Sum("amounts"))["amounts"],
                    "B": portfolios.filter(investment__grade__name__contains="B").aggregate(amounts=Sum("amounts"))["amounts"],
                    "C": portfolios.filter(investment__grade__name__contains="C").aggregate(amounts=Sum("amounts"))["amounts"],
                    "D": portfolios.filter(investment__grade__name__contains="D").aggregate(amounts=Sum("amounts"))["amounts"],
                },
                "return_rate": {
                    "8_under": portfolios.filter(investment__return_rate__lt=8).aggregate(amounts=Sum("amounts"))["amounts"],
                    "8_over_or_equal": portfolios.filter(investment__return_rate__gte=8, investment__return_rate__lt=10).aggregate(amounts=Sum("amounts"))["amounts"],
                    "10_over_or_equal": portfolios.filter(investment__return_rate__gte=10, investment__return_rate__lt=12).aggregate(amounts=Sum("amounts"))["amounts"],
                    "12_over_or_equal": portfolios.filter(investment__return_rate__gte=12).aggregate(amounts=Sum("amounts"))["amounts"],
                }
            }
        }

        return JsonResponse({"results": results}, status=200)
