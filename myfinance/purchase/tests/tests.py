from django.test import TestCase, Client
from purchase import views, models
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

    @mock.patch('purchase.views.render')
    @mock.patch.object(views, 'import_data')
    def test_purchase_importer_form_must_render_the_template_with_import_feedback_and_the_purchase_total_messages_in_case_of_post_request(self,
            import_data_mock, render_mock):
        fake_import_data_messages = {'import_feedback': 'Foo', 'purchase_total': 'Bar'}
        import_data_mock.return_value = fake_import_data_messages
        request_mock = mock.Mock()
        request_mock.method = 'POST'
        views.purchase_importer_form(request_mock)
        self.assertTrue(import_data_mock.called)
        render_mock.assert_called_with(
            request_mock,
            'purchase_importer_form.html',
            fake_import_data_messages,
        )

    @mock.patch.object(views, 'import_data')
    def test_purchase_importer_form_should_not_calls_import_data_in_case_of_get_request(self, import_data_mock):
        self.client.get('/purchase/pdi/')
        self.assertFalse(import_data_mock.called)


class ImportDataViewTestCase(TestCase):

    @mock.patch.object(views, 'calc_purchase_total')
    @mock.patch.object(views, 'save_purchase_data')
    @mock.patch.object(views, 'read_file_lines')
    @mock.patch.object(views, 'parse_purchase_file_data')
    @mock.patch.object(models, 'Purchase')
    def test_import_data_should_return_a_save_feedback_message_and_the_purchase_total(self,
            purchase_model_mock, parse_purchase_file_data_mock, read_file_lines_mock,
            save_purchase_data_mock, calc_purchase_total_mock):
        request_mock = mock.Mock()
        request_mock.FILES = {'purchase_file': mock.Mock()}

        fake_file_line = iter([
            ('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        ])
        read_file_lines_mock.return_value = fake_file_line

        calc_purchase_total_mock.return_value = 20

        messages = views.import_data(request_mock)

        self.assertIn('import_feedback', messages)
        self.assertIn('purchase_total', messages)

        self.assertEquals(messages['import_feedback'], 'Importacao efetuada com sucesso.')
        self.assertEquals(messages['purchase_total'], 'A receita bruta total foi de R$ 20.')

    @mock.patch.object(views, 'calc_purchase_total')
    @mock.patch.object(views, 'save_purchase_data')
    @mock.patch.object(views, 'read_file_lines')
    @mock.patch.object(views, 'parse_purchase_file_data')
    def test_import_data_integration(self, parse_purchase_file_data_mock,
            read_file_lines_mock, save_purchase_data_mock, calc_purchase_total_mock):
        request_mock = mock.Mock()
        fake_purchase_file = StringIO()
        request_mock.FILES = {'purchase_file': fake_purchase_file}

        file_line = ('Joao Silva', 'R$10 off R$ 20 of food', '10.0', '2', '987 Fake St', 'Bobs Pizza')
        read_file_lines_mock.return_value = iter([file_line])

        parsed_data = {
            'purchaser_name': 'Joao Silva',
            'item_description': 'R$10 off R$ 20 of food',
            'item_price': 10.0,
            'purchase_count': 2,
            'merchant_address': '987 Fake St',
            'merchant_name': 'Bobs Pizza'
        }
        parse_purchase_file_data_mock.return_value = parsed_data

        views.import_data(request_mock)

        read_file_lines_mock.assert_called_with(fake_purchase_file)

        parse_purchase_file_data_mock.assert_called_with(file_line)

        save_purchase_data_mock.assert_called_with(parsed_data)

        calc_purchase_total_mock.assert_called_with(parsed_data)


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

    @mock.patch.object(models.Merchant.objects, 'get_or_create')
    @mock.patch.object(models.Item.objects, 'get_or_create')
    @mock.patch.object(models.Purchaser.objects, 'get_or_create')
    @mock.patch.object(models, 'Purchase')
    def test_save_purchase_data_should_save_all_the_file_data_in_models_which_represents_a_purchase(self,
            purchase_model_mock, purchaser_create_mock, item_create_mock, merchant_create_mock):
        # Mocking all models
        purchaser_object = mock.Mock()
        purchaser_create_mock.return_value = [purchaser_object]
        item_object = mock.Mock()
        item_create_mock.return_value = [item_object]
        merchant_object = mock.Mock()
        merchant_create_mock.return_value = [merchant_object]
        purchase_object_mock = mock.Mock()
        purchase_model_mock.return_value = purchase_object_mock
        purchase_count = 2

        parsed_data = {
            'purchaser_name': 'Joao Silva',
            'item_description': 'R$10 off R$ 20 of food',
            'item_price': 10.0,
            'purchase_count': purchase_count,
            'merchant_address': '987 Fake St',
            'merchant_name': 'Bobs Pizza'
        }
        views.save_purchase_data(parsed_data)

        purchaser_create_mock.assert_called_with(name=parsed_data['purchaser_name'])

        item_create_mock.assert_called_with(
            description=parsed_data['item_description'],
            price=parsed_data['item_price']
        )

        merchant_create_mock.assert_called_with(
            name=parsed_data['merchant_name'],
            address=parsed_data['merchant_address']
        )

        self.assertTrue(purchase_object_mock.save.called)

        purchase_model_mock.assert_called_with(purchaser=purchaser_object, item=item_object,
            merchant=merchant_object, count=purchase_count)
