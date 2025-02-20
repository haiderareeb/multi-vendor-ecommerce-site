from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Product
from app import db
import os

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
vendor = Blueprint('vendor', __name__)

# Main routes
@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', product=product)

# Auth routes
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email'],
            is_vendor=request.form.get('is_vendor', False)
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Vendor routes
@vendor.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_vendor:
        return redirect(url_for('main.home'))
    products = Product.query.filter_by(vendor_id=current_user.id).all()
    return render_template('vendor/dashboard.html', products=products)

@vendor.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_vendor:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            description=request.form['description'],
            price=float(request.form['price']),
            vendor_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('vendor.dashboard'))
    return render_template('vendor/add_product.html') 