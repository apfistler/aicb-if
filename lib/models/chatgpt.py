from ..model import Model
from ..queue import MessageQueue
from ..protocol import Request, Response
from ..transmit import Transmitter


class ChatGPTBrowserModel(Model):
  def __init__(self, config, connection):
    self.config = config
    self.connection = connection

    send_transport = connection.transport(
      config["connections"]["send"]
    )

    self.transmitter = Transmitter(
      send_transport
    )

    self.queue = MessageQueue(
      path="/tmp/chatgpt-context",
      interval=2
    )

  def send(self, request):
    if not isinstance(request, Request):
      raise TypeError(
        "request must be a Request instance"
      )

    return self.transmitter.transmit(
      request
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
      request=request,
      content={
        "type": "text",
        "mime": "text/plain",
        "data": "HELLO FROM THE CHROMEBOOK MODEL"
      }
    )

    self.send(response)
