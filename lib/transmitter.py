import json
from datetime import datetime
from uuid import uuid4


class Transmitter:
  def __init__(self, transport):
    self.transport = transport

  def transmit(self, message):
    filename = (
      f"{message.type}-"
      f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-"
      f"{uuid4().hex[:8]}.json"
    )

    data = json.dumps(
      message.to_dict(),
      indent=2
    )

    self.transport.send(
      data,
      filename
    )

    return filename
