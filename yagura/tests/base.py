from django.test import Client, TestCase


class ViewTestCase(TestCase):
    """Abstract of view action tests
    """
    fixtures = [
        'initial',
        'unittest_suite',
    ]

    def setUp(self):
        super().setUp()
        self.client = Client()
