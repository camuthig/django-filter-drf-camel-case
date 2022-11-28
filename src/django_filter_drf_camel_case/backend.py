import django_filters.rest_framework as filters
from djangorestframework_camel_case.util import underscoreize


class DjangoFilterBackend(filters.DjangoFilterBackend):
    def parse_query_params(self, query_params):
        return underscoreize(query_params)

    def get_filterset_kwargs(self, request, queryset, view):
        return {
            "data": self.parse_query_params(request.query_params),
            "queryset": queryset,
            "request": request,
        }
