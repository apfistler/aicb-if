from .context import Context
from .transport import Transport


class Transmitter:
  def __init__(self, transport: Transport):
    self.transport = transport

  def transmit(self, context: Context, filename: str):
    if not isinstance(context, Context):
      raise TypeError("context must be a Context instance")

    return self.transport.send(
      context,
      filename
    )
