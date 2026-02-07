from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

songs = pickle.load(open("songs_df.pkl", "rb"))

def recommend(song):
    try:
        recs = songs[songs['track_name'] != song][['track_name', 'artists']].sample(5)
        return recs.to_dict('records')
    except:
        return []

@app.route("/", methods=["GET", "POST"])
def home():
    song_list = songs[['track_name', 'artists']].drop_duplicates()

    recommendations = []
    selected_song = None

    if request.method == "POST":
        selected_song = request.form.get("song")

        if selected_song:
            # "Song — Artist" me se sirf song name nikalna
            selected_song = selected_song.split(" — ")[0]
            recommendations = recommend(selected_song)

    return render_template(
        "index.html",
        songs=song_list.to_dict('records'),
        selected_song=selected_song,
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)
