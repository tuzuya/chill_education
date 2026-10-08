"""
apps/accounts/tests.py

JA: 新規登録(POST /api/auth/signup/)を検証する。★発表デモでの同時利用向けに
    追加した機能なので、正常系・重複ユーザー名・弱いパスワードの3本を確認する。
VI: Kiểm tra đăng ký mới (POST /api/auth/signup/). ★Tính năng thêm để dùng đồng
    thời khi demo thuyết trình, nên kiểm tra 3 luồng: chính thường, trùng username,
    mật khẩu yếu.
"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase

from apps.common.throttles import LoginRateThrottle, SignupRateThrottle

User = get_user_model()


class SignupTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        resp = self.client.post(
            "/api/auth/signup/",
            {"username": "attendee1", "password": "correct-horse-1"},
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["username"], "attendee1")
        self.assertTrue(User.objects.filter(username="attendee1").exists())

        # JA: 登録直後にログイン状態(セッション)になっていることを確認する。
        # VI: Xác nhận ngay sau đăng ký đã ở trạng thái đăng nhập (session).
        me_resp = self.client.get("/api/auth/me/")
        self.assertEqual(me_resp.status_code, 200)
        self.assertEqual(me_resp.json()["username"], "attendee1")

    def test_signup_rejects_duplicate_username(self):
        User.objects.create_user(username="attendee2", password="correct-horse-1")

        resp = self.client.post(
            "/api/auth/signup/",
            {"username": "attendee2", "password": "another-pass-1"},
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_signup_rejects_weak_password(self):
        resp = self.client.post(
            "/api/auth/signup/",
            {"username": "attendee3", "password": "1234"},
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(User.objects.filter(username="attendee3").exists())


class AuthThrottleTests(TestCase):
    """
    JA: 回帰テスト。ログインに回数制限が無く総当たりできた問題の再発防止。
        回数はテスト用に小さく差し替え、キャッシュは毎回空にする(他テストのカウントを持ち越さない)。
    VI: Test hồi quy. Ngăn tái diễn lỗi đăng nhập không giới hạn số lần (dò mật khẩu được).
        Thay số lần nhỏ cho test, và xóa cache mỗi lần (không mang số đếm từ test khác sang).
    """

    def setUp(self):
        cache.clear()
        User.objects.create_user(username="victim", password="correct-horse-1")

    def _login(self, username, password="wrong-pass-1", **extra):
        return self.client.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            content_type="application/json",
            **extra,
        )

    def test_login_is_throttled_per_username_even_if_ip_changes(self):
        with patch.object(LoginRateThrottle, "THROTTLE_RATES", {"login": "3/min"}):
            for i in range(3):
                resp = self._login("victim", HTTP_X_FORWARDED_FOR=f"10.0.0.{i}")
                self.assertNotEqual(resp.status_code, 429)
            # JA: IP を変えても同じユーザー名なら4回目で止まる。
            # VI: Đổi IP nhưng cùng username thì lần thứ 4 bị chặn.
            resp = self._login("Victim", HTTP_X_FORWARDED_FOR="10.0.0.99")
            self.assertEqual(resp.status_code, 429)

            # JA: 別のユーザー名は巻き添えにならない。
            # VI: Username khác không bị ảnh hưởng.
            self.assertNotEqual(self._login("someone-else").status_code, 429)

    def test_signup_is_throttled(self):
        with patch.object(SignupRateThrottle, "THROTTLE_RATES", {"signup": "2/min"}):
            for i in range(2):
                resp = self.client.post(
                    "/api/auth/signup/",
                    {"username": f"bot{i}", "password": "correct-horse-1"},
                    content_type="application/json",
                )
                self.assertEqual(resp.status_code, 201)
                self.client.logout()
            resp = self.client.post(
                "/api/auth/signup/",
                {"username": "bot9", "password": "correct-horse-1"},
                content_type="application/json",
            )
            self.assertEqual(resp.status_code, 429)
