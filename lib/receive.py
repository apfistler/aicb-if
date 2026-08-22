from pathlib import Path

from .context import Context
from .transport import Transport


class Receiver:
  def __init__(self, transport: Transport):
    self.transport = transport

  def receive(self):
    return self.transport.receive()
