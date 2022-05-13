from typing import TypedDict
from models.artist import Artist

from models.track import Track

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
  artists: list[Artist]
  tracks: list[Track]