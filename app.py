from flask import Flask, render_template, request, jsonify
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movies dataframe
with open("model/movies.pkl", "rb") as f:
    movies = pickle.load(f)

# Recreate vectors and similarity matrix
cv = CountVectorizer(
    max_features=5000,
    stop_words="english"
)

vectors = cv.fit_transform(
    movies["tags"]
).toarray()

similarity = cosine_similarity(vectors)


def recommend(movie_name):

    movie_index = movies[
        movies["title"].str.lower() ==
        movie_name.lower()
    ].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    recommendations = []

    for movie in movie_list:

        recommendations.append({
            "title": movies.iloc[movie[0]].title
        })

    return recommendations


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def get_recommendations():

    try:

        movie_name = request.json.get(
            "movie",
            ""
        )

        recommendations = recommend(
            movie_name
        )

        return jsonify({
            "success": True,
            "movies": recommendations
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "error":
            "Movie not found. Try another title."
        })


if __name__ == "__main__":
    app.run(debug=True)
