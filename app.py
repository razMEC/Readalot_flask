from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def landing():
    
    return render_template('landing.html')

@app.route('/review')
def review():
    book_details ={
        "name": "How to win friends and Influence people",
        "author": "Dale carnegie",
        "review": "Ah kollaam.. nallatha",
        "summary": "Lorem ipsum dolor silit"
    }
    return render_template('review.html', data= book_details)

@app.route('/summary')
def summary():
    book_details ={
        "name": "How to win friends and Influence people",
        "author": "Dale carnegie",
        "review": "Ah kollaam.. nallatha",
        "summary": "Lorem ipsum dolor silit"
    }
    return render_template('summary.html', data= book_details)


if __name__ == "__main__":
    app.run(debug = True)

