from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, request, url_for, flash, redirect
# from prometheus_flask_exporter import PrometheusMetrics
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import re                               #import regular expression to allow case insensitive query in mongodb

# from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
# metrics = PrometheusMetrics(app)

app.config['SECRET_KEY'] = '85a5f518e96640cf97b232de853e03ff7522c2373a403955'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Readalot"
mongo = PyMongo(app)


    
# book_details =[
#         {
#             "book_id": "B2",
#             "name": "How to win friends and Influence people",
#             "author": "Dale carnegie",
#             "review": "Ah kollaam.. nallatha",
#             "rating": 5.0,
#             "summary": "Lorem ipsum dolor silit",
#             "genre": "Self Help",
#             "no_pages": 280
#         },
#         {
#             "book_id": "B1",
#             "name": "India wins freedom",
#             "author": "Maulana Abdul Kalam Azad",
#             "review": "Ah kollaam.. nallatha",
#             "rating": 5.0,
#             "summary": "Lorem ipsum dolor silit",
#             "genre": "History/Sociology",
#             "no_pages": 280
#         },
#         {
#             "book_id": "B3",
#             "name": "Zero to One",
#             "author": "Peter Thiel",
#             "review": "Ah kollaam.. nallatha",
#             "rating": 5.0,
#             "summary": "Lorem ipsum dolor silit",
#             "genre": "Entrepreneurship/Business",
#             "no_pages": 280
#         },
#         {
#             "book_id": "B4",
#             "name": "Thinking Fast and Slow",
#             "author": "Daniel Kahneman",
#             "review": "Ah kollaam.. nallatha",
#             "rating": 5.0,
#             "summary": "Lorem ipsum dolor silit",
#             "genre": "Psychology",
#             "no_pages": 400
#         }
#         ]
books_requested = []
name = ""
review_metric = {}

@app.route('/', methods=('GET','POST'))
def landing():

    return render_template('landing.html')

@app.route('/review', methods=('GET','POST'))
def review():
            name = "No name entered"
            selected_book = {}
            fetch_review = "Sorry, this book is not available in our database"
            fetch_name = "Unknown"
            fetch_rating = 0.0
            if request.method == 'POST':
                name = request.form['name_book']
                # Create a case-insensitive regular expression for the name
                name_regex = re.compile(re.escape(name), re.IGNORECASE)
                if name not in review_metric:
                     review_metric[name] = 1
                else:
                     review_metric[name] += 1
                
                selected_book = mongo.db.book_details.find_one({'_id.name': {'$regex': name_regex}}) 
                #find the book in the collection book_details with the given name (case insensitive)
                # selected_book = jsonify(selected_book_bson)
                if selected_book and selected_book.get('_id', {}).get('name'):
                    fetch_rating = selected_book['_id']['rating']
                    fetch_review = selected_book['_id']['review']
                    fetch_name = selected_book['_id']['name']

                    # for item in book_details:
                    #     if (name == item["name"]):
                    #         fetch_review=item["review"]
                    #         fetch_rating=item["rating"]
                return render_template('review.html', fetch_name=fetch_name, fetch_review=fetch_review, fetch_rating=fetch_rating)


            else:
                # books_requested.append({'name': name})
                return render_template('landing.html')
            # return render_template('review.html', data= book_details, name_requested=name)

@app.route('/summary', methods =('GET', 'POST'))
def summary():
            name = "No name entered"
            fetch_summary = "Sorry, this book is not available in our database"
            fetch_name = "Unknown"
            if request.method == 'POST':
                name = request.form['name_book']
                # Create a case-insensitive regular expression for the name
                name_regex = re.compile(re.escape(name), re.IGNORECASE)
                if name not in review_metric:
                     review_metric[name] = 1
                else:
                     review_metric[name] += 1
                
                selected_book = mongo.db.book_details.find_one({'_id.name': {'$regex': name_regex}}) 
                #find the book in the collection book_details with the given name (case insensitive)                
                # # selected_book = jsonify(selected_book_bson)
                if selected_book and selected_book.get('_id', {}).get('name'):
                    fetch_summary = selected_book['_id']['summary']
                    fetch_name = selected_book['_id']['name']

                return render_template('summary.html', fetch_name=fetch_name, fetch_summary=fetch_summary)

            else:
                # books_requested.append({'name': name})
                return render_template('landing.html')
            # return render_template('review.html', data= book_details, name_requested=name)

@app.route('/suggestions', methods= ('POST', 'GET'))
def suggestions():
    suggested_books_name = []
    suggested_books_author = []
    suggested_books_rating = []
    suggested_books_genre = []
    suggested_books_no_pages = []
    field_of_interest=[]
    if request.method== 'POST':
        reader_speed = request.form["speed"]
        booklength_prefered = request.form["length"]
        results = request.form
        for key, value in results.items():
            if(key == "speed"):                     #Speed attribute used as delimitter for 'field of interest'
                break
            else:
                field_of_interest.append(value)
        #Add suggestion algorithm here
        for genre in field_of_interest:
            selected_book = mongo.db.book_details.find_one({'_id.genre':genre})   #ONLY FINDS ONE BOOK IN EACH GENRE. CHANGE THIS SOON
            if selected_book and selected_book.get('_id', {}).get('name'):
                suggested_books_name.append(selected_book['_id']['name'])
                suggested_books_author.append(selected_book['_id']['author'])
                suggested_books_rating.append(selected_book['_id']['rating'])
                suggested_books_genre.append(selected_book['_id']['genre'])
                suggested_books_no_pages.append(selected_book['_id']['no_pages'])
            
        total_suggested_books = len(suggested_books_name)
        # for item in book_details:
        #     if (item ["genre"] in field_of_interest):
        #         suggested_books.append(item)
    return render_template('suggestions.html',reader_speed = reader_speed, booklength_prefered=booklength_prefered, field_of_interest=field_of_interest, 
                           suggested_books_name=suggested_books_name,
                           suggested_books_author=suggested_books_author,
                           suggested_books_rating=suggested_books_rating,
                           suggested_books_genre=suggested_books_genre,
                           suggested_books_no_pages=suggested_books_no_pages,
                           total_suggested_books=total_suggested_books
                           )
                                #try genre with list of genre for each books

@app.route('/metrics')
def metrics():
    metrics = ""
    for id in review_metric:
         metrics += 'review_total{product="%s"} %s\n'% (id, review_metric[id])

    metrics += 'books_total{product="%s"} %s\n'% ("Total books", len(book_details))

    return metrics


if __name__ == "__main__":
    app.run(debug = True)

