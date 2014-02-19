from django.test import TestCase, Client
from purchase import views, models
import mock
from StringIO import StringIO
from django import shortcuts as django_shortcuts


class PurchaseImporterFormViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    @mock.patch.object(views, 'import_data')
    def test_if_purchase_importer_form_calls_import_data_in_case_of_post_request(self, import_data_mock):
        self.client.post('/purchase/pdi/')
        self.assertTrue(import_data_mock.called)

    @mock.patch.object(django_shortcuts, 'render')
    @mock.patch.object(views, 'import_data')
    def test_purchase_importer_form_must_render_the_template_with_import_feedback_and_the_purchase_total_messages_in_case_of_post_request(self,
            import_data_mock, render_mock):
        fake_import_data_messages = {'import_feedback': 'Foo', 'purchase_total': 'Bar'}
        import_data_mock.return_value = fake_import_data_messages
        self.client.post('/purchase/pdi/')
        import ipdb;ipdb.set_trace();
        self.assertTrue(import_data_mock.called)
        render_mock.assert_called_with(
            'purchase_importer_form.html',
            fake_import_data_messages,
            request=self.client.request,
        )

    @mock.patch.object(views, 'import_data')
    def test_purchase_importer_form_should_not_calls_import_data_in_case_of_get_request(self, import_data_mock):
        self.client.get('/purchase/pdi/')
        self.assertFalse(import_data_mock.called)


class ImportDataViewTestCase(TestCase):

    @mock.patch.object(views, 'parse_purchase_file_data')
    @mock.patch.object(models, 'Purchase')
    @mock.patch.object(views, 'normalize_data')
    def test_import_data_should_return_a_save_feedback_message_and_the_purchase_total(self,
            normalize_data, purchase_model_mock, parse_purchase_file_data_mock):
        fake_parsed_line = iter([('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St',
                'Bobs Pizza')])
        request_mock = mock.Mock()
        request_mock.FILES = {'purchase_file': mock.Mock()}
        parse_purchase_file_data_mock.return_value = fake_parsed_line
        messages = views.import_data(request_mock)
        self.assertIn('import_feedback', messages)
        self.assertIn('purchase_total', messages)
        self.assertGreater(len(messages['import_feedback']), 0)
        self.assertGreater(len(messages['purchase_total']), 0)

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
        file_line1 = ('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        file_line2 = ('Homer', 'R$50 off R$ 20 of beer', '5.0', '4', '111 Fake St', 'Beer Taste')
        fake_parsed_line = iter([file_line1, file_line2])
        parse_purchase_file_data_mock.return_value = fake_parsed_line
        views.import_data(request_mock)
        excepted_calls = [mock.call(file_line1), mock.call(file_line2)]
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

    @mock.patch.object(models, 'Purchase')
    @mock.patch.object(views, 'normalize_data')
    def test_save_purchase_data_must_call_normalize_data_method(self, normalize_data_mock,
            purchase_model_mock):
        views.save_purchase_data(mock.Mock())
        self.assertTrue(normalize_data_mock.called)

    @mock.patch.object(models, 'Purchase')
    @mock.patch.object(views, 'normalize_data')
    def test_save_purchase_data_should_save_all_the_normalized_data_in_a_model_that_represents_a_purchase(self,
            normalize_data_mock, purchase_model_mock):
        purchaser_mock = mock.Mock()
        item_mock = mock.Mock()
        merchant_mock = mock.Mock()
        normalize_data_mock.return_value = {
            'purchaser': purchaser_mock,
            'item': item_mock,
            'merchant': merchant_mock
        }
        views.save_purchase_data(mock.Mock())
        purchase_model_mock.assert_called_with(purchaser=purchaser_mock, item=item_mock,
                merchant=merchant_mock)


class NormalizaDataViewTestCase(TestCase):

    def test_normalize_data_must_return_instances_of_purchase_models(self):
        fake_parsed_line = ('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        normalized_data = views.normalize_data(fake_parsed_line)
        self.assertIn('purchaser', normalized_data)
        self.assertIn('item', normalized_data)
        self.assertIn('merchant', normalized_data)
        self.assertIsInstance(normalized_data['purchaser'], models.Purchaser)
        self.assertIsInstance(normalized_data['item'], models.Item)
        self.assertIsInstance(normalized_data['merchant'], models.Merchant)

    def test_normalize_data_must_convert_the_data_lines_in_data_models(self):
        fake_parsed_line = ('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        normalized_data = views.normalize_data(fake_parsed_line)

        purchaser = normalized_data['purchaser']
        item = normalized_data['item']
        merchant = normalized_data['merchant']

        self.assertEquals(purchaser.name, 'Joao Silva')
        self.assertEquals(purchaser.count, 2)

        self.assertEquals(item.description, 'R$10 off R$ 20 of food')
        self.assertEquals(item.price, 10.0)

        self.assertEquals(merchant.address, '987 Fake St')
        self.assertEquals(merchant.name, 'Bobs Pizza')

    @mock.patch.object(models.Merchant, 'objects')
    @mock.patch.object(models.Item, 'objects')
    @mock.patch.object(models.Purchaser, 'objects')
    @mock.patch('purchase.models.Purchase')
    def test_normalize_data_must_save_some_of_the_normalized_models(self, purchase_model_mock,
            purchaser_manager_mock, item_manager_mock, merchant_manager_mock):
        fake_parsed_line = ('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        views.normalize_data(fake_parsed_line)
        self.assertTrue(purchaser_manager_mock.get_or_create.called)
        self.assertTrue(item_manager_mock.get_or_create.called)
        self.assertTrue(merchant_manager_mock.get_or_create.called)


    def test_normalize_data_should_cast_to_int_the_purchaser_count(self):
        pass

    def test_normalize_data_should_cast_to_float_the_item_price(self):
        pass
