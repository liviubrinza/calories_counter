from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, redirect, url_for, request
from CsvReader import CsvReader

app = Flask(__name__)

bootstrap = Bootstrap4(app)

@app.route("/")
def main():
    return render_template('main.html')

@app.route('/products')
def get_products_list():
    csvReader = CsvReader()
    products = csvReader.get_products_list()

    return render_template('products.html', products=products)

@app.route('/daily')
def daily_tracker():
    return render_template('daily.html')


@app.route('/add_product', methods=['GET', 'PUT'])
def add_product():
    print("ADD ITEM ENDPOINT")
    return redirect(url_for('get_products_list'))

@app.route('/remove_product', methods=['GET', 'DELETE'])
def remove_product():
    args = request.args
    print("REMOVE ITEM ENDPOINT: " + str(args))
    return redirect(url_for('get_products_list'))
