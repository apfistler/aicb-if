import time

from .protocol import loads


class MessageQueue:
  def __init__(
    self,
    transport,
    message_type=None,
    interval=2
  ):
    self.transport = transport
    self.message_type = message_type
    self.interval = interval

  def send(
    self,
    message,
    filename=None
  ):
    if filename is None:
      filename = self._filename(
        message
      )

    return self.transport.send(
      message,
      filename
    )

  def receive(self):
    filenames = self.list()

    if not filenames:
      return None

    filename = sorted(
      filenames
    )[0]

    data = self.transport.receive(
      filename
    )

    try:
      message = loads(
        data
      )
    except Exception:
      self.transport.remove(
        filename
      )
      raise

    self.transport.remove(
      filename
    )

    return message

  def wait(self):
    while True:
      message = self.receive()

      if message is not None:
        return message

      time.sleep(
        self.interval
      )

  def list(self):
    filenames = self.transport.list()

    if self.message_type is None:
      return filenames

    prefix = (
      f"{self.message_type}-"
    )

    return [
      filename
      for filename in filenames
      if filename.startswith(prefix)
    ]

  def remove(self, filename):
    return self.transport.remove(
      filename
    )

  def _filename(self, message):
    if hasattr(
      message,
      "to_dict"
    ):
      data = message.to_dict()
    else:
      data = message

    message_type = data.get(
      "type",
      "message"
    )

    message_id = data.get(
      "id",
      "unknown"
    )

    return (
      f"{message_type}-"
      f"{message_id}.json"
    )
