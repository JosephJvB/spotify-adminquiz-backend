from datetime import datetime
import os
import requests
from base64 import b64encode
from clients.helpers import now_ts

from models.spotify import SpotifyArtist, SpotifyRefreshResponse, SpotifyToken, SpotifyTopItemsResponse, SpotifyTrack

class SpotifyClient:
  basic_auth = ''
  def __init__(self) -> None:
    auth_str = f"{os.environ.get('SpotifyClientId')}:{os.environ.get('SpotifyClientSecret')}"
    self.basic_auth = b64encode(auth_str.encode()).decode()

  def validate_token(self, token: SpotifyToken):
    now = now_ts()
    if now > token['ts'] + token['expires_in'] * 1000:
      refreshed = self.refresh_token(token)
      token['access_token'] = refreshed['access_token']
      token['ts'] = now
  
  def refresh_token(self, token: SpotifyToken) -> SpotifyRefreshResponse:
    r = requests.post('https://accounts.spotify.com/api/token', params={
      'grant_type': 'refresh_token',
      'refresh_token': token['refresh_token']
    }, headers={
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': f'Basic {self.basic_auth}',
    })
    r.raise_for_status()
    return r.json()

  def load_artists(self, token: SpotifyToken, range: str, limit: int, offset: int = 0) -> list[SpotifyArtist]:
    r: SpotifyTopItemsResponse = self.load_top_items(token, 'artists', limit, range, offset)
    return r['items']
  def load_tracks(self, token: SpotifyToken, range: str, limit: int, offset: int = 0) -> list[SpotifyTrack]:
    r: SpotifyTopItemsResponse = self.load_top_items(token, 'tracks', limit, range, offset)
    return r['items']

  def load_top_items(
    self,
    token: SpotifyToken,
    item_type: str,
    limit: int,
    range: str,
    offset: int,
  ) -> SpotifyTopItemsResponse:
    self.validate_token(token)
    r = requests.get(f'https://api.spotify.com/v1/me/top/{item_type}', params={
      'limit': limit,
      'offset': offset,
      'time_range': range,
    }, headers= {
      'Authorization': f'Bearer {token["access_token"]}',
    })
    r.raise_for_status()
    return r.json()
