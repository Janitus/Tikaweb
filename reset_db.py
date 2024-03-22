from app import app, db  # Ensure these are correctly imported from your Flask app

with app.app_context():
    db.drop_all()  # Drops all tables
    db.create_all()  # Recreates tables with the current model definitions
    print("Recreated all")
