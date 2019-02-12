import os
import pandas

from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from inspect import getmembers
from pprint import pprint
from .models import Sales

def upload(request):
	'''processa o processo upload com arquivo enviado pelo formulário'''
	total_revenue = 0

	if request.method == 'POST' and request.FILES['spreadsheet_file']:
		spreadsheet_file = request.FILES['spreadsheet_file']
		file_only_name, file_ext = os.path.splitext(spreadsheet_file.name)

		if not file_ext == '.tab':
			return render(request, 'upload.html', {'msg': 'Invalid extension, please select only TAB spreadsheets'}, status=415)
		else:
            
			path_saved_file = save_file(spreadsheet_file)
			sales_sheet = get_sales_sheet(path_saved_file)
			sales_list = get_data_sheet(sales_sheet)
			save_sales(sales_list)
			total_revenue = get_total_revenue(sales_sheet)

	return render(request, 'upload.html', {'total_revenue': total_revenue})

def save_file(spreadsheet_file):
	'''salva o arquivo no diretório configurado em settings.py linhas (128, 129) e retorna o caminho do mesmo'''
	fs = FileSystemStorage()
	filename = fs.save(spreadsheet_file.name, spreadsheet_file)
	uploaded_file_url = fs.url(filename)
	full_path_file = '{}/{}/{}'.format(os.getcwd(), 'spreadsheets', spreadsheet_file.name)
	return full_path_file

def get_total_revenue(sales_sheet):
	'''retorna a soma da receita total descrita na planilha'''
	revenue = sales_sheet['purchase_total'].sum()
	return revenue

def get_sales_sheet(file_name):
	'''retorna um objeto Dataframe carregado pelo Pandas com os dados do arquivo .tab'''
	sales_sheet = pandas.read_csv(file_name, sep='\t')
	#realiza a multiplicação da quantidade pelo preço para conseguir o total em outro momento
	sales_sheet['purchase_total'] = sales_sheet.apply(lambda row: (row['purchase count']*row['item price']), axis=1)
	return sales_sheet

def get_data_sheet(sales_sheet):
	'''cria lista com dicionários de sales alimantada pelo dados do Dataframe'''	
	sales_list = []

	for sale_line in sales_sheet.values:
		new_sale = {}

		for k_sale, sale_value in enumerate(sale_line):
			new_sale[sales_sheet.columns.values[k_sale]] = sale_value

		sales_list.append(new_sale)

	return sales_list

def save_sales(sales_list):
	'''remove e salva todas as informações da planilha no postgres'''
	Sales.objects.all().delete()
	for sale in sales_list:
		sale_database = Sales()
		sale_database.purchaser_name = sale.get('purchaser name')
		sale_database.item_description = sale.get('item description')
		sale_database.item_price = sale.get('item price')
		sale_database.purchase_count = sale.get('purchase count')
		sale_database.merchant_address = sale.get('merchant address')
		sale_database.merchant_name = sale.get('merchant name')
		sale_database.save()