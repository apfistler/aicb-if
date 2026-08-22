from .context import Context
from .transport import Transport


class Receiver:
  def __init__(self, transport: Transport):
    self.transport = transport

  def receive(self, filename: str):
    return self.transport.receive(filename)
