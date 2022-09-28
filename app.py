from flask import Flask, render_template, redirect, url_for
from flask_pymongo import flask_pymongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")   # This route tells Flask what to display when we're looking at the home page, index.html
def index():
   mars = mongo.db.mars.find_one()   # uses PyMongo to find the "mars" collection in our database
   return render_template("index.html", mars=mars)   # tells Flask to return an HTML template using an index.html file

@app.route("/scrape")   # defines the route that Flask will be using. This route will run the function beneath it
def scrape():
   mars = mongo.db.mars   # assign a new variable that points to our Mongo database
   mars_data = scraping.scrape_all()   # create a new variable to hold the newly scraped data
   mars.update_one({}, {"$set":mars_data}, upsert=True)   # update the database
   return redirect('/', code=302)   # This will navigate our page back to where we can see the updated content.

   if __name__ == "__main__":
   app.run()