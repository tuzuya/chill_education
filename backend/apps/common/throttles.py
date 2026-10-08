"""
apps/common/throttles.py

JA: 回数制限(レート制限)の共通クラス。総当たり攻撃と AI API の料金浪費を防ぐ。
    数える単位(キー)は守る対象ごとに変える。IP は X-Forwarded-For で偽装できるため、
    偽装できない単位で数えられるものはそちらを使う。
    - ログイン: 入力されたユーザー名ごと(IP を変えても同じアカウントは狙えない)
    - 新規登録: IP ごと(ユーザーが未確定なので IP しか無い。抑止目的)
    - AI 呼び出し: ログインユーザーごと
    回数は settings の DEFAULT_THROTTLE_RATES で決める。
VI: Lớp giới hạn tần suất (rate limit) dùng chung. Chống dò mật khẩu và lãng phí phí API AI.
    Đơn vị đếm (key) thay đổi theo đối tượng cần bảo vệ. IP có thể giả mạo qua
    X-Forwarded-For, nên chỗ nào đếm được bằng đơn vị không giả mạo được thì dùng đơn vị đó.
    - Đăng nhập: theo username được nhập (đổi IP cũng không nhắm được cùng tài khoản)
    - Đăng ký: theo IP (chưa có user nên chỉ có IP; mục đích răn đe)
    - Gọi AI: theo user đang đăng nhập
    Số lần quy định ở DEFAULT_THROTTLE_RATES trong settings.
"""

from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        username = str(request.data.get("username", "")).strip().lower()
        if not username:
            # JA: ユーザー名が無ければ検証で 400 になるので数えない。
            # VI: Không có username thì sẽ bị 400 ở bước kiểm tra nên không đếm.
            return None
        return self.cache_format % {"scope": self.scope, "ident": username}


class SignupRateThrottle(SimpleRateThrottle):
    scope = "signup"

    def get_cache_key(self, request, view):
        return self.cache_format % {"scope": self.scope, "ident": self.get_ident(request)}


class AIRateThrottle(UserRateThrottle):
    scope = "ai"
