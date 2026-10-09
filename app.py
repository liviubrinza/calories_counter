from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, redirect, url_for, request, abort
from ProductsHandler import ProductsHandler
from DailyTracker import DailyTracker
from DishesHandler import DishesHandler
from Product import Product

app = Flask(__name__)

bootstrap = Bootstrap4(app)

productsHandler = ProductsHandler()
dishesHandler = DishesHandler(productsHandler=productsHandler)

dTracker_Titi = DailyTracker(productsHandler=productsHandler, username="titi", dishesHandler=dishesHandler)
dTracker_Inci = DailyTracker(productsHandler=productsHandler, username="inci", dishesHandler=dishesHandler)

trackers = {"Titi": dTracker_Titi, "Inci": dTracker_Inci}

def get_tracker_for_user(user_name):
    tracker = trackers.get(user_name)
    if tracker is None:
        abort(404)
    return tracker

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
            
    products = productsHandler.get_products_list()
    return render_template('products.html', 
                           products=products, 
                           success_message=success_message,
                           error_message=error_message)

@app.route('/add_product', methods=['POST'])
def add_product():
    args = request.form

    if productsHandler.get_product_by_name(args['product-name']) or dishesHandler.get_dish_by_name(args['product-name']):
        error_message = "A product or dish with this name already exists: " + args['product-name']
        return redirect(url_for('get_products_list', error_message=error_message))

    new_product = Product(name=args['product-name'],
                          calories=args['product-calories'],
                          protein=args['product-protein'],
                          fats=args['product-fats'],
                          carbs=args['product-carbs'])

    retVal = productsHandler.add_new_product(new_product=new_product)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully added product: " + args['product-name']
    else:
        error_message = "Error encountered while adding product: " + args['product-name']

    return redirect(url_for('get_products_list', success_message=success_message, error_message=error_message))

@app.route('/remove_product', methods=['GET', 'DELETE'])
def remove_product():
    args = request.args
    name = args['name']

    retVal = productsHandler.remove_product(product_name=name)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully removed product: " + args['name']
    else:
        error_message = "Error encountered while removing product: " + args['name']

    return redirect(url_for('get_products_list', success_message=success_message, error_message=error_message))

@app.route('/change_product', methods=['POST'])
def change_product():
    args = request.form
    changed_product = Product(name=args['product-name'],
                              calories=args['product-calories'],
                              protein=args['product-protein'],
                              fats=args['product-fats'],
                              carbs=args['product-carbs'])
    
    retVal = productsHandler.change_product(changed_product=changed_product)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully updated product: " + changed_product.name
    else:
        error_message = "Product not found for update: " + changed_product.name

    return redirect(url_for('get_products_list', success_message=success_message, error_message=error_message))

@app.route('/daily')
def daily_tracker():

    user = request.args['user']

    tracker_instance = get_tracker_for_user(user_name=user)

    products = productsHandler.get_products_list()

    success_message = None
    error_message = None

    if request.args:
     if 'success_message' in request.args.keys() and request.args['success_message'] is not None:
        success_message = request.args['success_message']
    if 'error_message' in request.args.keys() and request.args['error_message'] is not None:
        error_message = request.args['error_message']


    return render_template('daily.html',
                            user = user, 
                            calories=round(tracker_instance.total_calories, 2),
                            protein=round(tracker_instance.total_protein, 2),
                            fats = round(tracker_instance.total_fats, 2),
                            carbs = round(tracker_instance.total_carbs, 2),
                            products = tracker_instance.products,
                            all_products = products,
                            all_dishes = dishesHandler.get_dishes_list(),
                            values = tracker_instance.percentage_values,
                            labels = DailyTracker.labels,
                            colors = DailyTracker.colors,
                            success_message=success_message, 
                            error_message=error_message)

@app.route('/add_product_daily', methods=['GET', 'POST'])
def add_product_daily():
    product = None
    quantity = 0
    user = None

    if request.form:
        user = request.form.get('user')
        product = request.form.get('product')
        quantity = request.form.get('quantity')

        tracker_instance = get_tracker_for_user(user_name=user)

        tracker_instance.add_product(name=product, quantity=quantity)

    return redirect(url_for('daily_tracker', user=user))

@app.route('/remove_product_daily', methods=['GET', 'DELETE'])
def remove_product_daily():

    args = request.args
    name = args['name']
    user = args['user']

    tracker_instance = get_tracker_for_user(user_name=user)

    retVal = tracker_instance.remove_product(name=name)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully removed product: " + name
    else:
        error_message = "Error encountered while removing product: " + name

    return redirect(url_for('daily_tracker', user=user, success_message=success_message, error_message=error_message))


@app.route('/reset_day')
def reset_day():
    args = request.args
    user = args['user']

    tracker_instance = get_tracker_for_user(user_name=user)

    tracker_instance.reset_day()
    return redirect(url_for('daily_tracker', user=user))


@app.route('/adjust_product_daily', methods=['GET', 'POST'])
def adjust_product_daily():

    args = request.form

    name=args['product-name']
    quantity=args['product-quantity']
    user = args['user']

    tracker_instance = get_tracker_for_user(user_name=user)

    retVal = tracker_instance.adjust_product_quantity(name=name, quantity=quantity)
    success_message = None
    error_message = None
    
    if retVal:
        success_message = "Successfully adjusted quantity for: "+ name
    else:
        error_message = "Error encountered while adjusting quantity for: " + name

    return redirect(url_for('daily_tracker', user=user, success_message=success_message, error_message=error_message))

@app.route('/save_stats')
def save_stats():
    args = request.args
    user = args['user']

    tracker_instance = get_tracker_for_user(user_name=user)

    tracker_instance.save_daily_stats()
    return redirect(url_for('daily_tracker', user=user))

@app.route('/dishes')
def get_dishes_list():
    success_message = None
    error_message = None

    if request.args:
        if 'success_message' in request.args.keys() and request.args['success_message'] is not None:
            success_message = request.args['success_message']
        if 'error_message' in request.args.keys() and request.args['error_message'] is not None:
            error_message = request.args['error_message']

    products = productsHandler.get_products_list()
    # per 100g values, used by the page to show the dish totals while it is being built
    products_data = {product.name: {'calories': product.calories,
                                    'protein': product.protein,
                                    'fats': product.fats,
                                    'carbs': product.carbs} for product in products}

    return render_template('dishes.html',
                           dishes=dishesHandler.get_dishes_list(),
                           products=products,
                           products_data=products_data,
                           labels=DailyTracker.labels,
                           colors=DailyTracker.colors,
                           success_message=success_message,
                           error_message=error_message)

@app.route('/add_dish', methods=['POST'])
def add_dish():
    args = request.form
    name = args.get('dish-name', '').strip()
    ingredients = list(zip(args.getlist('ingredient-name'), args.getlist('ingredient-quantity')))

    error = dishesHandler.add_new_dish(name=name, ingredients=ingredients)
    success_message = None
    error_message = None

    if error:
        error_message = "Error encountered while adding dish: " + error
    else:
        success_message = "Successfully added dish: " + name

    return redirect(url_for('get_dishes_list', success_message=success_message, error_message=error_message))

@app.route('/remove_dish', methods=['GET', 'DELETE'])
def remove_dish():
    args = request.args
    name = args['name']

    retVal = dishesHandler.remove_dish(dish_name=name)
    success_message = None
    error_message = None

    if retVal:
        success_message = "Successfully removed dish: " + name
    else:
        error_message = "Error encountered while removing dish: " + name

    return redirect(url_for('get_dishes_list', success_message=success_message, error_message=error_message))

if __name__ == "__main__":
    app.run(debug=True)