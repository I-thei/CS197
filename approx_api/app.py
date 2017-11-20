from flask import Flask
from flask import jsonify

import sys
import optparse
import time
import approx_api
import requests

app = Flask(__name__)
start = int(round(time.time()))

a = approx_api.ApproximationAPI("localhost", "ebayanihan_development",  "postgres",  "8080")
a.test()
a.connect()

@app.route("/")
def hello_world():
    return "Hello World Flask Test!"

@app.route("/get_geo_tweets/<int:collection_id>")
def get_geo_tweets(collection_id):
    return jsonify(a.get_geo_tweets(collection_id))

@app.route("/get_non_geo_tweets/<int:collection_id>")
def get_non_geo_tweets(collection_id):
    return jsonify(a.get_non_geo_tweets(collection_id))

@app.route("/get_tweet_vis_data/<int:collection_id>")
def get_tweet_vis_data(collection_id):
    return jsonify(a.get_tweet_vis_data(collection_id))

@app.route("/get_city/<float:lat>/<float:lon>")
def get_place(lat, lon):
    return jsonify(a.get_location_name(lat, lon))

@app.route("/update/<float:tweet_id>/<float:lat>/<float:lon>/<int:radius>")
def update_location(tweet_id, lat, lng, radius):
    return a.update_location(tweet_id, lat, lng, radius)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python3 app.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='127.0.0.1', port=int(args.port), debug=False)