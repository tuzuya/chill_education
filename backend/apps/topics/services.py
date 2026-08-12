"""
JA: 検索セッションの業務ロジック。カテゴリ木の走査とキーワード検索を行う。
    HTTP・requestには依存しない。
VI: Logic nghiệp vụ của phiên tìm kiếm. Duyệt cây danh mục và tìm theo từ khóa.
    Không phụ thuộc HTTP/request.
"""

from django.db.models import Q

from .models import KnowledgeNode, Topic


def get_children(topic: Topic):
    """
    JA: 指定Topicの直下(子Topic・このTopicに属するKnowledgeNode)だけを返す。
        ドリルダウンUI用。AI生成の使い捨て類題(origin_nodeを持つもの)は含めない。
    VI: Trả về trực tiếp con của Topic (Topic con, KnowledgeNode thuộc Topic này).
        Dùng cho UI duyệt sâu dần. Không bao gồm node類題 AI sinh dùng một lần.
    """
    child_topics = topic.children.all().order_by("position", "created_at")
    nodes = topic.knowledge_nodes.filter(origin_node__isnull=True).order_by("-created_at")
    return child_topics, nodes


def get_descendant_topic_ids(topic: Topic) -> list:
    """
    JA: topic自身を含む、配下すべてのTopic idを幅優先で集める。
        django-mptt等は使わず素朴なループで実装している(規模が大きくなったら見直す)。
    VI: Gom tất cả id Topic (bao gồm topic hiện tại) ở bên dưới, duyệt theo BFS.
        Không dùng django-mptt, chỉ vòng lặp đơn giản (quy mô lớn hơn thì xem lại).
    """
    ids = [topic.id]
    frontier = [topic.id]
    while frontier:
        children = list(Topic.objects.filter(parent_id__in=frontier).values_list("id", flat=True))
        if not children:
            break
        ids.extend(children)
        frontier = children
    return ids


def search_knowledge_nodes(topic: Topic, query: str):
    """
    JA: topic配下(自身含む)を再帰的に対象に、title/contentの部分一致で検索する。
        AI生成の使い捨て類題(origin_nodeがある)は検索対象に含めない。
    VI: Tìm đệ quy trong topic (bao gồm chính nó), khớp một phần title/content.
        Không bao gồm node類題 AI sinh dùng một lần (có origin_node).
    """
    topic_ids = get_descendant_topic_ids(topic)
    return (
        KnowledgeNode.objects.filter(topic_id__in=topic_ids, origin_node__isnull=True)
        .filter(Q(title__icontains=query) | Q(content__icontains=query))
        .select_related("topic")
        .order_by("-created_at")
    )
