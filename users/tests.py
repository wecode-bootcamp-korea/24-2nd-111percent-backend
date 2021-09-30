from django.test import TestCase, Client
from unittest.mock import patch, MagicMock


class KakaoSocialLoginTest(TestCase):
    @patch("users.kakao.requests")
    def test_kakao_signin_post_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                return {
                    "id": 123456789,
                    "kakao_account": {
                        "profile": {
                            "nickname": "최파란별멋쟁이",
                        },
                        "email": "cprb@naver.com",
                    },
                }

        header = {"HTTP_Authorization": "Bearer test_kakao_access_token"}
        mocked_requests.get = MagicMock(return_value=MockedResponse(200))
        response = client.post(
            "/users/signin/kakao", content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "SUCCESS",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6M30.-mxXIixRm4tiNsBan9H6dYe3JsVOi2gbWxMSycVoGpc",
                "user_name": "최파란별멋쟁이",
                "user_email": "cprb@naver.com",
            },
        )

    def test_kakao_signin_post_token_does_not_exist(self):
        client = Client()

        response = client.post("/users/signin/kakao", content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "TOKEN_DOES_NOT_EXIST"})

    @patch("users.kakao.requests")
    def test_kakao_signin_email_required(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                return {
                    "id": 123456789,
                    "kakao_account": {
                        "profile": {
                            "nickname": "최파란별멋쟁이",
                        }
                    },
                }

        header = {"HTTP_Authorization": "Bearer test_kakao_access_token"}
        mocked_requests.get = MagicMock(return_value=MockedResponse(200))
        response = client.post(
            "/users/signin/kakao", content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"message": "EMAIL_REQUIRED"})

    @patch("users.kakao.requests")
    def test_kakao_signin_profile_required(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                return {
                    "id": 123456789,
                    "kakao_account": {
                        "email": "cprb@naver.com",
                    },
                }

        header = {"HTTP_Authorization": "Bearer test_kakao_access_token"}
        mocked_requests.get = MagicMock(return_value=MockedResponse(200))
        response = client.post(
            "/users/signin/kakao", content_type="application/json", **header
        )

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"message": "PROFILE_REQUIRED"})
