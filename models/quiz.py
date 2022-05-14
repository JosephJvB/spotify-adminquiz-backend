from typing import Callable, TypedDict
from models.spotify import SpotifyTrack

# base quiz data
class ProfileAnswer(TypedDict):
  spotifyId: str
  spotifyDisplayName: str
  spotifyDisplayPicture: str
class Question(TypedDict):
  id: str
  subject: dict[str, str]
  choices: list[dict[str, str]]
  answer: dict[str, str]
class QuizResponse(TypedDict):
  spotifyId: str
  answers: list[Question]
  score: int
class BaseQuiz(TypedDict):
  guid: str
  quizId: str
  quizType: str
  type: str
  questions: list[Question]
  responses: list[QuizResponse]

# track quiz data
class TrackQuestion(Question):
  subject: SpotifyTrack
  answer: ProfileAnswer
  choices: list[ProfileAnswer]
class TrackQuizResponse(QuizResponse):
  answers: list[TrackQuestion]
class TrackQuiz(BaseQuiz):
  questions: list[TrackQuestion]


# wip festy quiz
class FestySubject(TypedDict):
  poster_url: str
class FestyQuestion(Question):
  subject: FestySubject
  answer: ProfileAnswer
  choices: list[ProfileAnswer]
class Festy(BaseQuiz):
  questions: list[FestyQuestion]
