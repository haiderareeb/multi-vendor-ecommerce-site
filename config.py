import os

class Config:
    SECRET_KEY = 'hello123'
    # Update with the credentials we just created
    SQLALCHEMY_DATABASE_URI = 'mysql://ecommerce_user:password123@localhost/ecommerce_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('app', 'static', 'product_images')