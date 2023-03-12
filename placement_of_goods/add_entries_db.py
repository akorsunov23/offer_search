"""
Модуль, наполняющий модели базы данных необходимыми записями.
В SETTINGS задаются параметры для дальнейшего наполнения БД.
'goods' = Список товаров;
'amount_stocks' = Количество складов;
'amount_clients' = Количество клиентов.

После запуска модуля, БД наполняется. При следующем запуске параметры необходимо изменить для избежания дублирования.
"""

import os
import random

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_job.settings')
django.setup()

from placement_of_goods.models import Good, Stock, Client


def add_goods(goods_list: list) -> None:
	"""
	Функция, добавляющая в модель товары.
	"""
	for good in goods_list:
		Good.objects.create(name=good)


def add_stocks(amount: int) -> None:
	"""
	Функция, добавляющая в модель количество складов по заданному параметру.
	:param amount: Количество складов, задаётся пользователем.
	"""
	for i in range(1, amount + 1):
		amount_goods: int = random.randint(1, 20)
		goods_list: list = random.sample(list(Good.objects.all()), k=amount_goods)

		Stock.objects.create(
			name=f'C{i}',
			all_limit=random.randint(1, 1000)
		)
		for good in goods_list:
			Stock.objects.get(name=f'C{i}').stockgood_set.create(
				good=good,
				rate=round(random.uniform(1, 100), 2),
				amount=random.randint(1, 100)
			)


def add_clients(amount: int) -> None:
	"""
	Функция, добавляющая в модель количество клиентов по заданному параметру.
	:param amount: Количество клиентов, задаётся пользователем.
	"""
	for i in range(1, amount + 1):
		amount_goods: int = random.randint(1, 20)
		goods_list: list = random.sample(list(Good.objects.all()), k=amount_goods)

		Client.objects.create(
			name=f'K{i}',
		)
		for good in goods_list:
			Client.objects.get(name=f'K{i}').clientgood_set.create(
				good=good,
				amount=random.randint(1, 50)
			)


SETTINGS: dict = {
	'goods': [
		'T1', 'T2', 'T3', 'T4', 'T5',
		'T6', 'T7', 'T8', 'T9', 'T10',
		'T11', 'T12', 'T13', 'T14', 'T15',
		'T16', 'T17', 'T18', 'T19', 'T20'
	],
	'amount_stocks': 10,
	'amount_clients': 10,
}


if __name__ == '__main__':
	add_goods(goods_list=SETTINGS['goods'])
	add_stocks(amount=SETTINGS['amount_stocks'])
	add_clients(amount=SETTINGS['amount_clients'])
