import logging
import json
import traceback
from aws_lambda_typing import context as context_, events, responses
from clients.ddb import DdbClient
from clients.spotify import SpotifyClient
from models.http import HttpFailure, HttpSuccess, CreateQuizRequest
from services.track_quiz import TrackQuizService

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ddb = DdbClient()
spotify = SpotifyClient()

def handler(event: events.APIGatewayProxyEventV1, context: context_.Context)-> responses.APIGatewayProxyResponseV1:
  try:
    logger.info('method ' + event['httpMethod'])
    if event['httpMethod'] == 'OPTIONS':
      return HttpSuccess()

    if event.get('pathParameters') is None:
      m = 'Invalid request, missing pathParameters'
      logger.warn(m)
      return HttpFailure(400, m)

    if event.get('body') is None:
      m = 'Invalid request, missing body'
      logger.warn(m)
      return HttpFailure(400, m)

    quiz_type: str = event['pathParameters'].get('type')
    req: CreateQuizRequest = json.loads(event['body'])
    user_ids = req.get('userIds')

    if user_ids is None or len(user_ids) == 0:
      m = 'Invalid request, no userIds in request'
      logger.warn(m)
      return HttpFailure(400, m)

    service = {
      'track': TrackQuizService,
    }.get(quiz_type)
    if service is None:
      m = f'Invalid request, failed to get service of type [{quiz_type}]'
      logger.warn(m)
      return HttpFailure(400, m)

    service = service(ddb, spotify)
    service.load_data(user_ids)
    service.generate_questions()
    service.save()

    return HttpSuccess(json.dumps({
      'message': f'generate [{quiz_type}] quiz success',
    }))

  except Exception:
    tb = traceback.format_exc()
    logger.error(tb)
    logger.error('handler failed')
    return HttpFailure(500, tb)