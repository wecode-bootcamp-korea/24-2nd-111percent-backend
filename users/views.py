import json
import re 
import bcrypt

from uuid import uuid4

from django.http  import JsonResponse
from django.views import View
from django.db import transaction

from users.models import User
from transactions.models import Bank, Deposit


class SignupView(View):
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                if User.objects.filter(email=data["email"]).exists():
                    return JsonResponse({"message": "EMAIL Already Exist"}, status=400)

                REGEX_EMAIL    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
                REGEX_PASSWORD = re.compile(
                    "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
                )

                is_email_valid    = REGEX_EMAIL.match(data["email"])
                is_password_valid = REGEX_PASSWORD.match(data["password"])

                if not (is_email_valid and is_password_valid):
                    return JsonResponse({"message": "INVALID INPUT FORMAT"}, status=400)

                bank_created = Bank.objects.get_or_create(name=data["bank_name"])

                deposit_created = Deposit.objects.create(
                    withdrawal_account = data["account_number"],
                    withdrawal_bank    = bank_created[0],
                    deposit_account    = str(uuid4().int)[:14],
                    deposit_bank_id    = Bank.DefaultBank.NH_BANK.value 
                )

                User.objects.create(
                    name         =data["name"],
                    email        =data["email"],
                    phone_number =data["phone_number"],
                    password     =bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                    deposit      =deposit_created
                )
                return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
