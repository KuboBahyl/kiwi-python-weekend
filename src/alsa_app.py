from flask import Flask, request, jsonify, render_template
from alsa_connections import search_results
from templates import *


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/')
def home_page():
    return render_template('index.html', welcome='Welcome to', name='Alsa search')


@app.route('/ping')
def ping():
    return render_template('index.html', welcome='Pong', name=':-)')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # inputs
    user_dep = request.form.get('source')
    user_dest = request.form.get('destination')
    user_time_dep = request.form.get('date_from', default='09-12-2018')  # MM-DD-YYYY
    user_passengers = request.form.get('passengers', 1)
    print(user_dep, user_dest, user_time_dep, user_passengers)

    results = search_results(user_dep, user_dest, user_time_dep, user_passengers)
    colNames = list(results[0].keys())
    print(colNames)

    return render_template('results.html', results=results, colnames=colNames)
    # return jsonify(results)



if __name__ == '__main__':
   app.run()
   #http://127.0.0.1:5000/search?src=Madrid+(All+stops)&dst=Barcelona+(All+stops)&date_from=09-20-2018&passengers=2

