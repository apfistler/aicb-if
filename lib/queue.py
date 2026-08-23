from pathlib import Path
import json
import time


class MessageQueue:
  def __init__(
    self,
    path="/tmp/chatgpt-context",
    message_type=None,
    interval=2
  ):
    self.path = Path(path)
    self.message_type = message_type
    self.interval = interval

  def receive(self):
    self.path.mkdir(
      parents=True,
      exist_ok=True
    )

    while True:
      files = sorted(
        self.path.glob("*.json")
      )

      for filename in files:
        try:
          message = json.loads(
            filename.read_text(
              encoding="utf-8"
            )
          )
        except (
          json.JSONDecodeError,
          OSError
        ):
          continue

        if (
          self.message_type is not None
          and message.get("type")
          != self.message_type
        ):
          continue

        filename.unlink(
          missing_ok=True
        )

        return message

      print(
        "waiting...",
        flush=True
      )

      time.sleep(
        self.interval
      )
