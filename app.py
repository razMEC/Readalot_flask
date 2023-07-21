from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '85a5f518e96640cf97b232de853e03ff7522c2373a403955'

book_details =[{
        "name": "How to win friends and Influence people",
        "author": "Dale carnegie",
        "review": "Ah kollaam.. nallatha",
        "summary": "Lorem ipsum dolor silit"
    },
    ]
books_requested = []
name = ""

@app.route('/', methods=('GET','POST'))
def landing():

    return render_template('landing.html')

@app.route('/review', methods=('GET','POST'))
def review():
            name = "xyz"
            if request.method == 'POST':
                name = request.form['name_book']
                return render_template('review.html', data= book_details, name_requested=name)

            # if name == "":
            #     flash('Please enter a name!')
            else:
                # books_requested.append({'name': name})
                return render_template('landing.html')
            # return render_template('review.html', data= book_details, name_requested=name)

@app.route('/summary', methods =('GET', 'POST'))
def summary():
            name = "xyz"
            if request.method == 'POST':
                name = request.form['name_book']
                return render_template('summary.html', data= book_details, name_requested=name)

            # if name == "":
            #     flash('Please enter a name!')
            else:
                # books_requested.append({'name': name})
                return render_template('landing.html')
            # return render_template('review.html', data= book_details, name_requested=name)

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html', data= book_details)

if __name__ == "__main__":
    app.run(debug = True)

