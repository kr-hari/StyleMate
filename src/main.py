from flask import Flask
import json

from recommendations import Recommender

recommender = Recommender(primary_column='description')


app = Flask(__name__)

@app.route("/get_query_results/<query>")
def query_results(query):
    recommendation_indices, recommendation_titles = recommender.return_most_similar(query=query)
    # print(recommendations)
    return [str(i) for i in recommendation_titles]


@app.route("/")
def home():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5743)