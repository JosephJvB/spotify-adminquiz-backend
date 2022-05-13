import logging
import json
from random import randint, shuffle
from models.profile import LoadedProfile
from uuid import uuid4
from clients.ddb import DdbClient
from clients.helpers import now_ts, run_io_tasks_in_parallel
from clients.spotify import SpotifyClient
from models.quiz import Quiz, TrackQuiz, TrackQuizResponse, TrackAnswer, TrackQuestion
from models.spotify import SpotifyTrack

class TrackQuizService():
  # json properties
  id: str
  ts: int
  questions: dict[str, TrackQuestion]
  responses: list[TrackQuizResponse]
  # data properties used to generate quiz
  profiles: list[LoadedProfile]
  past_questions: dict[str, TrackQuiz]
  num_choices: int = 4
  num_questions: int = 20
  # clients
  ddb: DdbClient
  spotify: SpotifyClient
  def __init__(self, ddb: DdbClient, spotify: SpotifyClient):
    self.id = str(uuid4())
    self.ts = now_ts()
    self.questions = {}
    self.responses = []
    self.profiles = []
    self.past_questions = {}
    self.ddb = ddb
    self.spotify = spotify

  def load_data(self):
    data = run_io_tasks_in_parallel([
      lambda: self.ddb.scan_profiles(),
      lambda: self.ddb.scan_quizzes('track'),
    ])

    profiles: list[LoadedProfile] = data[0]
    past_quizzes: list[TrackQuiz] = data[1]
    shuffle(profiles) # make sure profiles are not added in same order every quiz

    for quiz in past_quizzes:
      for question in quiz['questions']:
        k = f"{question['subject']['id']}__{question['answer']['spotifyId']}"
        self.past_questions[k] = question

    for p in profiles:
      token = json.loads(p['tokenJson'])
      p['tracks'] = self.spotify.load_tracks(token, 'short_term', 30, 0)
    self.profiles: list[LoadedProfile] = [p for p in profiles if len(p['tracks']) > 0]
    if len(self.profiles) < 4:
      self.num_choices = len(self.profiles)

  def generate_quiz(self):
    while len(self.questions.keys()) < self.num_questions:
      for p in self.profiles:
        self.add_question(p)

  def add_question(self, profile: LoadedProfile):
    ans: TrackAnswer = {
      'spotifyId': profile['spotifyId'],
      'spotifyDisplayPicture': profile.get('displayPicture'),
      'spotifyDisplayName': profile.get('displayName'),
    }
    track: SpotifyTrack = None
    for t in profile['tracks']:
      k = f"{t['id']}__{profile['spotifyId']}"
      if not self.questions.get(t['id']) and not self.past_questions.get(k):
        track = t
    if track is None:
      opts = [t for t in profile['tracks'] if not self.questions.get(t['id'])]
      if len(opts) > 0:
        track = opts[randint(0, len(opts) - 1)]
  
    choices: dict[str, TrackAnswer] = {}
    choices[profile['spotifyId']] = ans
    i = 0
    while len(choices.keys()) < self.num_choices:
      i += 1
      opts = [p for p in self.profiles if not choices.get(p['spotifyId'])]
      choice = opts[randint(0, len(opts) - 1)]
      if choice:
        choices[choice['spotifyId']] = {}
        choices[choice['spotifyId']]['spotifyId'] = choice['spotifyId']
        choices[choice['spotifyId']]['spotifyDisplayName'] = choice.get('displayName')
        choices[choice['spotifyId']]['spotifyDisplayPicture'] = choice.get('displayPicture')
      if i == 50: # while loops scare me a bit
        break

    next_question: TrackQuestion = {}
    next_question['id'] = str(uuid4())
    next_question['answer'] = ans
    next_question['choices'] = list(choices.values())
    next_question['subject'] = track
    shuffle(next_question['choices'])
    self.questions[track['id']] = next_question


  @property
  def to_ddb(self) -> Quiz:
    logger = logging.getLogger()
    logger.info('huh')
    logger.info(self.questions)
    questions = list(self.questions.values())
    logger.info(questions)
    logger.info(len(questions))
    shuffle(questions)
    logger.info(questions)
    logger.info(len(questions))
    return {
      'quizId': self.id,
      'quizType': 'track',
      'ts': self.ts,
      'questions': json.dumps(questions),
      'responses': json.dumps(self.responses),
    }