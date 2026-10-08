"""
config/settings/production.py

JA: 本番用の設定のスケルトン。DB は環境変数から PostgreSQL を組み立てられる形にし、
    秘密情報は必ず環境変数で注入する。今はまだデプロイしないので最小限。
    「SQLite から PostgreSQL へ後で切替できる」という要件の受け皿がここ。
VI: Bộ khung cấu hình production. DB dựng PostgreSQL từ biến môi trường, secret luôn
    tiêm qua biến môi trường. Hiện chưa deploy nên giữ tối thiểu. Đây là nơi hiện thực
    yêu cầu "sau này chuyển từ SQLite sang PostgreSQL".

【設計変更 2026-10-09】
JA: DJANGO_SECRET_KEY が無いと起動時にエラーで止めるようにした。以前は base の公開済み
    既定値で黙って起動してしまい、設定漏れに気づけず Cookie を偽造されうる状態だった。
    あわせて HSTS を有効化した。
【Thay đổi thiết kế 2026-10-09】
VI: Thiếu DJANGO_SECRET_KEY thì dừng ngay khi khởi động. Trước đây app lặng lẽ chạy với
    giá trị mặc định đã công khai trong base, không phát hiện được thiếu cấu hình và có thể
    bị giả mạo Cookie. Đồng thời bật HSTS.
"""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import BASE_DIR, MIDDLEWARE

DEBUG = False

# JA: 本番では SECRET_KEY を必須にする（未設定なら起動させない）。
# VI: Ở production bắt buộc SECRET_KEY (chưa đặt thì không cho khởi động).
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production")

# JA: 本番ホストは環境変数から。カンマ区切りで複数指定可。
# VI: Host production lấy từ biến môi trường, phân tách bằng dấu phẩy.
ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h]

# JA: PostgreSQL への切替口。環境変数が揃っていれば PostgreSQL を使う。
# VI: Điểm chuyển sang PostgreSQL. Nếu đủ biến môi trường thì dùng PostgreSQL.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", ""),
        "USER": os.environ.get("POSTGRES_USER", ""),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# JA: 本番は Cookie を HTTPS 限定にするなどの強化をここで行う（担当が後で拡張）。
# VI: Ở production tăng cường bảo mật Cookie chỉ qua HTTPS... (người phụ trách mở rộng sau).
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# JA: フロントとバックエンドが別ドメイン(別サーバー)構成のため、Cookieをクロスオリジンで
#     やり取りできるようにする。SameSite=None は Secure(HTTPS)とセットでのみブラウザに
#     受理されるため、上の SESSION_COOKIE_SECURE / CSRF_COOKIE_SECURE = True と対になる。
# VI: Frontend và backend nằm ở domain (server) khác nhau, nên cần cho phép Cookie đi
#     kèm request cross-origin. SameSite=None chỉ được trình duyệt chấp nhận khi đi kèm
#     Secure (HTTPS), nên luôn đi cùng SESSION_COOKIE_SECURE / CSRF_COOKIE_SECURE = True ở trên.
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

# JA: Render 等のPaaSはTLSをリバースプロキシ側で終端し、Djangoにはhttpで転送してくる。
#     この指定が無いと Django は自分がHTTP応答中だと誤認し、Secure Cookieやリダイレクトの
#     判定を誤る。
# VI: Các PaaS như Render kết thúc TLS ở reverse proxy rồi chuyển tiếp bằng http tới Django.
#     Thiếu dòng này thì Django hiểu nhầm đang phản hồi qua HTTP, làm sai phán đoán về
#     Secure Cookie/redirect.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# JA: HSTS。ブラウザに「以後このホストは HTTPS でしか開かない」と覚えさせる。
#     onrender.com は共有ドメインなので includeSubDomains / preload は付けない。
#     HTTP→HTTPS のリダイレクトは Render が入口で行うため SECURE_SSL_REDIRECT は使わない
#     (内部の HTTP ヘルスチェックまでリダイレクトされて失敗するため)。
# VI: HSTS. Bảo trình duyệt "từ nay host này chỉ mở bằng HTTPS".
#     onrender.com là domain dùng chung nên không bật includeSubDomains / preload.
#     Render đã redirect HTTP→HTTPS ở cổng vào nên không dùng SECURE_SSL_REDIRECT
#     (nếu bật thì cả health check HTTP nội bộ cũng bị redirect và thất bại).
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SILENCED_SYSTEM_CHECKS = ["security.W005", "security.W008", "security.W021"]

# JA: フロントのオリジンを環境変数で指定する(カンマ区切りで複数可)。例:
#     CORS_ALLOWED_ORIGINS=https://chill-education.vercel.app
#     CSRF_TRUSTED_ORIGINS=https://chill-education.vercel.app
#     local.py にはあるがここには無く、別ドメイン構成でクロスオリジンのCookie付き
#     リクエストが全てブロックされていた(このコメントを書いている時点で発見・修正)。
# VI: Chỉ định origin của frontend qua biến môi trường (phân tách bằng dấu phẩy nếu
#     nhiều origin). local.py có nhưng ở đây trước đó không có, khiến mọi request kèm
#     Cookie cross-origin bị chặn hết khi frontend/backend khác domain (phát hiện và
#     sửa ngay lúc viết comment này).
CORS_ALLOWED_ORIGINS = [o for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o]

AI_PROVIDER = os.environ.get("AI_PROVIDER", "gemini")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# JA: 分岐推定の方式(ai / bigram / off)。詳細は local.py のコメントを参照。
# VI: Phương thức đoán nhánh (ai / bigram / off). Xem chú thích ở local.py.
CHAT_BRANCHING_STRATEGY = os.environ.get("CHAT_BRANCHING_STRATEGY", "ai")

# JA: gunicorn は静的ファイルを自分で配信しないため、WhiteNoiseに任せる。
#     collectstatic の出力先が STATIC_ROOT。manifest化+圧縮で配信する。
# VI: gunicorn không tự phục vụ static file, nên giao cho WhiteNoise.
#     STATIC_ROOT là nơi collectstatic xuất ra. Phục vụ dạng manifest + nén.
MIDDLEWARE = MIDDLEWARE.copy()
MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
