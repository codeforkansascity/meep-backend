from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://meep:meep@localhost:3306/meep_dev'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return '<h1>MEEP!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
