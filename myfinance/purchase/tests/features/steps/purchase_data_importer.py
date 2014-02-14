# -*- coding: utf-8 -*-

from behave import given, when, then
from nose import tools
from django.conf import settings
import os

@given(u'que eu acesso o formulário de importação')
def that_i_access_the_importer_form(context):
    context.browser.get('http://127.0.0.1:8000/purchase/pdi')

@given(u'que eu faço o upload de um arquivo')
def that_i_upload_a_purchase_file(context):
    purchase_file_field = context.browser.find_element_by_name('purchase_file')
    tools.assert_true(purchase_file_field)
    #purchase_file_path = os.path.join(settings.BASE_DIR, 'example_input.tab')
    purchase_file_path = '/home/rcarvalho/Workspace/desafio-programacao-1/example_input.tab'
    purchase_file_field.send_keys(purchase_file_path)

@when('eu pressiono o botão importar')
def i_press_the_import_button(context):
    import_button = context.browser.find_element_by_name('import_button')
    import_button.click()

@then('eu devo ver "{message}"')
def i_must_see_the_message(context, message):
    import ipdb;ipdb.set_trace();
    message_field = context.browser.find_element_by_id('message')
