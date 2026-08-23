from ..model import Model
from ..queue import MessageQueue
from ..protocol import Request, Response
from ..transmit import Transmitter


class ChatGPTBrowserModel(Model):
  def __init__(
    self,
    config,
    connection,
    connections
  ):
    self.config = config
    self.connection = connection
    self.connections = connections

    send_transport = connection.transport(
      connections["send"]
    )

    self.transmitter = Transmitter(
      send_transport
    )

    self.queue = MessageQueue(
      path="/tmp/chatgpt-context",
      message_type="request",
      interval=2
    )

  def send(self, message):
    if not isinstance(
      message,
      (Request, Response)
    ):
      raise TypeError(
        "message must be a Request or Response"
      )

    return self.transmitter.transmit(
      message
    )

  def receive(self):
    return self.queue.receive()

  def process(self, request):
    print()
    print("=== REQUEST RECEIVED ===")
    print(f"id: {request['id']}")
    print(f"model: {request['model']}")
    print(
      f"conversation: "
      f"{request['conversation']}"
    )
    print(
      f"content type: "
      f"{request['content']['type']}"
    )
    print(
      f"mime: "
      f"{request['content']['mime']}"
    )
    print(
      f"content: "
      f"{request['content']['data']}"
    )
    print("========================")
    print()

    response = Response(
      request_id=request["id"],
      content={
        "type": "text",
        "mime": "text/plain",
        "data": "HELLO FROM THE CHROMEBOOK MODEL"
      }
    )

    filename = self.send(response)

    print(
      f"response sent: {filename}"
    )

    return response

  def run(self):
    print(
      "ChatGPT browser model "
      "waiting for requests..."
    )

    while True:
      request = self.receive()

      if request is None:
        continue

      self.process(request)

  def wait_for_response(self, request_id):
    queue = MessageQueue(
      path="/tmp/chatgpt-context",
      message_type="response",
      interval=2
    )

    while True:
      response = queue.receive()

      if response is None:
        continue

      if response.get("request_id") == request_id:
        return response

      print(
        f"ignoring response for "
        f"{response.get('request_id')}"
      )
