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
    message = None
    if request.args and request.args['message']:
        print("PRODUCT LIST MESSAGE: " + request.args['message'])
        message = request.args['message']

    products = csvReader.get_products_list()
    return render_template('products.html', products=products, message=message)

@app.route('/daily')
def daily_tracker():

    products = csvReader.get_products_list()

    return render_template('daily.html', 
                            calories=dailyTracker.total_calories,
                            protein=dailyTracker.total_protein,
                            fats = dailyTracker.total_fats,
                            carbs = dailyTracker.total_carbs,
                            products = dailyTracker.products,
                            all_products = products,
                            max=17000, 
                            set=zip(values, labels, colors))

@app.route('/add_product', methods=['POST'])
def add_product():
    print("FORM")
    print(request.form)
    args = request.form

    new_product = Product(name=args['name'],
                          calories=args['calories'],
                          protein=args['protein'],
                          fats=args['fats'],
                          carbs=args['carbs'])

    retVal = csvReader.add_new_product(new_product=new_product)
    
    message = None
    if retVal:
        message = "Successfully added product: " + args['name']
    else:
        message = "Error encountered while adding product: " + args['name']

    return redirect(url_for('get_products_list', message=message))

@app.route('/remove_product', methods=['GET', 'DELETE'])
def remove_product():
    args = request.args
    name = args['name']

    retVal = csvReader.remove_product(product_name=name)

    message = None
    if retVal:
        message = "Successfully removed product: " + name
    else:
        message = "Error encountered while removing produc: " + name

    return redirect(url_for('get_products_list', message=message))
