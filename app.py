from flask_bootstrap import Bootstrap4
from flask import Flask, render_template
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
