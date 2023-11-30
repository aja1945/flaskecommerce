from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

products = [
    {"id": 1, "name": "Product 1", "price": 20.0},
    {"id": 2, "name": "Product 2", "price": 30.0},
    {"id": 3, "name": "Product 3", "price": 25.0},
]

users = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"},
]

user_cart = []


@app.route('/')
def index():
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    else:
        flash('Product not found', 'error')
        return redirect(url_for('index'))


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        flash('Please log in to add products to your cart', 'error')
        return redirect(url_for('index'))

    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        user_cart.append(product)
        flash('Product added to your cart', 'success')
    else:
        flash('Product not found', 'error')

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    return render_template('cart.html', cart=user_cart)


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    user_cart.clear()
    flash('Cart cleared', 'success')
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    product = next((p for p in user_cart if p['id'] == product_id), None)
    if product:
        user_cart.remove(product)
        flash('Product removed from your cart', 'success')
    else:
        flash('Product not found in your cart', 'error')

    return redirect(url_for('cart'))


if __name__ == '__main__':
    app.run(debug=True)
