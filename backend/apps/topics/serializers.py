"""
JA: Topic・KnowledgeNodeのJSON表現。検索セッション画面向けに必要な項目だけ返す。
    保存処理や業務判断はここに書かない(services.pyの責務)。
VI: Biểu diễn JSON của Topic/KnowledgeNode. Chỉ trả các trường cần cho màn hình
    phiên tìm kiếm. Không viết xử lý lưu hay phán đoán nghiệp vụ ở đây.
"""

from rest_framework import serializers

from .models import KnowledgeNode, Topic


class TopicSerializer(serializers.ModelSerializer):
    # JA: 子Topicがあるかどうか(UI側で開閉アイコンの出し分けに使う)
    # VI: Có Topic con hay không (frontend dùng để hiện/ẩn icon mở rộng)
    has_children = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ["id", "name", "description", "position", "parent", "has_children"]
        read_only_fields = fields

    def get_has_children(self, obj):
        return obj.children.exists()


class KnowledgeNodeSummarySerializer(serializers.ModelSerializer):
    """一覧・検索結果用の軽量表現 / Biểu diễn nhẹ cho danh sách & kết quả tìm kiếm"""

    class Meta:
        model = KnowledgeNode
        fields = ["id", "title", "topic"]
        read_only_fields = fields


class KnowledgeNodeDetailSerializer(serializers.ModelSerializer):
    """課題詳細表示用 / Dùng cho màn hình xem chi tiết bài toán"""

    topic_name = serializers.CharField(source="topic.name", read_only=True)

    class Meta:
        model = KnowledgeNode
        fields = ["id", "title", "content", "topic", "topic_name"]
        read_only_fields = fields
