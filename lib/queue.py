from pathlib import Path
import json
import time


class MessageQueue:
  def __init__(
    self,
    path="/tmp/chatgpt-context",
    interval=2
  ):
    self.path = Path(path)
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

      if files:
        filename = files[0]

        try:
          message = json.loads(
            filename.read_text(
              encoding="utf-8"
            )
          )
        finally:
          filename.unlink(
            missing_ok=True
          )

        return message

      time.sleep(self.interval)
