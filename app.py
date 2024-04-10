from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key

print(secret_key)


client = MongoClient('mongodb://localhost:27017/')
db = client['shop_data']
shops_collection = db['shops']
items_collection = db['items']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seller', methods=['GET', 'POST'])
def seller():
    if request.method == 'POST':
        shop_no = request.form['shop_no']
        shop = shops_collection.find_one({'registration_no': shop_no})
        if shop:
            return redirect(url_for('shop_entry', shop_no=shop_no))
        else:
            return render_template('shop_reg.html', shop_no=shop_no)
    return render_template('seller.html')

@app.route('/shop_entry/<shop_no>', methods=['GET', 'POST'])
def shop_entry(shop_no):
    if request.method == 'POST':
        item_name = request.form['itemName']
        item_quantity = int(request.form['itemQuantity'])
        item_price = float(request.form['itemPrice'])
        gst_percentage = float(request.form['itemTax'])
        

        items_collection.insert_one({
            'shop_no': shop_no,
            'item_name': item_name,
            'item_quantity': item_quantity,
            'item_price': item_price,
            'gst_percentage': gst_percentage
        })
        
        return redirect(url_for('index'))
    
    return render_template('shop_entry.html', shop_no=shop_no)

@app.route('/register_shop', methods=['POST'])
def register_shop():
    if request.method == 'POST':
        shop_name = request.form['shopName']
        shop_address = request.form['shopAddress']
        gst_number = request.form['gstNumber']
        
     
        existing_shop = shops_collection.find_one({'gst_number': gst_number})
        if existing_shop:
            return "Shop with this GST number already exists."
        

        shops_collection.insert_one({
            'name': shop_name,
            'shop_address': shop_address,
            'registration_no': gst_number
        })
        
        return render_template('thank_you.html')


@app.route('/customer')
def customer():
    shop_list = shops_collection.find()
    return render_template('customer.html', shop_list=shop_list)

@app.route('/shop/<shop_no>', methods=['GET', 'POST'])
def shop(shop_no):
    shop = shops_collection.find_one({'registration_no': shop_no})
    if shop:
        if request.method == 'POST':
            selected_items = request.form.getlist('selected_items')
            item_quantity_mapping = {}
            for selected_item in selected_items:
                item_id, quantity = selected_item.split('-')
                item_quantity_mapping[item_id] = int(quantity)
            session['item_quantity_mapping'] = item_quantity_mapping
            session['shipping_address'] = request.form['shipping_address']
            print("1:", session['item_quantity_mapping'])
            session['shop_no'] = shop_no
            return redirect(url_for('generate_invoice'))

        items = items_collection.find({'shop_no': shop_no})
        items_as_dicts = [item for item in items]
        return render_template('shop.html', shop=shop, items=items_as_dicts)
    else:
        return "Shop not found."

@app.route('/generate_invoice')
def generate_invoice():
    item_quantity_mapping = session.get('item_quantity_mapping', {})
    shipping_address = session.get('shipping_address', '')
    shop_no = session.get('shop_no', '')
    shop = shops_collection.find_one({'registration_no': shop_no})
    print("2:", item_quantity_mapping)
    items = []
    total_amount = 0
    
    for item_id, quantity in item_quantity_mapping.items():
        item = items_collection.find_one({'_id': ObjectId(item_id)})
        print("3:", item)
        if item:
            item_price = float(item['item_price'])
            item_quantity = int(quantity)
            gst_percentage = float(item['gst_percentage'])

            total_price_excluding_tax = item_price * item_quantity
            tax_amount = total_price_excluding_tax * (gst_percentage / 100)
            total_price_including_tax = total_price_excluding_tax + tax_amount

            item['item_quantity'] = item_quantity 
            item['total_price_excluding_tax'] = total_price_excluding_tax
            item['tax_amount'] = tax_amount
            item['total_price_including_tax'] = total_price_including_tax

            total_amount += total_price_including_tax
            items.append(item)
    
    invoice_date = datetime.now().strftime("%Y-%m-%d")
    print("4:", shop)
    return render_template('invoice.html', items=items, total_amount=total_amount, shipping_address=shipping_address, shop=shop, invoice_date=invoice_date)

if __name__ == "__main__":
    app.run(debug=True)