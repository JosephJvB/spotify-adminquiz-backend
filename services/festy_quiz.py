import json
from random import randint, shuffle
from typing import Callable
from models.documents import LoadedProfile, ProfileDoc, QuizDoc
from uuid import uuid4
from clients.ddb import DdbClient
from clients.helpers import now_ts, run_io_tasks_in_parallel
from clients.spotify import SpotifyClient
from models.quiz import FestySubject, ProfileAnswer, FestyQuestion
from models.spotify import SpotifyArtist

class FestyQuizService():
  # clients
  ddb: DdbClient
  spotify: SpotifyClient
  # data
  questions: dict[str, FestyQuestion]
  profiles: list[LoadedProfile]
  past_questions: dict[str, FestyQuestion]
  last_quiz: QuizDoc
  # settings
  num_choices: int = 4
  num_questions: int = 20

  def __init__(self, ddb: DdbClient, spotify: SpotifyClient):
    self.questions = {}
    self.profiles = []
    self.past_questions = {}
    self.ddb = ddb
    self.spotify = spotify
    self.last_quiz = None

  def unload(self):
    self.questions = {}
    self.profiles = []
    self.past_questions = {}
    self.last_quiz = None

  def load_data(self, user_ids: list[str]):
    data = run_io_tasks_in_parallel([
      lambda: self.ddb.get_profiles(user_ids),
      lambda: self.ddb.query_quizzes('festy'),
    ])

    profiles: list[ProfileDoc] = data[0]
    past_quizzes: list[QuizDoc] = data[1]
    shuffle(profiles) # make sure profiles are not added in same order every quiz

    for quiz in past_quizzes:
      if quiz['quizId'] == 'current':
        self.last_quiz = quiz
      questions: list[FestyQuestion] = json.loads(quiz['questions'])
      for question in questions:
        for day in ['friday', 'saturday', 'sunday']:
          for artist in question['subject'][day]:
            k = f"{artist}__{question['answer']['spotifyId']}"
            self.past_questions[k] = True

    for p in profiles:
      p['tokenJson'] = json.loads(p['tokenJson'])
      p['tracks'] = []
      p['artists'] = self.spotify.load_artists(p['tokenJson'], 'long_term', 50, 0)
    self.profiles: list[LoadedProfile] = [p for p in profiles if len(p['arists']) > 0]
    if len(self.profiles) < 4:
      self.num_choices = len(self.profiles)

  def generate_questions(self):
    for p in self.profiles:
      self.add_question(p)

  def save(self):
    tasks: list[Callable] = []
    if self.last_quiz is not None:
      self.last_quiz['quizId'] = self.last_quiz['guid']
      tasks.append(lambda: self.ddb.put_quiz(self.last_quiz))
    questions = list(self.questions.values())
    shuffle(questions)
    next_quiz: QuizDoc = {}
    next_quiz['guid'] =  str(uuid4())
    next_quiz['quizId'] = 'current'
    next_quiz['quizType']= 'festy'
    next_quiz['ts']= now_ts()
    next_quiz['questions']= json.dumps(questions)
    tasks.append(lambda: self.ddb.put_quiz(next_quiz))
    run_io_tasks_in_parallel(tasks)
    self.unload()

  def add_question(self, profile: LoadedProfile):
    ans: ProfileAnswer = {
      'spotifyId': profile['spotifyId'],
      'spotifyDisplayPicture': profile.get('displayPicture'),
      'spotifyDisplayName': profile.get('displayName'),
    }

    # create festy lineup for profile['artists']
    # create as datamodel here and render as poster on Gatsby
    # or: create poster_url here
    festy: FestySubject = {}
    festy['poster_url'] = ''
    festy['friday'] = []
    festy['saturday'] = []
    festy['sunday'] = []
    # get 24 random artists from list
    lineup: dict[str, SpotifyArtist] = {}
    while len(lineup.keys()) < 24:
      x: SpotifyArtist = randint(0, len(profile['artists']) - 1)
      if not lineup.get(x['id']):
        lineup[x['id']] = x
    lineup: list[SpotifyArtist] = list(lineup.values())
    lineup.sort(key=lambda a: a['popularity'])
    for i in range(0, 24):
      if i % 2 == 0:
        festy['sunday'].append(lineup[i]['name'])
      elif i % 2 == 1:
        festy['saturday'].append(lineup[i]['name'])
      elif i % 2 == 2:
        festy['friday'].append(lineup[i]['name'])
  
    choices: dict[str, ProfileAnswer] = {}
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
      if i == 10: # while loops scare me a bit
        break

    next_question: FestyQuestion = {}
    next_question['id'] = str(uuid4())
    next_question['answer'] = ans
    next_question['choices'] = list(choices.values())
    next_question['subject'] = festy
    shuffle(next_question['choices'])
    self.questions[profile['spotifyId']] = next_question