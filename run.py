from app import app
from flask_migrate import upgrade

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

with app.app_context():
    upgrade()
