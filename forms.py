from wtforms import Form, StringField, DecimalField, validators

class ProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    unit = StringField('Unit', [validators.Length(min=1, max=20)])
    unit_price = DecimalField('Unit_price', [validators.NumberRange(min=0.1, max=9999)])
    quantity = DecimalField('Quantity', [validators.NumberRange(min=0.1, max=9999)])