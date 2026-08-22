from datetime import datetime
from uuid import uuid4

from .context import Context
from .transport import Transport


class Transmitter:
  def __init__(self, transport: Transport):
    self.transport = transport

  def transmit(self, context: Context):
    if not isinstance(context, Context):
      raise TypeError("context must be a Context instance")

    filename = (
      f"context-"
      f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-"
      f"{uuid4().hex[:8]}.txt"
    )

    self.transport.send(
      context,
      filename
    )

    return filename
