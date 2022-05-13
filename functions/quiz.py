import logging
import json
import traceback
from aws_lambda_typing import context as context_, events, responses
from clients.ddb import DdbClient
from clients.helpers import run_io_tasks_in_parallel
from clients.spotify import SpotifyClient
from models.http import HttpFailure, HttpSuccess
from models.track_quiz import TrackQuiz

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ddb = DdbClient()
spotify = SpotifyClient()

def handler(event: events.APIGatewayProxyEventV1, context: context_.Context)-> responses.APIGatewayProxyResponseV1:
  try:
    logger.info('method ' + event['httpMethod'])
    if event['httpMethod'] == 'OPTIONS':
      return HttpSuccess()

    # generate different quiz types...
    quiz_type = event['queryStringParameters'].get('type')
    docs = run_io_tasks_in_parallel([
      lambda: ddb.scan_profiles(),
      lambda: ddb.scan_quizzes(quiz_type),
    ])
    q = {
      'track': TrackQuiz
    }[quiz_type](*docs)

    ddb.put_quiz(q)

    return HttpSuccess(json.dumps({
      'message': 'generate quiz success',
    }))

  except Exception:
    tb = traceback.format_exc()
    logger.error(tb)
    logger.error('handler failed')
    return HttpFailure(500, tb)