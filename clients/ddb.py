import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from boto3_type_annotations.dynamodb import Client

from models.profile import Profile
from models.quiz import Quiz

class DdbClient():
  client: Client
  td: TypeDeserializer
  ts: TypeSerializer
  def __init__(self):
    self.client = boto3.client('dynamodb')
    self.td = TypeDeserializer()
    self.ts = TypeSerializer()
  
  def scan_profiles(self) -> list[Profile]:
    profiles: list[Profile] = []
    last_key = None
    while True:
      r = self.client.scan(
        TableName='SpotifyProfile',
        ExclusiveStartKey=last_key,
      )
      for i in r['Items']:
        profiles.append(self.to_document(i))
      last_key = r['LastEvaluatedKey']
      if last_key is None:
        return profiles

  def scan_quizzes(self, quizType: str) -> list[Quiz]:
    quizzes: list[Quiz] = []
    last_key = None
    while True:
      r = self.client.scan(
        TableName='SpotifyProfile',
        ExclusiveStartKey=last_key,
        FilterExpression='n_quizType=v_quizType',
        ExpressionAttributeNames={ 'n_quizType': 'quizType' },
        ExpressionAttributeValues={ 'v_quizType': { 'S': quizType } },
      )
      for i in r['Items']:
        quizzes.append(self.to_document(i))
      last_key = r['LastEvaluatedKey']
      if last_key is None:
        return quizzes

  def put_quiz(self, quiz: Quiz):
    self.client.put_item(
      TableName='SpotifyQuiz',
      Item=self.to_document(quiz)
    )

  def to_document(self, obj: dict):
    return {
      k: self.ts.serialize(v) for k, v in obj.items()
    }
  def to_object(self, item: dict):
    if not item:
      return None
    return {
      k: self.td.deserialize(item[k]) for k in item.keys()
    }