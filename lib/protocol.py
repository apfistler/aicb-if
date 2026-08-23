import json
from datetime import datetime, timezone
from uuid import uuid4


class Request:
  def __init__(
    self,
    content,
    model="chatgpt",
    conversation="current"
  ):
    self.type = "request"
    self.id = uuid4().hex
    self.timestamp = datetime.now(
      timezone.utc
    ).isoformat()
    self.model = model
    self.conversation = conversation
    self.content = content

  def to_dict(self):
    return {
      "type": self.type,
      "id": self.id,
      "timestamp": self.timestamp,
      "model": self.model,
      "conversation": self.conversation,
      "content": self.content,
    }


class Response:
  def __init__(
    self,
    request_id,
    content
  ):
    self.type = "response"
    self.id = uuid4().hex
    self.timestamp = datetime.now(
      timezone.utc
    ).isoformat()
    self.request_id = request_id
    self.content = content

  def to_dict(self):
    return {
      "type": self.type,
      "id": self.id,
      "timestamp": self.timestamp,
      "request_id": self.request_id,
      "content": self.content,
    }


def dumps(message):
  return json.dumps(
    message.to_dict(),
    indent=2
  )


def loads(data):
  return json.loads(data)
