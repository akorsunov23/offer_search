from django.db import models


class Good(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)

	def __str__(self):
		return self.name


class StockGood(models.Model):
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
	good = models.ForeignKey(Good, on_delete=models.CASCADE)
	rate = models.DecimalField(decimal_places=2, max_digits=10, null=False, blank=False)
	amount = models.PositiveIntegerField()


class Stock(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)
	goods = models.ManyToManyField(Good, through=StockGood)
	all_limit = models.IntegerField()
	transportation_cost = models.DecimalField(default=0.01, decimal_places=2, max_digits=10)

	def __str__(self):
		return self.name


class ClientGood(models.Model):
	client = models.ForeignKey('Client', on_delete=models.CASCADE)
	good = models.ForeignKey(Good, on_delete=models.CASCADE)
	amount = models.PositiveIntegerField()


class Client(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)
	goods = models.ManyToManyField(Good, through=ClientGood)

	def __str__(self):
		return self.name
