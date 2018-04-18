from inmemorycache import vendor_data, restaurent_items
import uuid
import json

class Order(object):
	def __init__(self, username, invoice):
		self.username = username
		self.invoice = invoice
		self.items = []

	def set_item(self, item_id, item_name, count):
		self.items.append( [item_id, item_name, count] )

	def __repr__(self):
		return '[username = {}, invoice number = {}, items=({})]'.format(self.username, self.invoice, self.items)

def consume_order(invoice):
	current_count = get_current_count_before_invoice(invoice)
	print('current_count before consuming the first order', current_count, invoice)
	for k, v in vendor_data.items():
		for o in v:
			if o.invoice == invoice:
				v.remove(o)
				return '1'
	return '0'


def get_current_count_before_invoice(invoice):
	for k, v in vendor_data.items():
		current_count = 0;
		for o in v:
			print(k, o, current_count)
			if o.invoice == invoice:
				count = current_count
				return count
			else:
				current_count += 1
	return -1

def get_total_count(restaurent_id):
	return len(vendor_data[restaurent_id])

def add_order(restaurent_id, order):
	vendor_data[restaurent_id].append(order)
	print('total count of', restaurent_id, ' is', get_total_count(restaurent_id))

def create_order(restaurent_id, username, items):
	order = Order(username, str(uuid.uuid4()))
	for item in items:
		order.set_item(item['itemId'], get_item_name(item['itemId']), item['count'])
	print('LOG ', 'Order created for restaurent_id = {}, Order = {}'.format(restaurent_id, order))
	add_order(restaurent_id, order)
	return order

def get_item_name(item_id):
	restaurent_id = int(item_id.split('_')[0])
	restaurent_item = list(filter(lambda x : x['id'] == restaurent_id, restaurent_items))[0]
	item_name = list(filter(lambda x: x['id'] == item_id, restaurent_item['items']))[0]['name']
	return item_name

def get_orders_for_customer(username):
	orders = []
	for k, v in vendor_data.items():
		for o in v:
			if o.username == username:
				orders.append(o)
				print(username, o)
	return orders

def get_order_details(invoice):
	order = None
	for k, v in vendor_data.items():
		for o in v:
			if o.invoice == invoice:
				order = o
				return order
	return order