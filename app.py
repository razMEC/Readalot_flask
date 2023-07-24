from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '85a5f518e96640cf97b232de853e03ff7522c2373a403955'
    
book_details =[
        {
            "name": "How to win friends and Influence people",
            "author": "Dale carnegie",
            "review": "Ah kollaam.. nallatha",
            "rating": 5.0,
            "summary": "Lorem ipsum dolor silit",
            "genre": "Self Help",
            "no_pages": 280
        },
        {
            "name": "India wins freedom",
            "author": "Maulana Abdul Kalam Azad",
            "review": "Ah kollaam.. nallatha",
            "rating": 5.0,
            "summary": "Lorem ipsum dolor silit",
            "genre": "History/Sociology",
            "no_pages": 280
        },
        {
            "name": "Zero to One",
            "author": "Peter Thiel",
            "review": "Ah kollaam.. nallatha",
            "rating": 5.0,
            "summary": "Lorem ipsum dolor silit",
            "genre": "Entrepreneurship/Business",
            "no_pages": 280
        },
        {
            "name": "Thinking Fast and Slow",
            "author": "Daniel Kahneman",
            "review": "Ah kollaam.. nallatha",
            "rating": 5.0,
            "summary": "Lorem ipsum dolor silit",
            "genre": "Psychology",
            "no_pages": 400
        }
        ]
books_requested = []
name = ""

@app.route('/', methods=('GET','POST'))
def landing():

    return render_template('landing.html')

@app.route('/review', methods=('GET','POST'))
def review():
            name = "No name entered"
            fetch_review = "Sorry, this book is not available in our database"
            fetch_rating = 0.0
            if request.method == 'POST':
                name = request.form['name_book']
                for item in book_details:
                    if (name == item["name"]):
                        fetch_review=item["review"]
                        fetch_rating=item["rating"]
                return render_template('review.html', name_requested=name, fetch_review=fetch_review, fetch_rating=fetch_rating)

            # if name == "":
            #     flash('Please enter a name!')
            else:
                # books_requested.append({'name': name})
                return render_template('landing.html')
            # return render_template('review.html', data= book_details, name_requested=name)

@app.route('/summary', methods =('GET', 'POST'))
def summary():
            name = "No name entered"
            fetch_summary = "Sorry, this book is not available in our database"
            if request.method == 'POST':
                name = request.form['name_book']
                for item in book_details:
                    if (name == item["name"]):
                        fetch_summary=item["summary"]
                return render_template('summary.html', name_requested=name, fetch_summary=fetch_summary)

            # if name == "":
            #     flash('Please enter a name!')
            else:
                # books_requested.append({'name': name})
                return render_template('landing.html')
            # return render_template('review.html', data= book_details, name_requested=name)

@app.route('/suggestions', methods= ('POST', 'GET'))
def suggestions():
    suggested_books = []
    field_of_interest=[]
    if request.method== 'POST':
        reader_speed = request.form["speed"]
        booklength_prefered = request.form["length"]
        results = request.form
        for key, value in results.items():
            if(key == "speed"):                 #INVERT THE FORM FIRST
                break
            else:
                field_of_interest.append(value)
        #Add suggestion algorithm here
        for item in book_details:
            if (item ["genre"] in field_of_interest):
                suggested_books.append(item)
    return render_template('suggestions.html',reader_speed = reader_speed, booklength_prefered=booklength_prefered, field_of_interest=field_of_interest, suggested_books=suggested_books)
                                #Remove all data sent to the suggestions page other than suggested_books list
                                #try genre with list of genre for each books
if __name__ == "__main__":
    app.run(debug = True)

