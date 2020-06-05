# fetch.py
import requests
import json
import cgi, cgitb
import secrets
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__, template_folder='./html')
app.config["SECRET_KEY"] = "h0DWgSEjBIU7tNZQ"

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
        return render_template('jeux2.html', produits=json.loads(r.text)['Products'])
    elif request.form['estimation'] != "-1":
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
        data = json.loads(r.text)['Products']
        for info in data:
            id = info['Id']
            prix = info['BestOffer']['SalePrice']
            ImgUrl = info['MainImageUrl']
            nom = info['Name']
        #print(prix)
        if float(prix) < float(estimation):
            sdata = {'essai': 1, 'estimation': estimation}
            session["data"] = json.dumps(sdata)
            payload = {'resultat': False, 'Id': id, 'estimation': estimation, 'ImgUrl': ImgUrl, 'Name': nom}
            return render_template('jeux3.html', produit=payload)
        elif float(prix) > float(estimation):
            payload = {'resultat': True, 'Id': id, 'estimation': estimation, 'ImgUrl': ImgUrl, 'Name': nom}
            return render_template('jeux3.html', produit=payload)
        elif float(prix) == float(estimation):
            return render_template('gagne.html', produit=prix)
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
