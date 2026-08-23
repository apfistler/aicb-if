from pathlib import Path

from .context import Context


class Queue:
  def __init__(self, path):
    self.path = Path(path)
    self.path.mkdir(
      parents=True,
      exist_ok=True
    )

  def put(self, context, filename):
    if not isinstance(context, Context):
      raise TypeError(
        "context must be a Context instance"
      )

    destination = self.path / filename

    destination.write_text(
      context.content,
      encoding="utf-8"
    )

    return filename

  def list(self):
    return sorted(
      path.name
      for path in self.path.glob(
        "context-*.txt"
      )
      if path.is_file()
    )

  def get(self, filename):
    path = self.path / filename

    return Context(
      path.read_text(
        encoding="utf-8"
      )
    )

  def remove(self, filename):
    path = self.path / filename
    path.unlink(missing_ok=True)
