from ..model import Model
from ..queue import MessageQueue
from ..protocol import Request, Response
from ..transmit import Transmitter
from ..processor import Processor


class ChatGPTBrowserModel(
  Model,
  Processor
):
  def __init__(
    self,
    config,
    connection
  ):
    self.config = config
    self.connection = connection
    self.model_name = "chatgpt"

    connections = config.get_endpoint().get(
      "connections",
      {}
    )

    context_dir = config.get_context_dir(
      model=self.model_name
    )

    send_transport = connection.transport(
      connections["send"],
      model=self.model_name
    )

    self.transmitter = Transmitter(
      send_transport
    )

    self.request_queue = MessageQueue(
      path=context_dir,
      message_type="request",
      interval=2
    )

    self.response_queue = MessageQueue(
      path=context_dir,
      message_type="response",
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
    return self.request_queue.receive()

  def wait_for_request(self):
    return self.request_queue.wait()

  def wait_for_response(
    self,
    request_id
  ):
    while True:
      response = self.response_queue.receive()

      if response is None:
        continue

      if response.get(
        "request_id"
      ) == request_id:
        return response

      print(
        f"ignoring response for "
        f"{response.get('request_id')}"
      )

  def process(self, request):
    print()
    print("=== REQUEST RECEIVED ===")
    print(
      f"id: {request['id']}"
    )
    print(
      f"model: {request['model']}"
    )
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
        "data": (
          "HELLO FROM THE CHROMEBOOK MODEL"
        )
      }
    )

    filename = self.send(
      response
    )

    print(
      f"response sent: {filename}"
    )

    return response
