from flask import Flask, render_template, request,redirect, url_for
from typing import List, Dict
from forms import ProductForm

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
    return render_template('product_list.html', products=ITEMS)

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
        return render_template('add.html', form=form, ITEMS=ITEMS)
    return 'Invalid form submission'
if __name__ == '__main__':
    app.run(debug=True)