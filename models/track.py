from models.spotify import SpotifyTrack


class Track():
  id: str
  albumImageUrl: str
  albumName: str
  releaseDate: str
  artists: list[str]
  name: str
  popularity: int
  previewUrl: str
  uri: str
  def __init__(self, data: SpotifyTrack):
    self.id = data['id']
    self.albumImageUrl = next((a.get('url') for a in data['album']['images']), None)
    self.albumName = data['album']['name']
    self.releaseDate = data['album']['release_date']
    self.artists = [a['name'] for a in data['artists']]
    self.name = data['name']
    self.popularity = data['popularity']
    self.previewUrl = data['preview_url']
    self.uri = data['uri']