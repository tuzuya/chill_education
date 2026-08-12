"""
JA: Django Adminへの登録。動作確認・手動でのデータ投入用。
    業務ロジックはここに書かない(services.pyの責務)。
VI: Đăng ký vào Django Admin. Dùng để kiểm tra hoạt động và nhập dữ liệu thủ công.
    Không viết logic nghiệp vụ ở đây (đó là trách nhiệm của services.py).
"""

from django.contrib import admin

from .models import ReviewLog, ReviewSchedule


@admin.register(ReviewSchedule)
class ReviewScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "node",
        "interval_days",
        "easiness_factor",
        "repetitions",
        "next_review_at",
        "learned_count",
    ]
    list_filter = ["node__topic"]
    search_fields = ["node__title"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["next_review_at"]


@admin.register(ReviewLog)
class ReviewLogAdmin(admin.ModelAdmin):
    list_display = ["attempt", "performance_rating", "response_time_seconds", "created_at"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]