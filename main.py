import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("movies.csv")

# Clean genres
movies['genres'] = movies['genres'].str.replace('|', ' ')

# Convert genres to vectors
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies['genres'])

# Compute similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Reset index
movies = movies.reset_index()

# Lowercase title mapping (important improvement)
movies['title_lower'] = movies['title'].str.lower()
indices = pd.Series(movies.index, index=movies['title_lower'])

# Recommendation function
def recommend(movie_name, top_n=5):
    movie_name = movie_name.lower()

    # Find matching movie (partial search)
    matches = movies[movies['title_lower'].str.contains(movie_name)]

    if matches.empty:
        return None, []

    idx = matches.index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    movie_indices = [i[0] for i in sim_scores]

    return matches.iloc[0]['title'], movies['title'].iloc[movie_indices]

# CLI loop
while True:
    movie = input("\nEnter movie name (or 'exit'): ")

    if movie.lower() == 'exit':
        break

    found_movie, results = recommend(movie)

    if found_movie is None:
        print("\n❌ Movie not found! Try something else.")
    else:
        print(f"\n🎬 Showing results for: {found_movie}")
        print("\nRecommended movies:")
        for m in results:
            print("-", m)