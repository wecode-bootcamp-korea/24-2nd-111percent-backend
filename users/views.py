import json
import re
import bcrypt
import jwt

from uuid import uuid4

from django.http import JsonResponse
from django.views import View
from django.db import transaction

from users.models import User
from users.kakao import KakaoAPI
from transactions.models import Bank, Deposit
from my_settings import MY_SECRET_KEY


class SignupView(View):
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)

                if User.objects.filter(email=data["email"]).exists():
                    if not User.objects.get(email=data["email"]).kakao_id:
                        return JsonResponse(
                            {"message": "EMAIL_ALREADY_EXIST"}, status=400
                        )

                REGEX_EMAIL = re.compile(
                    "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                )
                REGEX_PASSWORD = re.compile(
                    "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
                )

                is_email_valid = REGEX_EMAIL.match(data["email"])
                is_password_valid = REGEX_PASSWORD.match(data["password"])

                if not (is_email_valid and is_password_valid):
                    return JsonResponse({"message": "INVALID_INPUT_FORMAT"}, status=400)

                bank_created = Bank.objects.get_or_create(name=data["bank_name"])

                deposit_created = Deposit.objects.create(
                    withdrawal_account=data["account_number"],
                    withdrawal_bank=bank_created[0],
                    deposit_account=str(uuid4().int)[:14],
                    deposit_bank_id=Bank.DefaultBank.NH_BANK.value,
                )

                user, created = User.objects.get_or_create(email=data["email"])

                user.name = data["name"]
                user.phone_number = data["phone_number"]
                user.password = bcrypt.hashpw(
                    data["password"].encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                user.deposit = deposit_created
                user.save()

                return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            token = jwt.encode({"id": user.id}, MY_SECRET_KEY, algorithm="HS256")
            return JsonResponse(
                {"message": "SUCCESS", "token": token, "user_name": user.name},
                status=200,
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class KakaoSigninView(View):
    def post(self, request):
        try:
            access_token = request.headers.get("Authorization", None)

            if not access_token:
                return JsonResponse({"message": "TOKEN_DOES_NOT_EXIST"}, status=400)

            kakao_user = KakaoAPI(access_token).get_kakao_user()
            kakao_account = kakao_user["kakao_account"]

            if "profile" not in kakao_account:
                return JsonResponse({"message": "PROFILE_REQUIRED"}, status=405)

            if "email" not in kakao_account:
                return JsonResponse({"message": "EMAIL_REQUIRED"}, status=405)

            kakao_profile = kakao_account["profile"]

            user, created = User.objects.get_or_create(
                email=kakao_account["email"],
                kakao_id=kakao_user["id"],
            )

            if created:
                user.name = kakao_profile["nickname"]
                user.password = uuid4().hex
                user.save()

            token = jwt.encode({"id": user.id}, MY_SECRET_KEY, algorithm="HS256")

            return JsonResponse(
                {
                    "message": "SUCCESS",
                    "token": token,
                    "user_name": user.name,
                    "user_email": user.email,
                },
                status=200,
            )

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except TimeoutError:
            return JsonResponse({"message": "TIMEOUT_ERROR"}, status=408)
