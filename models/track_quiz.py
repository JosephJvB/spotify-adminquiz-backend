from profile import Profile
from uuid import uuid4
from clients.helpers import now_ts
from models.quiz import Question, Quiz, QuizResponse


class TrackQuiz():
  ts: str
  questions: list[Question]
  responses: list[QuizResponse]
  profiles: list[Profile]
  past_quizzes: list[Quiz]
  def __init__(self, profiles: list[Profile], past_quizzes: list[Quiz]):
    self.id = uuid4()
    self.ts = now_ts()
    self.questions = []
    self.responses = []
    self.profiles = profiles
    self.past_quizzes = past_quizzes

  @property
  def json(self):
    return {
      'quizId': self.id,
      'quizType': 'track',
      'ts': self.ts,
      'questions': self.questions,
      'responses': self.responses,
    }