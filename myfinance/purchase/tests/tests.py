from django.test import TestCase, Client
from purchase import views
import mock


class ViewsTestCase(TestCase):

    def test_import_data_should_return_message(self):
        request_mock = mock.Mock()
        message_received = views.import_data(request_mock)
        self.assertIsInstance(message_received, str)
        self.assertGreater(len(message_received), 0)

    @mock.patch.object(views, 'import_data')
    def test_if_purchase_importer_form_calls_import_data_in_case_of_post_request(self, import_data_mock):
        request_mock = mock.Mock()
        request_mock.method = 'POST'
        views.purchase_importer_form(request_mock)
        self.assertTrue(import_data_mock.called)

    @mock.patch.object(views, 'import_data')
    def test_purchase_importer_form_should_not_calls_import_data_in_case_of_get_request(self, import_data_mock):
        request_mock = mock.Mock()
        request_mock.method = 'GET'
        views.purchase_importer_form(request_mock)
        self.assertFalse(import_data_mock.called)
