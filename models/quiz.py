from models.profile import Profile
from typing import TypedDict
from models.spotify import SpotifyArtistTrim

from models.track import Track


class Question(TypedDict):
  id: str
  subject: dict[str, str]
  choices: list[Profile]
  answer: Profile

class TrackQuestion(Question):
  subject: Track

class QuizResponse(TypedDict):
  spotifyId: str
  answers: list[Question]
  score: int

class Quiz(TypedDict):
  ts: str
  questions: list[Question]
  responses: list[QuizResponse]

class Festy(TypedDict):
  friday: list[SpotifyArtistTrim]
  saturday: list[SpotifyArtistTrim]
  sunday: list[SpotifyArtistTrim]
class FestyQuestion(Question):
  subject: Festy