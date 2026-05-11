from flask import Flask, render_template, request
import joblib
import pandas as pd
import requests
import os

app = Flask(__name__)

# ----------------------
# Project Paths
# ----------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(BASE_DIR, "similarity_matrices")

# Genre-wise dataset and similarity matrix paths
genre_files = {
    "Bollywood": {
        "df": os.path.join(DATA_FOLDER, "bollywood_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "bollywood_similarity.pkl")
    },

    "Punjabi": {
        "df": os.path.join(DATA_FOLDER, "punjabi_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "punjabi_similarity.pkl")
    },

    "English": {
        "df": os.path.join(DATA_FOLDER, "english_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "english_similarity.pkl")
    },

    "Tollywood": {
        "df": os.path.join(DATA_FOLDER, "tollywood_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "tollywood_similarity.pkl")
    },

    "Kollywood": {
        "df": os.path.join(DATA_FOLDER, "kollywood_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "kollywood_similarity.pkl")
    },

    "Sandalwood": {
        "df": os.path.join(DATA_FOLDER, "sandalwood_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "sandalwood_similarity.pkl")
    },

    "Mollywood": {
        "df": os.path.join(DATA_FOLDER, "mollywood_df.pkl"),
        "sim": os.path.join(DATA_FOLDER, "mollywood_similarity.pkl")
    }
}


# ----------------------
# Load Dataset and Similarity Matrix
# ----------------------

def load_data(genre):

    df = joblib.load(genre_files[genre]["df"])

    sim = joblib.load(genre_files[genre]["sim"])

    # Reset dataframe index
    df = df.reset_index(drop=True)

    # Convert similarity matrix to DataFrame if needed
    if not isinstance(sim, pd.DataFrame):
        sim = pd.DataFrame(sim)

    # Match dataframe size with similarity matrix
    df = df.iloc[:sim.shape[0]]

    return df, sim


# ----------------------
# Fetch iTunes Song Link
# ----------------------

def get_itunes_link(track_name, artist_name):

    try:
        query = f"{track_name} {artist_name}"

        url = "https://itunes.apple.com/search"

        params = {
            "term": query,
            "media": "music",
            "limit": 1
        }

        response = requests.get(url, params=params)

        data = response.json()

        if data.get('resultCount', 0) > 0:
            return data['results'][0].get('trackViewUrl')

        return None

    except Exception as e:
        print(f"Error fetching iTunes link: {e}")

        return None


# ----------------------
# Recommendation Logic
# ----------------------

def recommend_songs(song_name, df, sim_matrix, top_n=5, max_per_artist=1):

    try:
        idx = df[df['Track Name'] == song_name].index[0]

    except IndexError:
        return pd.DataFrame()

    # Calculate similarity scores
    sim_scores = list(enumerate(sim_matrix.iloc[idx].values))

    # Sort songs based on similarity
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommended_indices = []

    seen_tracks = set()

    artist_count = {}

    for i, score in sim_scores:

        track = df.loc[i, 'Track Name']

        artist = df.loc[i, 'Artist(s)']

        # Skip same or duplicate songs
        if track == song_name or track in seen_tracks:
            continue

        # Get main artist name
        artist_main = artist.split(",")[0].strip()

        if artist_main not in artist_count:
            artist_count[artist_main] = 0

        # Limit songs from same artist
        if artist_count[artist_main] >= max_per_artist:
            continue

        recommended_indices.append(i)

        seen_tracks.add(track)

        artist_count[artist_main] += 1

        # Stop after required recommendations
        if len(recommended_indices) >= top_n:
            break

    if len(recommended_indices) == 0:
        return pd.DataFrame()

    recommendations = df.loc[
        recommended_indices,
        ['Track Name', 'Artist(s)', 'Cover Image']
    ].copy()

    # Add iTunes links
    recommendations['iTunes Link'] = recommendations.apply(
        lambda x: get_itunes_link(
            x['Track Name'],
            x['Artist(s)']
        ),
        axis=1
    )

    return recommendations


# ----------------------
# Routes
# ----------------------

# Landing Page
@app.route('/')
def home():

    return render_template('index.html')


# Genre Selection Form
@app.route('/form')
def form():

    return render_template(
        'form.html',
        genres=list(genre_files.keys())
    )


# Load Songs Based on Genre
@app.route('/songs', methods=['POST'])
def songs():

    genre = request.form.get('genre')

    df, _ = load_data(genre)

    songs_list = df['Track Name'].tolist()

    return render_template(
        'form.html',
        genres=list(genre_files.keys()),
        selected_genre=genre,
        songs=songs_list
    )


# Generate Recommendations
@app.route('/recommend', methods=['POST'])
def recommend():

    genre = request.form.get('genre')

    selected_song = request.form.get('song')

    df, sim = load_data(genre)

    recommendations = recommend_songs(
        selected_song,
        df,
        sim
    )

    return render_template(
        'result.html',
        selected_song=selected_song,
        recommendations=recommendations.to_dict(orient='records')
    )


# ----------------------
# Run Flask App
# ----------------------

if __name__ == '__main__':
    app.run(debug=True)