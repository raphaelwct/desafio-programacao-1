from django.test import TestCase, Client
from purchase import views
import mock
from StringIO import StringIO


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
        fake_purchase_file = StringIO('header test\ntest')
        request_mock = mock.Mock()
        request_mock.FILES = {'purchase_file': fake_purchase_file}
        message_received = views.import_data(request_mock)
        self.assertIsInstance(message_received, str)
        self.assertGreater(len(message_received), 0)

    @mock.patch.object(views, 'parse_purchase_file_data')
    def test_import_data_should_call_parse_purchase_file_data(self, parse_purchase_file_data_mock):
        request_mock = mock.Mock()
        request_mock.FILES = {'purchase_file': mock.Mock()}
        views.import_data(request_mock)
        self.assertTrue(parse_purchase_file_data_mock.called)

    @mock.patch.object(views, 'parse_purchase_file_data')
    @mock.patch.object(views, 'save_purchase_data')
    def test_import_data_should_call_save_purchase_data(self, save_purchase_data_mock,
            parse_purchase_file_data_mock):
        request_mock = mock.Mock()
        request_mock.FILES = {'purchase_file': mock.Mock()}
        parse_purchase_file_data_mock.return_value = iter([1, 2, 3])
        views.import_data(request_mock)
        excepted_calls = [mock.call(1), mock.call(2), mock.call(3)]
        save_purchase_data_mock.assert_has_calls(excepted_calls, any_order=True)


class ParsePurchaseFileDataViewTestCase(TestCase):

    @mock.patch.object(views, 'parse_purchase_file_data')
    def test_parse_purchase_file_data_should_transform_each_line_in_a_tuple(self,
            parse_purchase_file_data_mock):
        fake_purchase_file = StringIO()
        fake_purchase_file.write("""purchaser name  item description    item price  purchase count
        merchant   address merchant name
        Joao Silva  R$10 off R$20 of food   10.0    2   987 Fake St Bobs Pizza""")
        expected_parsed_line = ('Joao Silva', 'R$10 off', 'R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        for parsed_line in views.parse_purchase_file_data(fake_purchase_file):
            self.assertEquals(parsed_line, expected_parsed_line)
        self.assertTrue(parse_purchase_file_data_mock.called)


class SavePurchaseDataViewTestCase(TestCase):

    @mock.patch.object(views, 'normalize_data')
    def test_save_purchase_data_must_call_normalize_data_method(self, normalize_data_mock):
        views.save_purchase_data(mock.Mock())
        self.assertTrue(normalize_data_mock.called)
