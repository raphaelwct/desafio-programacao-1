from django.test import TestCase
import views
import mock


class ViewsTestCase(TestCase):

    def test_import_data_should_return_message(self):
        request_mock = mock.Mock()
        message_received = views.import_data(request_mock)
        self.assertTrue(instanceof(message_received, 'str'))
        self.assertTrue(len(message_received) > 0)
