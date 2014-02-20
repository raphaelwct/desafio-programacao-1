# -*- coding: utf-8 -*-

from behave import given, when, then
from nose import tools
from myfinance import settings
from purchase import models
import os


@given(u'que eu acesso o formulario de importacao')
def that_i_access_the_importer_form(context):
    context.browser.get('http://127.0.0.1:8000/purchase/pdi')


@given(u'que eu faco o upload de um arquivo')
def that_i_upload_a_purchase_file(context):
    purchase_file_field = context.browser.find_element_by_name('purchase_file')
    tools.assert_true(purchase_file_field)
    purchase_file_path = os.path.join(settings.BASE_DIR, '..', 'example_input.tab')
    purchase_file_field.send_keys(purchase_file_path)


@when(u'eu pressiono o botao importar')
def i_press_the_import_button(context):
    import_button = context.browser.find_element_by_name('import_button')
    import_button.click()


@then(u'eu devo ver "{import_feedback}"')
def i_must_see_the_message(context, import_feedback):
    import_message_field = context.browser.find_element_by_id('import_feedback')
    tools.assert_equals(import_feedback, import_message_field.text)


@then(u'todos os dados do arquivo devem estar armazenados em banco de dados')
def all_the_file_data_must_be_saved_on_database(context):
    tools.assert_equals(models.Purchase.objects.count(), 4)
    tools.assert_equals(models.Purchaser.objects.count(), 4)
    tools.assert_equals(models.Item.objects.count(), 3)
    tools.assert_equals(models.Merchant.objects.count(), 3)


@then(u'eu devo ver a receita bruta total representada pelo arquivo enviado')
def i_must_see_the_purchase_total_from_that_file(context):
    purchase_total_field = context.browser.find_element_by_id('purchase_total')
    expected_purchase_total_message = "A receita bruta total foi de R$ 95.0."
    tools.assert_equals(expected_purchase_total_message, purchase_total_field.text)
