from flask import Flask, request, jsonify
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
def index():
    return '<h1>Go to <a href="/newsfeed">/newsfeed</a> to view the API</h1>'


@app.route("/newsfeed", methods=['GET'])
def NewsFeed():
    # if no argument is provided, the API will default to showing 15 items
    k = int(request.args.get('k', 15))
    news_items = NewsItem.query.limit(k).all()
    newsFeed = []

    for item in news_items:
        item_dict = {
            'id': item.id,
            'type': item.type
        }

        # Only output fields of a NewsItem if it actually exists
        if item.by is not None:
            item_dict['by'] = item.by

        if item.descendants is not None:
            item_dict['descendants'] = item.descendants

        if item.score is not None:
            item_dict['score'] = item.score

        if item.time is not None:
            item_dict['time'] = item.time

        if item.text is not None:
            item_dict['text'] = item.text

        if item.url is not None:
            item_dict['url'] = item.url

        newsFeed.append(item_dict)

    return jsonify(newsFeed)


if __name__ == "__main__":
    app.run(debug=True)
