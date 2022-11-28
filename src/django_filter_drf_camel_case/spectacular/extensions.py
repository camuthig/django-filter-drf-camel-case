import re

from djangorestframework_camel_case.util import underscore_to_camel
from drf_spectacular.contrib import django_filters

from django_filter_drf_camel_case import regex


class DjangoFilterExtension(django_filters.DjangoFilterExtension):
    target_class = "django_filter_drf_camel_case.backend.DjangoFilterBackend"

    def resolve_filter_field(self, auto_schema, model, filterset_class, field_name, filter_field):
        parameters = super().resolve_filter_field(auto_schema, model, filterset_class, field_name, filter_field)

        for parameter in parameters:
            original_name = parameter["name"]
            parameter["name"] = re.sub(regex.dunderscore_camelize_re, underscore_to_camel, original_name)

        return parameters
