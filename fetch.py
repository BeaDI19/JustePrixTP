# fetch.py
import requests
import json
import cgi, cgitb
from flask import Flask, render_template, request
app = Flask(__name__, template_folder='./html')


@app.route('/')
def index():


#app = Flask(__name__, template_folder='.')


#@app.route('/')
#def homepage():

    params = {
        "ApiKey": "8825dcca-9426-4cc9-83f1-bb6c829bb453",
        "SearchRequest": {
            "Keyword": "tablette",
            "SortBy": "relevance",
            "Pagination": {
                "ItemsPerPage": 5,
                "PageNumber": 0
                },
            "Filters": {
                "Price": {
                    "Min": 0,
                    "Max": 1500
                    },
                "Navigation": "computers",
                "IncludeMarketPlace": "false",
                "Brands": [
                    "hp"
                    ],
                "Condition": "none"
                }
                }
                }

    r = requests.post('https://api.cdiscount.com/OpenApi/json/Search', data=json.dumps(params))

    return render_template('jeux.html', produits=json.loads(r.text)['Products'])


@app.route('/', methods=['GET', 'POST'])
def jeux():
    if request.form['estimation'] == "-1":
        estimation = float(request.form['estimation'])
        params = {
        "ApiKey": "8825dcca-9426-4cc9-83f1-bb6c829bb453",
        "ProductRequest": {
            "ProductIdList": [
                request.form['Id']
            ],
            "Scope": {
                "Offers": "false",
                "AssociatedProducts": "false",
                "Images": "false",
                "Ean": "false"
                }
                }
                }

        r = requests.post('https://api.cdiscount.com/OpenApi/json/GetProduct', data=json.dumps(params))
        product = json.loads(r.text)
        prix = product['Products']
        print(product['Products'])
        prix = float(prix)
        if prix < estimation:
            print("prix inferieur")
        elif prix > estimation:
            print("prix supérieur")
        elif prix == estimation:
            return render_template('gagne.html', produit="")
    else:
        params = {
        "ApiKey": "8825dcca-9426-4cc9-83f1-bb6c829bb453",
        "ProductRequest": {
            "ProductIdList": [
                request.form['Id']
            ],
            "Scope": {
                "Offers": "false",
                "AssociatedProducts": "false",
                "Images": "false",
                "Ean": "false"
                }
                }
                }

    r = requests.post('https://api.cdiscount.com/OpenApi/json/GetProduct', data=json.dumps(params))

    return render_template('jeux2.html', produit=json.loads(r.text)['Products'])


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

#return render_template('movies.html', movies=json.loads(r.text)['movies'])

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True)
