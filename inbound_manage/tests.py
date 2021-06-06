from django.test import TestCase, client
from inbound_manage.models import Inbound


class InboundTest(TestCase):

    @staticmethod
    def test_query():
        kwargs = {'material_code': 'JP2021'}
        print(kwargs)
        count = Inbound.objects.filter(**kwargs).count()
        print(count)
