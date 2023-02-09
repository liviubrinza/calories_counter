from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, redirect, url_for, request
from CsvReader import CsvReader
from DailyTracker import DailyTracker

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
    products = csvReader.get_products_list()
    return render_template('products.html', products=products)

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

@app.route('/add_product', methods=['GET', 'PUT'])
def add_product():
    print("ADD ITEM ENDPOINT")
    return redirect(url_for('get_products_list'))

@app.route('/remove_product', methods=['GET', 'DELETE'])
def remove_product():
    args = request.args
    print("REMOVE ITEM ENDPOINT: " + str(args))
    return redirect(url_for('get_products_list'))
