import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("jobs.csv")

# Combine important features
df["combined"] = df["Skills"] + " " + df["Description"]

# Convert text into vectors
tfidf = TfidfVectorizer()
matrix = tfidf.fit_transform(df["combined"])

# Recommendation function
def recommend_jobs(user_input, top_n=5):
    user_vec = tfidf.transform([user_input])
    similarity = cosine_similarity(user_vec, matrix)

    scores = list(enumerate(similarity[0]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    results = []
    for i in scores[:top_n]:
        job = df.iloc[i[0]]
        results.append({
            "title": job["Job_Title"],
            "skills": job["Skills"],
            "score": round(i[1], 2)
        })

    return results