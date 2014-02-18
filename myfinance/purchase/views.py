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
    purchase_total = 0

    purchase_file = request.FILES['purchase_file']
    for parsed_line in parse_purchase_file_data(purchase_file):
        save_purchase_data(parsed_line)
        item_price = float(parsed_line[2])
        purchase_count = int(parsed_line[3])
        purchase_total += item_price * purchase_count

    return {
        'import_feedback': "Importacao efetuada com sucesso",
        'purchase_total': "A receita bruta total foi de R$ %s" % purchase_total
    }


def parse_purchase_file_data(purchase_file):
    purchase_file = iter(purchase_file)
    purchase_file.next()
    for line in purchase_file:
        yield (tuple(line.split('\t')))


def save_purchase_data(file_line):
    normalized_data = normalize_data(file_line)
    # normalized_data['purchaser'].objects.get_or_create()
    # normalized_data['item'].objects.get_or_create()
    # normalized_data['merchant'].objects.get_or_create()
    purchase = models.Purchase(
        purchaser=normalized_data['purchaser'],
        item=normalized_data['item'],
        merchant=normalized_data['merchant']
    )
    purchase.save()


def normalize_data(file_line):
    purchaser = models.Purchaser.objects.get_or_create(
        name=file_line[0], count=int(file_line[3]))[0]
    item = models.Item.objects.get_or_create(
        description=file_line[1], price=float(file_line[2]))[0]
    merchant = models.Merchant.objects.get_or_create(
        address=file_line[4], name=file_line[5])[0]

    return {
        'purchaser': purchaser,
        'item': item,
        'merchant': merchant
    }
