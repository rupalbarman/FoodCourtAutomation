from flask import Flask, render_template, request, jsonify, session, abort
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from inmemorycache import users, restaurent_items
import uuid
import json

import processing as pro

app = Flask(__name__)

def require_login(func):
    """Checks whether user is logged in or raises error 401."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_user'):
            return login()
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
	    json = request.get_json()
	    username = json['username']
	    password = json['password']
	    status = str()
	    if username in (x['username'] for x in users):
	    	status = 'login'
	    else:
	    	status = 'signup'
	    	users.append({'username' : username , 'password' : password})
	    session['logged_user'] = username
	    return jsonify( status=status, username=username, password=password)

@app.route('/api/get_users', methods=['GET'])
@require_login
def get_users():
	return jsonify( {'users' : users})

@app.route('/logout', methods=['GET'])
def logout():
	session.clear()
	return index()

@app.route('/api/get_restaurents', methods=['GET'])
@require_login
def list_restaurents():
	return render_template('restaurent.html', data = restaurent_items )

@app.route('/api/get_restaurents/<int:id>', methods=['GET'])
@require_login
def show_menu(id):
	menu = list(filter(lambda t: t['id'] == id, restaurent_items))
	if len(menu) == 0:
		abort(404)
	return jsonify( { 'menu': menu } )

@app.route('/api/checkout', methods=['POST'])
@require_login
def checkout():
	json = request.get_json()

	# get those values
	username = json['username']
	items = json['items']
	restaurent_id = items[0]['itemId'].split('_')[0]

	# create and add order to the vendor data
	order = pro.create_order(restaurent_id, username, items)

	return jsonify( status='Order placed', invoice=order.invoice, username=username, items=order.items)

@app.route('/api/check_order_status/<string:invoice>', methods=['GET'])
def check_order_status(invoice):
	print('Order check for invoice = {}'.format(invoice), ' is {}'.format(pro.get_current_count_before_invoice(invoice)))
	return jsonify({ 'status' : pro.get_current_count_before_invoice(invoice) })

@app.route('/api/get_orders/<string:username>', methods=['GET'])
@require_login
def get_orders(username):
	orders = pro.get_orders_for_customer(username)
	#directly converting to json, without a key
	#return json.dumps(orders, default=lambda x: x.__dict__)
	return render_template('order.html', orders = orders)

@app.route('/api/get_order_details/<string:invoice>', methods=['GET'])
@require_login
def get_order_details(invoice):
	order = pro.get_order_details(invoice)
	return jsonify(order=json.dumps(order, default=lambda x: x.__dict__))

# ------------------------------------------------------------------
# Restaurent vendor operations

@app.route('/api/consume_order/<string:invoice>', methods=['GET'])
def consume_order(invoice):
	status = pro.consume_order(invoice)
	print('Consume order for ', invoice, ' Status', status)
	return jsonify(consume=status)

if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host='0.0.0.0', port=8000, debug=True)