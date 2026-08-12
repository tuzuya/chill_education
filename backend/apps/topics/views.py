"""
JA: 認可・入力検証・services呼び出し・シリアライズのみ。業務ロジックは書かない。
VI: Chỉ phân quyền, kiểm tra đầu vào, gọi services, tuần tự hóa. Không viết
    logic nghiệp vụ ở đây.
"""

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.exceptions import ValidationError

from . import services
from .models import KnowledgeNode, Topic
from .serializers import (
    KnowledgeNodeDetailSerializer,
    KnowledgeNodeSummarySerializer,
    TopicSerializer,
)


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # JA: ★所有者絞り込み(必須)
        # VI: ★Lọc theo chủ sở hữu (bắt buộc)
        qs = Topic.objects.filter(user=self.request.user)
        # JA: ?parent=null でルートトピックだけに絞れる(検索セッションの起点選択用)
        # VI: ?parent=null để chỉ lấy Topic gốc (dùng khi chọn điểm bắt đầu phiên tìm kiếm)
        parent = self.request.query_params.get("parent")
        if parent == "null":
            qs = qs.filter(parent__isnull=True)
        return qs.order_by("position", "created_at")

    @action(detail=True, methods=["get"])
    def children(self, request, pk=None):
        """
        JA: 配下を取得する。直下の子Topicと、このTopicに属するKnowledgeNodeを返す。
        VI: Lấy dữ liệu con. Trả về Topic con trực tiếp và KnowledgeNode thuộc Topic này.
        """
        topic = self.get_object()
        child_topics, nodes = services.get_children(topic)
        return Response(
            {
                "topics": TopicSerializer(child_topics, many=True).data,
                "nodes": KnowledgeNodeSummarySerializer(nodes, many=True).data,
            }
        )

    @action(detail=True, methods=["get"])
    def search(self, request, pk=None):
        """
        JA: キーワードで絞り込む。topic配下(自身含む)を再帰的に検索する。
        VI: Thu hẹp bằng từ khóa. Tìm đệ quy trong topic (bao gồm chính nó).
        """
        query = request.query_params.get("q", "").strip()
        if not query:
            raise ValidationError("q is required")

        topic = self.get_object()
        results = services.search_knowledge_nodes(topic, query)
        return Response(KnowledgeNodeSummarySerializer(results, many=True).data)


class KnowledgeNodeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    JA: 課題(KnowledgeNode)の詳細表示のみ。一覧はTopicViewSet側(children/search)
        から取得する想定なので、ここでは list を持たせない。
    VI: Chỉ xem chi tiết KnowledgeNode. Danh sách lấy qua TopicViewSet
        (children/search), nên ở đây không có list.
    """

    serializer_class = KnowledgeNodeDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # JA: ★所有者絞り込み(必須)。Topic経由でuserを辿る
        # VI: ★Lọc theo chủ sở hữu (bắt buộc). Đi qua Topic để lấy user
        return KnowledgeNode.objects.filter(topic__user=self.request.user).select_related("topic")
