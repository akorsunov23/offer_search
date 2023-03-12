from django.contrib import admin
from .models import Good, Stock, Client


class StockGoodInline(admin.StackedInline):
	model = Stock.goods.through


class ClientGoodInline(admin.StackedInline):
	model = Client.goods.through


@admin.register(Good)
class GoodsAdmin(admin.ModelAdmin):
	list_display = 'name',


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
	inlines = StockGoodInline,
	list_display = 'name',


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	inlines = ClientGoodInline,
	list_display = 'name',
