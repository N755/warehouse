from flask import Flask, render_template, request,redirect, url_for, make_response 
from typing import List, Dict
from forms import ProductForm, ProductSaleForm
import csv
import io


app = Flask(__name__)
app.secret_key  = 'secret'

@app.route('/', methods=['GET'])
def get_homepage():
    return render_template('base.html')


class Product:
    def __init__(self, name: str, unit: str, unit_price: float, quantity:float):
        self.name = name
        self.unit = unit
        self.unit_price = unit_price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name} {self.unit} {self.unit_price} {self.quantity}"
        
  
ITEMS = [
    Product('Apple', 'kg', 2, 10),
    Product('Banana', 'kg', 7, 12),
    Product('Orange', 'kg', 8, 2)
    ]

@app.route('/products', methods=['GET'])
def product_list():
    form = ProductForm(request.form)
    for item in ITEMS:
        item.form = ProductSaleForm()
    return render_template('product_list.html', form=form, ITEMS=ITEMS)

@app.route('/add', methods=['POST'])
def add_product():
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        unit = form.unit.data
        unit_price = form.unit_price.data
        quantity = form.quantity.data
        product = Product(name, unit, unit_price, quantity)
        ITEMS.append(product)
        print('hi')
        return redirect(url_for('product_list'))
    else:
        return render_template('product_list.html', form=form, ITEMS=ITEMS)

@app.route('/sell/<product_name>', methods=['GET', 'POST'])
def sell_product(product_name):
    product = next((item for item in ITEMS if item.name == product_name), None)
    if product is None:
        return redirect(url_for('product_list'))
    form = ProductSaleForm(request.form)
    if request.method == 'POST' and form.validate():
        sold_quantity = form.quantity.data
        product.quantity -= sold_quantity
        return redirect(url_for('product_list'))
    return render_template('sell_product.html', product=product, form=form)



@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        file = request.files['file']
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)
        for row in csv_input:
            name, unit, unit_price, quantity = row
            product = Product(name, unit, float(unit_price), float(quantity))
            ITEMS.append(product)
        return redirect(url_for('product_list'))
    return render_template('import_data.html')

@app.route('/export', methods=['GET'])
def export_data():
    data = [['Name', 'Unit', 'Unit Price', 'Quantity']]
    for item in ITEMS:
        data.append([item.name, item.unit, item.unit_price, item.quantity])
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True)