from ..model import Model
from ..queue import MessageQueue


class ChatGPTBrowserModel(Model):
  def __init__(self, config, connection):
    self.config = config
    self.connection = connection

    self.queue = MessageQueue(
      path="/tmp/chatgpt-context",
      interval=2
    )

  def send(self, response):
    raise NotImplementedError(
      "Response sending will be implemented next"
    )

  def receive(self):
    return self.queue.receive()

  def process(self, request):
    print()
    print("=== REQUEST RECEIVED ===")
    print(f"id: {request['id']}")
    print(f"model: {request['model']}")
    print(f"conversation: {request['conversation']}")
    print(f"content type: {request['content']['type']}")
    print(f"mime: {request['content']['mime']}")
    print(f"content: {request['content']['data']}")
    print("========================")
    print()

  def run(self):
    print("ChatGPT browser model waiting for requests...")

    while True:
      request = self.receive()

      if request is None:
        continue

      self.process(request)
