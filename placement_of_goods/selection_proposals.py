"""
Модуль, выполняющий поиск оптимальных предложений для хранения товара клиента.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_job.settings')
django.setup()

import random
from placement_of_goods.models import Client, Stock
from django.db.models import QuerySet
from django.db import transaction
from django.db.models import F


def convenient_offers(offers_dict: dict, all_goods: list) -> dict:
	"""
	Функция, из списка всех возможных складов выбирает самые оптимальные.
	:param offers_dict: Список всех предложений.
	:param all_goods: Список всех продуктов клиента.
	:return: Список оптимальных предложений, минимизирует количество складов, на которые необходимо везти товар.
	"""
	result = dict()
	new = dict()

	for goods, stock in offers_dict.items():
		for stock_info in stock:
			stock_id = stock_info['stock']
			if stock_id not in result:
				result[stock_id] = [
					{
						'good': goods,
						'price': stock_info['price']
					}
				]
			else:
				result[stock_id].append(
					{
						'good': goods,
						'price': stock_info['price']
					}
				)
	sorted_result = {key: value for key, value in sorted(result.items(), key=lambda x: len(x[1]), reverse=True)}

	for key, value in sorted_result.items():
		if len(value) == len(all_goods):
			new[key] = value
			return new
		else:
			if len(all_goods) > 0:
				for good_i in value:
					if good_i['good'] in all_goods:
						all_goods.remove(good_i['good'])
						if key in new:
							new.setdefault(key, []).append(good_i)
						else:
							new[key] = [good_i]

	return new


def cheap_offers(offers_dict: dict) -> dict:
	"""
	Функция, из набора всех возможных предложения выбирает самые дешёвые.
	:param offers_dict: Список всех возможных складов.
	:return: Список самых дешёвых складов.
	"""
	min_price: int = 0
	result = dict()

	for key, value in offers_dict.items():
		min_price = offers_dict[key][0]['price']
		result[key] = offers_dict[key][0]

		for val in value:
			if val['price'] < min_price:
				min_price = val['price']
				result[key] = val

	return result


def placement_arrangement(data_goods: dict, flag: bool) -> str:
	"""
	Функция, выполняет размещение товара на складах в зависимости о выбранного способа хранения.
	:param data_goods: Массив с выбранным способом.
	:param flag: Флаг, указывающий на то, какой способ выбран.
	:return: Строка с информацией о размещении товара, если место на складах заканчивается,
	возвращаться соответствующая информация.
	"""
	result = list()

	if flag:
		for key, values in data_goods.items():
			for value in values:
				with transaction.atomic():
					Stock.objects.filter(name=key).update(
						all_limit=F('all_limit') - value['good'].amount
					)
					if Stock.objects.get(name=key).all_limit > 0:
						result.append(f'{value["good"].good.name} размещён')
					else:
						result.append(f'{value["good"].good.name} не размещён')
	else:
		for key, values in data_goods.items():
			with transaction.atomic():
				Stock.objects.filter(name=values['stock']).update(
					all_limit=F('all_limit') - key.amount
				)
				if Stock.objects.get(name=values['stock']).all_limit > 0:
					result.append(f'{key.good.name} размещён')
				else:
					result.append(f'{key.good.name} не размещён')

	if len(result) > 0:
		return ', '.join(result)
	else:
		return 'На складах закончилось место'


def select_proposals(clients: QuerySet, stocks: QuerySet) -> None:
	"""
	Функция, проводящая поиск всех возможных складов которые готовы принять товар от клиента,
	для дальнейшей передачи этих данных в функции для сортировки (самый удобное и дешёвое предложение).
	Затем после рандомного выбора способа хранения, данные передаются в функцию для оформления заказа.
	:param clients: Queryset, модели Client.
	:param stocks: Queryset, модели Stock.
	"""
	for client in clients:
		offers = dict()
		goods = list()
		cheap_offer_list = list()
		convenient_offer_list = list()

		for good in client.clientgood_set.all():
			goods.append(good)
			for stock in stocks:
				for good_stock in stock.stockgood_set.all():
					if good.good.name == good_stock.good.name \
							and good.amount <= good_stock.amount \
							and good.amount <= stock.all_limit:
						distance = random.randint(1, 50)
						price_storage = good.amount * distance * stock.transportation_cost
						info = {
							'stock': stock,
							'amount': good_stock.amount,
							'price': price_storage
						}
						if good in offers.keys():
							offers.setdefault(good, []).append(info)
						else:
							offers[good] = [info]

		convenient_offer = convenient_offers(offers_dict=offers, all_goods=goods.copy())
		cheap_offer = cheap_offers(offers_dict=offers)

		for key, value in convenient_offer.items():
			values = list()
			for good in value:
				values.append(good['good'].good.name)

			text = 'Склад {stock} - товары({goods})'.format(
				stock=key,
				goods=', '.join(values)
			)
			convenient_offer_list.append(text)

		for key, value in cheap_offer.items():
			text = '{good} - (склад: {stock}, цена: {price})'.format(
				good=key.good.name,
				stock=value['stock'],
				price=value['price']
			)
			cheap_offer_list.append(text)

		var = [['Оптимальные предложения', convenient_offer], ['Дешёвые предложения', cheap_offer]]
		selected_option = random.choice(var)
		if selected_option == var[0]:
			placement_arrangement_goods = placement_arrangement(
				data_goods=selected_option[1],
				flag=True
			)
		else:
			placement_arrangement_goods = placement_arrangement(
				data_goods=selected_option[1],
				flag=False
			)

		text = 'Клиент {name}' \
			   '\nТовары: {good}' \
			   '\nСамые оптимальные предложения: {stock}' \
			   '\nСамые дешевые варианты размещения: {stock_1}' \
			   '\nКлиент выбрал: {var}' \
			   '\n{accommodation}\n'.format(
			name=client.name,
			good=', '.join([f'{good.good.name} - {good.amount}шт.' for good in goods]),
			stock=', '.join(convenient_offer_list),
			stock_1=', '.join(cheap_offer_list),
			var=selected_option[0],
			accommodation=placement_arrangement_goods
		)
		print(text)


all_clients = Client.objects.all().prefetch_related('clientgood_set')
all_stocks = Stock.objects.all().prefetch_related('stockgood_set')

if __name__ == '__main__':
	select_proposals(clients=all_clients, stocks=all_stocks)
