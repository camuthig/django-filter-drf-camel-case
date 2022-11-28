import re

from django_filters import filters
from djangorestframework_camel_case.util import underscore_to_camel

from django_filter_drf_camel_case import regex


class OrderingFilter(filters.OrderingFilter):
    """
    An extension of the standard ordering filter that ensures the API keys are all camel cased.

    With this class, the following class instantiations create the same result:

    * `django_filters.rest_framework.filters.OrderingFilter(fields=(("my_field", "myField"))`
    * `OrderingFilter(fields=("my_field"))`
    """

    @classmethod
    def normalize_fields(cls, fields):
        normalized_fields = super().normalize_fields(fields)

        for field, param in normalized_fields.items():
            normalized_fields[field] = re.sub(regex.dunderscore_camelize_re, underscore_to_camel, param)

        return normalized_fields
