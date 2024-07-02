from flask import Flask, render_template, request, redirect, url_for, abort
import json
import math

app = Flask(__name__)

# Lieder werden aus der JSON-file geladen
def load_songs():
    with open('songs.json', 'r') as file:
        return json.load(file)


# Lieder werden in der JSON-file gespeichert
def save_songs(songs):
    with open('songs.json', 'w') as file:
        json.dump(songs, file)


# Berechnunf der Indices der Songs (je nach Seite, auf der sie sich befinden)
def get_paginated_songs(page=0, per_page=3, query=None):
    songs = load_songs()
    if query:
        songs = [song for song in songs if
                 query.lower() in song['title'].lower() or query.lower() in song['artist'].lower()]

    start = page * per_page # Ermittlung der Indices der Songs für die jeweiligen "Seiten" --> Anpsassung über per_page einfach möglich
    end = start + per_page
    return songs[start:end]


# Berechnung der aktuellen Anzahl an Seitenzahlen
def get_total_pages(per_page=3, query=None):
    songs = load_songs()
    if query:
        songs = [song for song in songs if
                 query.lower() in song['title'].lower() or query.lower() in song['artist'].lower()]
    total_pages = math.ceil(len(songs) / per_page)
    return total_pages


@app.route('/')
def index():
    query = request.args.get('query')
    page = request.args.get('page', 0, type=int)
    per_page = 3
    total_pages = get_total_pages(per_page, query)
    songs_paginated = get_paginated_songs(page, per_page, query)

    return render_template('index.html', songs=songs_paginated, page=page, total_pages=total_pages, query=query)


@app.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        new_song = {
            'title': request.form['title'],
            'artist': request.form['artist'],
            'youtube_url': request.form['youtube_url'],
            'cover_url': request.form['cover_url']
        }
        songs = load_songs()
        songs.append(new_song)
        save_songs(songs)
        return redirect(url_for('index'))
    return render_template('add_song.html')


@app.route('/edit/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    songs = load_songs()
    if song_id < 0 or song_id >= len(songs):
        abort(404, description="Song not found")
    if request.method == 'POST':
        songs[song_id] = {
            'title': request.form['title'],
            'artist': request.form['artist'],
            'youtube_url': request.form['youtube_url'],
            'cover_url': request.form['cover_url']
        }
        save_songs(songs)
        return redirect(url_for('index'))
    song = songs[song_id]
    return render_template('edit_song.html', song=song, song_id=song_id)


@app.route('/delete/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    songs = load_songs()
    if song_id < 0 or song_id >= len(songs):
        abort(404, description="Song not found")
    del songs[song_id]
    save_songs(songs)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
