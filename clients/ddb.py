import boto3
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from boto3_type_annotations.dynamodb import Client

from models.documents import ProfileDoc, QuizDoc

class DdbClient():
  client: Client
  td: TypeDeserializer
  ts: TypeSerializer
  def __init__(self):
    self.client = boto3.client('dynamodb')
    self.td = TypeDeserializer()
    self.ts = TypeSerializer()
  
  def get_profiles(self, user_ids: list[str]) -> list[ProfileDoc]:
    profiles: list[ProfileDoc] = []
    for i in range(0, len(user_ids), 100):
      b = user_ids[i:i+100]
      keys = []
      for id in b:
        keys.append({
          'spotifyId': { 'S': id }
        })
      r = self.client.batch_get_item(
        RequestItems={
          'SpotifyProfile': {
            'Keys': keys
          }
        }
      )
      for item in r['Responses']['SpotifyProfile']:
        p = self.to_object(item)
        profiles.append(p)
    return profiles

  # def scan_profiles(self) -> list[ProfileDoc]:
  #   r = self.client.scan(TableName='SpotifyProfile')
  #   items: list[dict] = r['Items']
  #   while r.get('LastEvaluatedKey'):
  #     r = self.client.scan(
  #       TableName='SpotifyProfile',
  #       ExclusiveStartKey=r['LastEvaluatedKey'],
  #     )
  #     items.extend(r['Items'])
  #   return [self.to_object(i) for i in items]

  def query_quizzes(self, quizType: str) -> list[QuizDoc]:
    r = self.client.query(
      TableName='SpotifyQuiz',
      KeyConditionExpression='#quizType = :quizType',
      ExpressionAttributeNames={ '#quizType': 'quizType' },
      ExpressionAttributeValues={ ':quizType': { 'S': quizType } },
    )
    items: list[dict] = r['Items']
    while r.get('LastEvaluatedKey'):
      r = self.client.query(
        TableName='SpotifyQuiz',
        ExclusiveStartKey=r['LastEvaluatedKey'],
        KeyConditionExpression='n_quizType = v_quizType',
        ExpressionAttributeNames={ 'n_quizType': 'quizType' },
        ExpressionAttributeValues={ 'v_quizType': { 'S': quizType } },
      )
      items.extend(r['Items'])
    return [self.to_object(i) for i in items]

  def put_quiz(self, quiz: QuizDoc):
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