"""
JA: トピック(カテゴリ木)と、その配下にぶら下がる知識カード(KnowledgeNode)。
    検索セッションはTopicを起点に配下を辿る。KnowledgeNodeはここでは構造
    (所属Topic・生成元・問題文)だけを持ち、間隔反復のスケジュール(SM-2・
    記憶定着フィールド)は apps/reviews/models.py の ReviewSchedule に
    分離してある(reviewsアプリが排他的に読み書きするフィールドを、他
    アプリのモデル定義に同居させないため)。
VI: Topic (cây danh mục) và các thẻ tri thức (KnowledgeNode) thuộc về nó.
    Phiên tìm kiếm bắt đầu từ Topic để duyệt xuống bên dưới. Ở đây
    KnowledgeNode chỉ giữ phần cấu trúc (Topic sở hữu, node gốc, nội dung
    bài toán); lịch ôn tập ngắt quãng (các trường SM-2, độ định) được
    tách sang ReviewSchedule trong apps/reviews/models.py (để các trường
    mà app reviews độc quyền đọc/ghi không nằm chung với model của app khác).
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Topic(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="topics",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        help_text="None の場合はルートトピック",
    )
    # 注意: parent を CASCADE にしているため、親トピックを削除すると
    # 配下の子トピック・KnowledgeNode・関連ログがすべて連鎖削除される。
    # 誤操作対策が必要なら論理削除(archived_at)への変更を検討すること。
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0, help_text="UI上でのブランチ(枝)の表示順序")

    class Meta:
        ordering = ["position", "created_at"]

    def __str__(self):
        return self.name


class KnowledgeNode(BaseModel):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="knowledge_nodes",
    )
    origin_node = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_nodes",
        help_text="間隔復習機能でAIが類題として生成した場合、元になったノード",
    )
    title = models.CharField(max_length=255, help_text="概念の簡潔な要約")
    content = models.TextField(help_text="課題本文 / プレーンテキスト形式の標準解答")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
