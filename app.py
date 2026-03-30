from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load dataset
df = pd.read_csv("jobs.csv")

def recommend_jobs(user_skills):
    user_skills = user_skills.lower()

    # Combine descriptions + user input
    data = df['Description'].str.lower().tolist()
    data.append(user_skills)

    # Convert text to vectors
    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform(data)

    # Compute similarity
    similarity = cosine_similarity(matrix[-1], matrix[:-1])

    # Rank jobs
    scores = list(enumerate(similarity[0]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Get top 5 jobs
    results = []
    for i in scores[:5]:
        results.append(df.iloc[i[0]]['Job_Title'])

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    jobs = []
    if request.method == "POST":
        skills = request.form["skills"]
        jobs = recommend_jobs(skills)
    return render_template("index.html", jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)