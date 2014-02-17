# -*- coding: utf-8 -*-

from django.shortcuts import render


def purchase_importer_form(request):
    import_message = ''
    if request.method == 'POST':
        import_message = import_data(request)
    return render(
        request,
        'purchase_importer_form.html',
        {'message': import_message}
    )


def import_data(request):
    purchase_file = request.FILES['purchase_file']
    parse_purchase_file_data(purchase_file)
    return 'Importacao efetuada com sucesso'

def parse_purchase_file_data(purchase_file):
    import ipdb;ipdb.set_trace();
    file_header = purchase_file.readline()
    for line in purchase_file.readline():
        yield tuple(line.split('    '))

def save_purchase_data(file_line):
    pass
