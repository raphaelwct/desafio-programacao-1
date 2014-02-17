# -*- coding: utf-8 -*-

from django.shortcuts import render
from purchase import models


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
    for parsed_line in parse_purchase_file_data(purchase_file):
        save_purchase_data(parsed_line)
    return 'Importacao efetuada com sucesso'

def parse_purchase_file_data(purchase_file):
    file_header = purchase_file.readline()
    for line in purchase_file.readline():
        yield tuple(line.split('    '))

def save_purchase_data(file_line):
    normalized_data = normalize_data(file_line)
    normalized_data['purchaser'].save()
    normalized_data['item'].save()
    normalized_data['merchant'].save()

def normalize_data(file_line):
    normalized_data = {
        'purchaser': models.Purchaser(name=file_line[0], count=int(file_line[3])),
        'item': models.Item(description=file_line[1], price=float(file_line[2])),
        'merchant': models.Merchant(address=file_line[4], name=file_line[5])
    }
    return normalized_data
