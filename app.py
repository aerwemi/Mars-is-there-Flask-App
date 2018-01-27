from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrapeMar

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    marsScrape = mongo.db.marsScrape.find_one()
    return render_template("index.html", marsScrape=marsScrape)


@app.route("/scrape")
def scrape():
    marsScrape = mongo.db.marsScrape
    marsScrape_data = scrapeMar.scrape()
    marsScrape.update(
        {},
        marsScrape_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
