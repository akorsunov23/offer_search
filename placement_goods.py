import random


class Goods:
	"""
	Класс, описывающий товары.
	При инициализации объекта на вход подаётся список товаров, пользователем.
	"""
	def __init__(self, goods: list):
		self._goods = goods

	def get_goods(self):
		return self._goods


class Stocks:
	"""
	Класс, описывающий склад.
	"""

	def __init__(self, name: str, amount_goods: int, goods: list):
		"""
		При инициализации склада, формируется словарь с товарами.
		:param name: Наименование склада.
		:param amount_goods: Количество хранимого товара на складе.
		"""
		self.__goods = goods
		self.__good = None
		self.__name = name
		self.__amount_goods = self.__set_amount_goods(amount_goods)
		self.__stock = dict()

	def __set_amount_goods(self, amount: int) -> int:
		"""
		Сеттер, проверяющий введённое количество товара и в зависимости от проверки устанавливает значение.
		:param amount: Количество товара, введённое пользователем.
		:return: Установленное значение.
		"""
		if amount > len(self.__goods):
			return len(self.__goods)
		else:
			return amount

	def get_stock(self) -> dict:
		"""
		Метод возвращающий скрытый атрибут
		:return: Список со словарями описывающий Склад.
		"""
		self.__stock['name'] = self.__name
		self.__stock['all_limit'] = random.randint(10, 500)
		self.__stock['transportation_cost'] = 0.01

		self.__good = random.sample(self.__goods, k=self.__amount_goods)

		for good in self.__good:
			limit = random.randint(10, 500)
			self.__stock[good] = {
					'limit': limit if limit < self.__stock['all_limit'] else self.__stock['all_limit'],
					'rate': random.randint(1, 100),
				}

		return self.__stock

	def __str__(self):
		return self.__name


class Clients:
	pass


new_goods = [
	'K1', 'K2', 'K3', 'K4', 'K5',
	'K6', 'K7', 'K8', 'K9', 'K10',
	'K11', 'K12', 'K13', 'K14', 'K15',
	'K16', 'K17', 'K18', 'K19', 'K20'
]
stocks = list()

k = Goods(goods=new_goods)

for stock in range(1, 11):
	stocks.append(Stocks(name=f'C{stock}', amount_goods=random.randint(1, 20), goods=k.get_goods()).get_stock())

# print(stocks)
