import pathlib

from django.db import models
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from drf_spectacular.validation import validate_schema
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from django_filter_drf_camel_case import DjangoFilterBackend

TEST_DIR = pathlib.Path(__file__).parent.absolute()


def generate_schema(route, viewset=None, view=None, view_function=None, patterns=None):
    """
    The generate_schema test function taken from drf_spectacular's tests.
    """
    from django.urls import path
    from drf_spectacular.generators import SchemaGenerator
    from rest_framework import routers
    from rest_framework.viewsets import ViewSetMixin

    if viewset:
        assert issubclass(viewset, ViewSetMixin)
        router = routers.SimpleRouter()
        router.register(route, viewset, basename=route)
        patterns = router.urls
    elif view:
        patterns = [path(route, view.as_view())]
    elif view_function:
        patterns = [path(route, view_function)]
    else:
        assert route is None and isinstance(patterns, list)

    generator = SchemaGenerator(patterns=patterns)
    schema = generator.get_schema(request=None, public=True)
    validate_schema(schema)  # make sure generated schemas are always valid
    return schema


class SampleModel(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, help_text="created_at")
    self_rel = models.ForeignKey("SampleModel", on_delete=models.SET_NULL)


class SampleFilterSet(FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = SampleModel
        fields = {
            "title": ("exact",),
            "self_rel__title": ("exact",),
        }


class SampleSerializer(ModelSerializer):
    class Meta:
        model = SampleModel
        fields = ("title", "created_at", "self_rel")


class SampleViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = SampleFilterSet
    serializer_class = SampleSerializer
    queryset = SampleModel.objects.all()


def test_django_filter_extension_camel_cases():
    schema = generate_schema("/x", SampleViewSet)

    expected_names = (
        "title",
        "selfRel__title",
        "createdAtBefore",
        "createdAtAfter",
    )

    parameters = schema["paths"]["/x/"]["get"]["parameters"]
    names = {p["name"] for p in parameters}
    assert not names.difference(expected_names)
