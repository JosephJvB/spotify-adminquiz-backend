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
    r = self.client.scan(TableName='SpotifyProfile')
    items: list[dict] = r['Items']
    while r.get('LastEvaluatedKey'):
      r = self.client.scan(
        TableName='SpotifyProfile',
        ExclusiveStartKey=r['LastEvaluatedKey'],
      )
      items.extend(r['Items'])
    return [self.to_document(i) for i in items]

  def scan_quizzes(self, quizType: str) -> list[Quiz]:
    r = self.client.scan(
      TableName='SpotifyProfile',
      FilterExpression='n_quizType=v_quizType',
      ExpressionAttributeNames={ 'n_quizType': 'quizType' },
      ExpressionAttributeValues={ 'v_quizType': { 'S': quizType } },
    )
    items: list[dict] = r['Items']
    while r.get('LastEvaluatedKey'):
      r = self.client.scan(
        TableName='SpotifyProfile',
        ExclusiveStartKey=r['LastEvaluatedKey'],
        FilterExpression='n_quizType=v_quizType',
        ExpressionAttributeNames={ 'n_quizType': 'quizType' },
        ExpressionAttributeValues={ 'v_quizType': { 'S': quizType } },
      )
      items.extend(r['Items'])
    return [self.to_document(i) for i in items]

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