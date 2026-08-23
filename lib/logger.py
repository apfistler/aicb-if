from datetime import datetime
from pathlib import Path


class Logger:
  def __init__(self, log_dir):
    self.log_dir = Path(log_dir)

    self.log_dir.mkdir(
      parents=True,
      exist_ok=True
    )

  def write(self, message):
    now = datetime.now().astimezone()

    filename = (
      f"aicb."
      f"{now.strftime('%Y-%m-%d')}"
      f".log"
    )

    logfile = self.log_dir / filename

    line = (
      f"[{now.isoformat()}] "
      f"{message}"
    )

    with logfile.open(
      "a",
      encoding="utf-8"
    ) as f:
      f.write(line)
      f.write("\n")

  def info(self, message):
    self.write(
      f"INFO: {message}"
    )

  def error(self, message):
    self.write(
      f"ERROR: {message}"
    )
