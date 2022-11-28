import pytest
from django.http import QueryDict
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from django_filter_drf_camel_case.backend import DjangoFilterBackend


class RequestFactory(APIRequestFactory):
    def request(self, **kwargs):
        r = super().request(**kwargs)
        return Request(r)


@pytest.fixture
def request_factory():
    return RequestFactory()


def test_it_converts_camel_case_to_snake_case(request_factory):
    request = request_factory.get("/?testOne=1&testTwo=2&testThree__lt=3&testFour__testFive=45")
    backend = DjangoFilterBackend()
    kwargs = backend.get_filterset_kwargs(request, None, None)
    data = kwargs["data"]
    expected = QueryDict("test_one=1&test_two=2&test_three__lt=3&test_four__test_five=45")

    assert data == expected


def test_it_supports_params_already_in_snake_case(request_factory):
    request = request_factory.get("/?test_one=1&test_two=2")
    backend = DjangoFilterBackend()
    kwargs = backend.get_filterset_kwargs(request, None, None)
    data = kwargs["data"]
    expected = QueryDict("test_one=1&test_two=2")

    assert data == expected
