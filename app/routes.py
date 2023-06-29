from app import app
from analyzer import analyze
from scraper import scraping
from flask import render_template, request, send_file


@app.route('/')
def index():
    return render_template('index.html.jinja')

@app.route('/opinions', methods=['POST'])
def opinions():
    productcode = request.form['productcode']
    with open('app/static/opinions/productcode.txt', 'w+') as file:
        file.write(productcode)
        file.close()
    scraping(productcode)
    data = analyze(productcode)
    rating = data[0]
    opinions = data[1]  
    pros = data[2]
    cons = data[3]
    return render_template('opinions.html.jinja', rating=rating, opinions=opinions, pros=pros, cons=cons)

@app.route('/json', methods=['POST', 'GET'])
def json():
    with open('app/static/opinions/productcode.txt', 'r') as file:
        productcode = file.read()
    return send_file(f'static/opinions/{productcode}.json', as_attachment=True)

@app.route('/bar', methods=['POST', 'GET'])
def bar():
    with open('app/static/opinions/productcode.txt', 'r') as file:
        productcode = file.read()
    return send_file(f'static/charts/{productcode}_bar.png', as_attachment=True)

@app.route('/pie', methods=['POST', 'GET'])
def pie():
    with open('app/static/opinions/productcode.txt', 'r') as file:
        productcode = file.read()
    return send_file(f'static/charts/{productcode}_pie.png', as_attachment=True)