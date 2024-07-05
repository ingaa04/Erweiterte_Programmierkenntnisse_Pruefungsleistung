import pytest
from app import app, load_songs

# Erstellung eines Clients für Interaktion mit Flask
@pytest.fixture
def client():
    app.config['TESTING'] = True   # Aktivierung des Testmodus
    with app.test_client() as client:
        yield client

# Überprüfung, ob Indexseite erfolgreich geladen wird
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200, "Index page should load successfully."

# Ein "neuer Song" wird testweise hinzugefügt und es wird überprüft, ob der Prozess erfolgreich verläuft
def test_add_song(client):
    new_song = {
        'title': 'New Song',
        'artist': 'New Artist',
        'youtube_url': 'https://youtube.com/new_song',
        'cover_url': 'https://example.com/new_cover.jpg'
    }
    response = client.post('/add', data=new_song, follow_redirects=True)
    assert response.status_code == 200, "Adding a song should redirect to the index page."

    # Ueberpruefung, ob der Song in der Liste gespeichert wurde
    songs = load_songs()
    assert any(song['title'] == 'New Song' for song in songs), "The new song should be present in the songs list."


# Hinzufuegen eines Songs (testweise), der bearbeitet werden soll
def test_edit_song(client):
    # Add a song to edit
    new_song = {
        'title': 'Song to Edit',
        'artist': 'Artist to Edit',
        'youtube_url': 'https://youtube.com/edit_song',
        'cover_url': 'https://example.com/edit_cover.jpg'
    }
    client.post('/add', data=new_song, follow_redirects=True)

    # ID des Songs wird ermittelt
    songs = load_songs()
    song_id = len(songs) - 1  # wir gehen davon aus, dass der Song am Ende geladen wird

    # Aktualisierung des zu bearbeitenden Songs und Speicherung
    updated_song = {
        'title': 'Updated Song',
        'artist': 'Updated Artist',
        'youtube_url': 'https://youtube.com/updated_song',
        'cover_url': 'https://example.com/updated_cover.jpg'
    }
    response = client.post(f'/edit/{song_id}', data=updated_song, follow_redirects=True)
    assert response.status_code == 200, "Editing a song should redirect to the index page."

    # Ueberpruefung, ob der Song sich in der bearbeiteten Form gespeichert hat
    songs = load_songs()
    assert any(song['title'] == 'Updated Song' for song in
               songs), "The edited song should be present in the songs list with updated details."
