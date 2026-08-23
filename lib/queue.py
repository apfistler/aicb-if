from .protocol import loads


class MessageQueue:
  def __init__(self, transport):
    self.transport = transport

  def send(self, message, filename=None):
    if filename is None:
      filename = self._filename(
        message
      )

    return self.transport.send(
      message,
      filename
    )

  def receive(self):
    filenames = self.transport.list()

    if not filenames:
      return None

    filename = sorted(
      filenames
    )[0]

    data = self.transport.receive(
      filename
    )

    try:
      message = loads(data)
    except Exception:
      self.transport.remove(
        filename
      )
      raise

    self.transport.remove(
      filename
    )

    return message

  def list(self):
    return self.transport.list()

  def remove(self, filename):
    return self.transport.remove(
      filename
    )

  def _filename(self, message):
    message_type = message.get(
      "type",
      "message"
    )

    message_id = message.get(
      "id",
      "unknown"
    )

    return (
      f"{message_type}-"
      f"{message_id}.json"
      )
