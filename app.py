from flask import Flask, render_template
from CsvReader import CsvReader

app = Flask(__name__)

@app.route("/")
def main():
    return "<h1>Main page</h1>"

@app.route('/products')
def get_products_list():
    csvReader = CsvReader()
    products = csvReader.get_products_list()

    return render_template('products.html', products=products)
