from pathlib import Path
import subprocess
import tempfile

from .context import Context


class Transport:
  def send(self, context: Context, filename: str):
    raise NotImplementedError

  def receive(self, filename: str):
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

  def send(self, context: Context, filename: str):
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
        f"{self.user}@{self.host}:"
        f"{self.context_path}/{filename}"
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

  def receive(self, filename: str):
    self.context_path.mkdir(
      parents=True,
      exist_ok=True
    )

    source = (
      f"{self.user}@{self.host}:"
      f"{self.context_path}/{filename}"
    )

    destination = self.context_path / filename

    subprocess.run(
      [
        "scp",
        "-P",
        str(self.port),
        "-i",
        str(self.identity_file),
        source,
        str(destination),
      ],
      check=True,
    )

    return Context(
      destination.read_text(encoding="utf-8")
    )
