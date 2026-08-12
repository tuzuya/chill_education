"""
JA: 検索セッション(topics)のルーティング登録。
VI: Đăng ký routing cho phiên tìm kiếm (topics).
"""

from rest_framework.routers import DefaultRouter

from .views import KnowledgeNodeViewSet, TopicViewSet

router = DefaultRouter()
router.register("topics", TopicViewSet, basename="topic")
router.register("knowledge-nodes", KnowledgeNodeViewSet, basename="knowledge-node")
urlpatterns = router.urls

# config/urls.py に以下を1行追加すること:
#   path("api/", include("apps.topics.urls"))