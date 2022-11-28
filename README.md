# Django-Filter DRF Camel Case Helpers

![Tests](https://github.com/camuthig/django-filter-drf-camel-case/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/camuthig/django-filter-drf-camel-case/branch/main/graph/badge.svg?token=GAGIIZXC95)](https://codecov.io/gh/camuthig/django-filter-drf-camel-case)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Source Code](https://img.shields.io/badge/Source-code-blue)](https://github.com/camuthig/django-filter-drf-camel-case)

A collection of utility classes that make using camel cased query parameters easier with [Django REST
Framework](https://www.django-rest-framework.org/) and [django-filter](https://django-filter.readthedocs.io/en/latest/index.html).
Filter set query parameters can be written using conventional snake cased naming in Python code, but will be treated as
camel case in the API. Additionally, schemas generated using [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html)
will use the correct camel case notation.

# Usage

To get the full benefit of this package, just swap out the normal `DjangoFilterBackend` and `OrderingFilter` classes
provided by the `django_filter` package with those implemented in `django_filter_drf_camel_case`.

```python
from django.db import models
from django_filters.rest_framework import filters
from django_filters.rest_framework import filterset
from rest_framework.viewsets import ModelViewSet

from django_filter_drf_camel_case import OrderingFilter
from django_filter_drf_camel_case import DjangoFilterBackend

class Post(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_add_now=True)
    follow_up = models.ForeignKey("Post", null=True, on_delete=models.SET_NULL)


class PostFilters(filterset.FilterSet):
    created_at = filters.IsoDateTimeFromToRangeFilter()
    sort = OrderingFilter(fields=("created_at", "title", "follow_up__title"))

    class Meta:
        model = Post
        fields = {
            "title": {"exact", "contains"},
            "follow_up__title": {"exact"},
        }

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilters
```

The supported query parameters will be:
* `title`
* `createdAt`
* `createdAt__lt`
* `author__fullName`

The sort keys are:
* `createdAt`/`-createdAt`
* `title`/`-title`
* `followUp__title`/`-followUp__title`

# Underscore vs Dunderscore

To avoid ambiguous query parameters based on lookup expressions, these utilities will respect the  default use of the
dunderscore (`__`) pattern by django-filter to separate fields from lookup expressions and relationships.

If you want to avoid this dunderscore behavior, then the recommendation is to use explicit keys, using underscores
instead of dunderscores where you want. A possible alternative filterset would be

```python
from django.db import models
from django_filters.rest_framework import filters
from django_filters.rest_framework import filterset
from django_filter_drf_camel_case import OrderingFilter

class Post(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_add_now=True)
    follow_up = models.ForeignKey("Post", null=True, on_delete=models.SET_NULL)

class PostFilters(filterset.FilterSet):
    created_at = filters.IsoDateTimeFromToRangeFilter()
    follow_up_title = filters.CharFilter(field_name="follow_up__title")
    sort = OrderingFilter(fields={
        "created_at": "createdAt",
        "title": "title",
        "follow_up__title": "followUpTitle",
    })

    class Meta:
        model = Post
        fields = ("title",)
```

Resulting in the query parameters:
* `title`
* `createdAt`
* `createdAtLt`
* `followUpTitle`

The sort keys are:
* `createdAt`/`-createdAt`
* `title`/`-title`
* `followUpTitle`/`-followUpTitle`
