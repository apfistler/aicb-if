from pathlib import Path
import subprocess
import tempfile

from .context import Context


class Transport:
  def send(self, context: Context):
    raise NotImplementedError


class SCPTransport(Transport):
  def __init__(self, connection):
    self.connection = connection

    self.host = connection["host"]
    self.port = connection["port"]
    self.user = connection["user"]

    self.identity_file = Path(
      connection["identity_file"]
    ).expanduser()

    self.context_path = Path(
      connection["context_path"]
    )

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
      destination = (
        f"{self.user}@{self.host}:{self.context_path}/"
      )

      subprocess.run(
        [
          "scp",
          "-P",
          str(self.port),
          "-i",
          str(self.identity_file),
          str(source_path),
          destination,
        ],
        check=True,
      )
    finally:
      source_path.unlink(missing_ok=True)

  def receive(self):
    destination_path = self.context_path

    destination_path.mkdir(
      parents=True,
      exist_ok=True
    )

    subprocess.run(
      [
        "scp",
        "-P",
        str(self.port),
        "-i",
        str(self.identity_file),
        f"{self.user}@{self.host}:{self.context_path}/*",
        str(destination_path),
      ],
      check=True,
    )

    files = list(destination_path.glob("*.txt"))

    if not files:
      return None

    latest = max(
      files,
      key=lambda path: path.stat().st_mtime
    )

    return Context(
      latest.read_text(encoding="utf-8")
    )
