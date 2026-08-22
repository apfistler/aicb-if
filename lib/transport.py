from pathlib import Path
import subprocess
import tempfile

from .context import Context


class Transport:
  def send(self, context: Context):
    raise NotImplementedError


class SCPTransport(Transport):
  def __init__(self, destination, destination_path):
    self.destination = destination
    self.destination_path = Path(destination_path)

  def send(self, context: Context):
    if not isinstance(context, Context):
      raise TypeError("context must be a Context instance")

    with tempfile.NamedTemporaryFile(
      mode="w",
      encoding="utf-8",
      suffix=".txt",
      delete=False
    ) as f:
      f.write(context.content)
      source_path = Path(f.name)

    try:
      subprocess.run(
        [
          "scp",
          str(source_path),
          f"{self.destination}:{self.destination_path}",
        ],
        check=True,
      )
    finally:
      source_path.unlink(missing_ok=True)
