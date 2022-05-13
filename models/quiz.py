from models.profile import Profile
from typing import TypedDict
from models.spotify import SpotifyArtistTrim, SpotifyTrack

# base quiz data
class Question(TypedDict):
  id: str
  subject: dict[str, str]
  choices: list[dict[str, str]]
  answer: dict[str, str]
class QuizResponse(TypedDict):
  spotifyId: str
  answers: list[Question]
  score: int
class Quiz(TypedDict):
  id: str
  ts: int
  type: str
  questions: list[Question]
  responses: list[QuizResponse]

# track quiz data
class TrackAnswer(TypedDict):
  spotifyId: str
  spotifyDisplayName: str
  spotifyDisplayPicture: str
class TrackQuestion(Question):
  subject: SpotifyTrack
  answer: TrackAnswer
  choices: list[TrackAnswer]
class TrackQuizResponse(QuizResponse):
  answers: list[TrackQuestion]
class TrackQuiz(Quiz):
  id: str
  ts: int
  questions: list[TrackQuestion]
  responses: list[QuizResponse]


# wip festy quiz
class Festy(TypedDict):
  friday: list[SpotifyArtistTrim]
  saturday: list[SpotifyArtistTrim]
  sunday: list[SpotifyArtistTrim]
class FestyQuestion(Question):
  subject: Festy
