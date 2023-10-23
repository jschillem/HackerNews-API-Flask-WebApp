from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class NewsItem(db.Model):
    __tablename__ = 'news_items'

    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String)
    descendants = db.Column(db.Integer)
    score = db.Column(db.Integer)
    text = db.Column(db.Text)
    time = db.Column(db.Integer)
    type = db.Column(db.String)
    url = db.Column(db.String)
    # Omitting the 'kids' field as this is not part of our project requirements

@app.route("/")
def hello():
    return "<h1>Hello yall!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
