from typing import TypedDict
from models.spotify import SpotifyArtist, SpotifyTrack

class Profile(TypedDict):
  spotifyId: str
  tokenJson: str
  displayName: str
  displayPicture: str
  userAgent: str
  ipAddress: str
  lastLogin: int

class LoadedProfile(Profile):
  spotifyId: str
  tokenJson: str
  displayName: str
  displayPicture: str
  userAgent: str
  ipAddress: str
  lastLogin: int
  artists: list[SpotifyArtist]
  tracks: list[SpotifyTrack]