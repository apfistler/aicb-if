from pathlib import Path
import subprocess
import tempfile


class Transport:
  def send(self, content, filename):
    raise NotImplementedError


class SCPTransport(Transport):
  def __init__(
    self,
    connection,
    context_dir
  ):
    self.connection = connection

    self.host = connection["host"]
    self.port = connection["port"]
    self.user = connection["user"]

    self.identity_file = Path(
      connection["identity_file"]
    ).expanduser()

    self.context_dir = Path(
      context_dir
    ).expanduser()

  def send(self, content, filename):
    with tempfile.NamedTemporaryFile(
      mode="w",
      encoding="utf-8",
      suffix=".json",
      delete=False
    ) as f:
      f.write(content)
      source_path = Path(f.name)

    try:
      destination = (
        f"{self.user}@{self.host}:"
        f"{self.context_dir}/{filename}"
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
      source_path.unlink(
        missing_ok=True
      )
