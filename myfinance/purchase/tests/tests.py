from django.test import TestCase, Client
from purchase import views
import mock


class PurchaseImporterFormViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    @mock.patch.object(views, 'import_data')
    def test_if_purchase_importer_form_calls_import_data_in_case_of_post_request(self, import_data_mock):
        self.client.post('/purchase/pdi/')
        self.assertTrue(import_data_mock.called)

    @mock.patch.object(views, 'import_data')
    def test_purchase_importer_form_should_not_calls_import_data_in_case_of_get_request(self, import_data_mock):
        self.client.get('/purchase/pdi/')
        self.assertFalse(import_data_mock.called)


class ImportDataViewTestCase(TestCase):

    def test_import_data_should_return_message(self):
        request_mock = mock.Mock()
        message_received = views.import_data(request_mock)
        self.assertIsInstance(message_received, str)
        self.assertGreater(len(message_received), 0)

    def test_import_data_should_parse_all_the_file_data(self):
        request_mock = mock.Mock()
        message_received = views.import_data(request_mock)
        self.assertIsInstance(message_received, str)
        self.assertGreater(len(message_received), 0)
