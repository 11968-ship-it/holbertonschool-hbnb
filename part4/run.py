from app import create_app, db
import sqlite3
import os

# flask app
app = create_app()

# database path
DB_PATH = os.path.join(os.path.dirname(__file__), "hbnb.db")
SEED_FILE = os.path.join(os.path.dirname(__file__), "seed.sql")

#create table and seed db
with app.app_context():
    # Create tables from SQLAlchemy models
    db.create_all()
    print("Tables created successfully.")
    
# Seed database if not already seeded
    if os.path.exists(SEED_FILE):
        conn = sqlite3.connect(DB_PATH)
        with open(SEED_FILE, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database seeded from seed.sql.")

# this here runs the flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
