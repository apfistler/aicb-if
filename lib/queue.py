from pathlib import Path
import time

from .protocol import dumps, loads


class MessageQueue:
  def __init__(
    self,
    path,
    message_type=None,
    interval=2
  ):
    self.path = Path(
      path
    ).expanduser()

    self.message_type = message_type
    self.interval = interval

    self.path.mkdir(
      parents=True,
      exist_ok=True
    )

  def send(
    self,
    message,
    filename=None
  ):
    if filename is None:
      filename = self._filename(
        message
      )

    destination = (
      self.path / filename
    )

    destination.write_text(
      dumps(message),
      encoding="utf-8"
    )

    return filename

  def receive(self):
    filenames = self.list()

    if not filenames:
      return None

    filename = sorted(
      filenames
    )[0]

    path = (
      self.path / filename
    )

    try:
      data = path.read_text(
        encoding="utf-8"
      )

      message = loads(
        data
      )

    except Exception:
      path.unlink(
        missing_ok=True
      )
      raise

    path.unlink(
      missing_ok=True
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
    pattern = "*.json"

    if self.message_type:
      pattern = (
        f"{self.message_type}-*.json"
      )

    return [
      path.name
      for path in self.path.glob(
        pattern
      )
      if path.is_file()
    ]

  def remove(self, filename):
    path = (
      self.path / filename
    )

    path.unlink(
      missing_ok=True
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
