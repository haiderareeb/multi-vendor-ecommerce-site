from app import create_app, db
from sqlalchemy.exc import OperationalError

app = create_app()

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True)
    except OperationalError as e:
        print("Error connecting to MySQL database:")
        print(e)
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials are correct in config.py")
        print("3. Database 'ecommerce_db' exists")