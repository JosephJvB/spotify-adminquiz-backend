from typing import TypedDict
from models.spotify import SpotifyArtist, SpotifyToken, SpotifyTrack

class ProfileDoc(TypedDict):
  spotifyId: str
  tokenJson: str
  displayName: str
  displayPicture: str
  userAgent: str
  ipAddress: str
  lastLogin: int

class QuizDoc(TypedDict):
  quizId: str
  quizType: str
  questions: str
  responses: str
  guid: str

class LoadedProfile(ProfileDoc):
  spotifyId: str
  tokenJson: SpotifyToken
  displayName: str
  displayPicture: str
  userAgent: str
  ipAddress: str
  lastLogin: int
  artists: list[SpotifyArtist]
  tracks: list[SpotifyTrack]