from ..context import Context
from ..model import Model
from ..transmit import Transmitter
from ..receive import Receiver


class ChatGPTBrowserModel(Model):
  def __init__(self, config, connection):
    self.config = config

    send_transport = connection.transport(
      config["connections"]["send"]
    )

    receive_transport = connection.transport(
      config["connections"]["receive"]
    )

    self.transmitter = Transmitter(
      send_transport
    )

    self.receiver = Receiver(
      receive_transport
    )

  def send(self, context: Context):
    return self.transmitter.transmit(
      context
    )

  def receive(self):
    return self.receiver.receive()

  def process(self, context: Context):
    if not isinstance(context, Context):
      raise TypeError(
        "context must be a Context instance"
      )

    response = Context(
      content=(
        "ChatGPT browser model received:\n\n"
        + context.content
      )
    )

    self.send(response)

    return response
