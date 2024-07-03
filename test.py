import pytest
from app import app, load_songs


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200, "Index page should load successfully."
    assert b"Playlist" in response.data, "Index page should contain 'Playlist'."


def test_add_song(client):
    new_song = {
        'title': 'New Song',
        'artist': 'New Artist',
        'youtube_url': 'https://youtube.com/new_song',
        'cover_url': 'https://example.com/new_cover.jpg'
    }
    response = client.post('/add', data=new_song, follow_redirects=True)
    assert response.status_code == 200, "Adding a song should redirect to the index page."

    songs = load_songs()
    assert any(song['title'] == 'New Song' for song in songs), "The new song should be present in the songs list."


def test_edit_song(client):
    new_song = {
        'title': 'Song to Edit',
        'artist': 'Artist to Edit',
        'youtube_url': 'https://youtube.com/edit_song',
        'cover_url': 'https://example.com/edit_cover.jpg'
    }
    client.post('/add', data=new_song, follow_redirects=True)

    songs = load_songs()
    song_id = len(songs) - 1

    updated_song = {
        'title': 'Updated Song',
        'artist': 'Updated Artist',
        'youtube_url': 'https://youtube.com/updated_song',
        'cover_url': 'https://example.com/updated_cover.jpg'
    }
    response = client.post(f'/edit/{song_id}', data=updated_song, follow_redirects=True)
    assert response.status_code == 200, "Editing a song should redirect to the index page."

    songs = load_songs()
    assert any(song['title'] == 'Updated Song' for song in
               songs), "The edited song should be present in the songs list with updated details."
