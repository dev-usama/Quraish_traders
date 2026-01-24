from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'productmanager/instance/product_database.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("secret_key")
print('Secret Key:', os.environ.get("secret_key"))
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)
from productstore import project1
from pdftojson import project3

app.register_blueprint(project1, url_prefix="/excel_to_db")
app.register_blueprint(project3, url_prefix="/PDF_TO_JSON")

@app.route("/")
def main_home():
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host="0.0.0.0", debug=True)
