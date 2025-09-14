from flask import Flask
from config import Config
from models import db
from routes.auth import auth_bp
from routes.leave import leave_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(leave_bp)

if __name__ == '__main__':
    app.run(debug=True)
