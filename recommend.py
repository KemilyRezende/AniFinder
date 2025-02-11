from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app) 

def find_closest_anime(title, df_cleaned):
        matches = df_cleaned[df_cleaned["Title"].str.contains(title, case=False, na=False)]
        if not matches.empty:
            return matches.iloc[0]["Title"]
        return None

def recommend_by_cluster(anime_title,df_cleaned, num_recommendations=5):
        anime_title = find_closest_anime(anime_title, df_cleaned)
    
        if anime_title is None:
            return f"Anime '{anime_title}' não encontrado na base de dados."

        cluster_id = df_cleaned.loc[df_cleaned["Title"] == anime_title, "Cluster"].values[0]
        similar_animes = df_cleaned[df_cleaned["Cluster"] == cluster_id].sample(
            n=min(num_recommendations, len(df_cleaned[df_cleaned["Cluster"] == cluster_id])),
            random_state=42
        )

        return similar_animes["Title"].tolist()


@app.route('/anifinder', methods=['POST'])
def recommend():
    data = request.json

    anime_name = (data['name'])

    csv_filename = "/home/kemily/Desktop/Engenharia/Ciencia de Dados/AniFinder/data/anilist_genres_years.csv"

    df = pd.read_csv(csv_filename)

    df_cleaned = df.dropna()
    df_cleaned.head()

    df_cleaned = df_cleaned.copy()
    df_cleaned["Genres"] = df_cleaned["Genres"].fillna("")
    df_cleaned["Genres_Combined"] = df_cleaned.groupby("Title")["Genres"].transform(lambda x: " ".join(x))
    df_cleaned = df_cleaned.drop_duplicates(subset=["Title", "Genres_Combined"]).reset_index(drop=True)

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df_cleaned["Genres_Combined"])

    num_clusters = 18
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    df_cleaned["Cluster"] = kmeans.fit_predict(tfidf_matrix)

    recommended_animes_by_cluster = recommend_by_cluster(anime_name, df_cleaned, num_recommendations=10)

    print(f"Animes similares a '{anime_name}':")
    for anime in recommended_animes_by_cluster:
        print(f"- {anime}")

    return jsonify({
        'list': recommended_animes_by_cluster
    })

if __name__ == '__main__':
    app.run(port=5011, debug=True)