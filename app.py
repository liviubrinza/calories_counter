from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, redirect, url_for, request
from CsvReader import CsvReader
from DailyTracker import DailyTracker
from Product import Product

app = Flask(__name__)

bootstrap = Bootstrap4(app)

csvReader = CsvReader()
dailyTracker = DailyTracker(csvReader=csvReader)


labels = ['Protein', 'Fats', 'Carbs']
values = [30, 40, 30]
colors = ["#1E81B0", "#DCE629", "#D93939"]


@app.route("/")
def main():
    return render_template('main.html')

@app.route('/products')
def get_products_list():
    success_message = None
    error_message = None

    if request.args:
     if 'success_message' in request.args.keys() and request.args['success_message'] is not None:
        success_message = request.args['success_message']
    if 'error_message' in request.args.keys() and request.args['error_message'] is not None:
        error_message = request.args['error_message']
            
    products = csvReader.get_products_list()
    return render_template('products.html', 
                           products=products, 
                           success_message=success_message,
                           error_message=error_message)

@app.route('/add_product', methods=['POST'])
def add_product():
    args = request.form

    new_product = Product(name=args['name'],
                          calories=args['calories'],
                          protein=args['protein'],
                          fats=args['fats'],
                          carbs=args['carbs'])

    retVal = csvReader.add_new_product(new_product=new_product)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully added product: " + args['name']
    else:
        error_message = "Error encountered while adding product: " + args['name']

    return redirect(url_for('get_products_list', success_message=success_message, error_message=error_message))

@app.route('/remove_product', methods=['GET', 'DELETE'])
def remove_product():
    args = request.args
    name = args['name']

    retVal = csvReader.remove_product(product_name=name)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully removed product: " + args['name']
    else:
        error_message = "Error encountered while removing product: " + args['name']

    return redirect(url_for('get_products_list', success_message=success_message, error_message=error_message))

@app.route('/change_product', methods=['GET', 'POST'])
def change_product():
    args = request.form
    print(args)
    return redirect(url_for('get_products_list'))



@app.route('/daily')
def daily_tracker():
    products = csvReader.get_products_list()

    success_message = None
    error_message = None

    if request.args:
     if 'success_message' in request.args.keys() and request.args['success_message'] is not None:
        success_message = request.args['success_message']
    if 'error_message' in request.args.keys() and request.args['error_message'] is not None:
        error_message = request.args['error_message']


    return render_template('daily.html', 
                            calories=dailyTracker.total_calories,
                            protein=dailyTracker.total_protein,
                            fats = dailyTracker.total_fats,
                            carbs = dailyTracker.total_carbs,
                            products = dailyTracker.products,
                            all_products = products,
                            max=17000, 
                            set=zip(values, labels, colors),
                            success_message=success_message, 
                            error_message=error_message)

@app.route('/add_product_daily', methods=['GET', 'POST'])
def add_product_daily():
    product = None
    quantity = 0

    if request.form:
        product = request.form.get('product')
        quantity = request.form.get('quantity')

    dailyTracker.add_product(name=product, quantity=quantity)

    return redirect(url_for('daily_tracker'))

@app.route('/remove_product_daily', methods=['GET', 'DELETE'])
def remove_product_daily():

    args = request.args
    name = args['name']

    retVal = dailyTracker.remove_product(name=name)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully removed product: " + name
    else:
        error_message = "Error encountered while removing product: " + name

    return redirect(url_for('daily_tracker', success_message=success_message, error_message=error_message))

@app.route('/adjust_product_daily', methods=['GET', 'POST'])
def adjust_product_daily():

    success_message = None
    error_message = None

    return redirect(url_for('daily_tracker', success_message=success_message, error_message=error_message))