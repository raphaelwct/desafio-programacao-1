# -*- coding: utf-8 -*-

from behave import step, given
from nose import tools

@given(u'que eu acesso o formulário de importação')
def that_i_access_the_importer_form(context):
    context.browser.get('http://127.0.0.1:8000/pdi')

@given(u'que eu faço o upload de um arquivo')
def that_i_upload_a_purchase_file(context):
    purchase_file_field = context.browser.find_element_by_name('purchase_file')
    tools.assert_true(purchase_file)
