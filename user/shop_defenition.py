from time import gmtime, strftime

import items.itemloader as itemloader

import logging
from constants import *

from localizations import locale_manager

def open_shop(self, reply):
	self.state = 'shop'

	if self.visited_shop:
		self.open_corridor(reply)
		return

	self.shop_items = itemloader.load_shop_items()

	items =  [ itemloader.load_item(i[1], i[0]) for i in self.shop_items ]
	self.shop_names = [ i.name for i in items ]
	self.shop_names.append(locale_manager.get('EXIT'))

	for item in self.get_items():
		item.on_shop(self, reply, items)

	txt = locale_manager.get('SHOP_MESSAGE').format(
		items[0].name, items[0].price, items[0].description, 
		items[1].name, items[1].price, items[1].description,
		items[2].name, items[2].price, items[2].description
	)

	reply(txt, self.shop_names)

def buy(self, item, reply):
	if self.paid(item.price):
		if item.buff == 'bad':
			reply(locale_manager.get('BAD_BUYED'))
		elif item.buff == 'good':
			reply(locale_manager.get('GOOD_BUYED'))
		else:
			reply(locale_manager.get('NEUTRAL_BUYED'))

		check = locale_manager.get('SHOP_CHECK').format(strftime("%Y-%m-%d %H:%M:%S UTC", gmtime()), item.name, item.price,)

		self.items.append((item.buff, item.code_name))
		item.on_buy(self, reply)
		reply(check)

		self.visited_shop = True
		self.open_corridor(reply)
	else:
		reply(locale_manager.get('NO_GOLD'), self.shop_names)

def shop(self, reply, text):
	if text == locale_manager.get('EXIT'):
		reply(locale_manager.get('SHOP_EXITED'))
		self.open_corridor(reply)
	else:
		for ind, name in enumerate(self.shop_names):
			if name == text:
				buff, name = self.shop_items[ind]
				item = itemloader.load_item(name, buff)
				self.buy(item, reply)
				return

		reply(locale_manager.get('NO_GOODS'), self.shop_names)