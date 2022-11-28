from blog import models
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from django_filter_drf_camel_case import DjangoFilterBackend
from django_filter_drf_camel_case import OrderingFilter


class PostSerializer(ModelSerializer):
    class Meta:
        model = models.Post
        fields = ("title", "content", "created_at", "follow_up")


class PostFilters(FilterSet):
    created_at = filters.IsoDateTimeFromToRangeFilter()
    sort = OrderingFilter(fields=("created_at", "title", "follow_up__title"))

    class Meta:
        model = models.Post
        fields = {
            "title": {"exact", "contains"},
            "follow_up__title": {"exact"},
        }


class PostViewSet(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilters


class ExplicitPostFilters(FilterSet):
    created_at = filters.IsoDateTimeFromToRangeFilter()
    follow_up_title = filters.CharFilter(field_name="follow_up__title")
    title_contains = filters.CharFilter(field_name="title", lookup_expr="contains")
    sort = OrderingFilter(
        fields={
            "created_at": "created_at",
            "title": "title",
            "follow_up__title": "follow_up_title",
        }
    )

    class Meta:
        model = models.Post
        fields = {
            "title": {"exact"},
        }


class ExplicitPostViewSet(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExplicitPostFilters
