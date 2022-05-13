
from models.spotify import SpotifyArtist


class Artist():
  followers: int
  genres: list[str]
  image_url: str
  name: str
  popularity: int
  def __init__(self, data: SpotifyArtist):
    self.followers = data['followers']['total']
    self.genres = data['genres']
    self.imageUrl = next((i.get('url') for i in data['images'] if i.get('url')), None)
    self.name = data['name']
    self.popularity = data['popularity']