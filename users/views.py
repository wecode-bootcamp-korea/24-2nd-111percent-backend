import json
import re 
import bcrypt

from django.http import JsonResponse
from django.views import View

from users.models import User


class SignupView(View):
    def post(self, request):
        try:
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

            User.objects.create(
                name         =data["name"],
                email        =data["email"],
                phone_number =data["phone_number"],
                password     =bcrypt.haswpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                deposit      =data["deposit"]
            )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
