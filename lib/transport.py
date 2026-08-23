from pathlib import Path
import subprocess
import tempfile


class Transport:
  def send(self, content, filename):
    raise NotImplementedError

  def receive(self, filename):
    raise NotImplementedError

  def list(self):
    raise NotImplementedError

  def remove(self, filename):
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
      source_path.unlink(
        missing_ok=True
      )

  def receive(self, filename):
    self.context_path.mkdir(
      parents=True,
      exist_ok=True
    )

    source = (
      f"{self.user}@{self.host}:"
      f"{self.context_path}/{filename}"
    )

    destination = (
      self.context_path / filename
    )

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

    return destination.read_text(
      encoding="utf-8"
    )

  def list(self):
    result = subprocess.run(
      [
        "ssh",
        "-p",
        str(self.port),
        "-i",
        str(self.identity_file),
        f"{self.user}@{self.host}",
        f"find {self.context_path} "
        f"-maxdepth 1 "
        f"-type f "
        f"-name '*.json' "
        f"-printf '%f\\n'",
      ],
      capture_output=True,
      text=True,
      check=True,
    )

    return [
      filename
      for filename in result.stdout.splitlines()
      if filename
    ]

  def remove(self, filename):
    remote_path = (
      f"{self.context_path}/{filename}"
    )

    subprocess.run(
      [
        "ssh",
        "-p",
        str(self.port),
        "-i",
        str(self.identity_file),
        f"{self.user}@{self.host}",
        f"rm -f {remote_path}",
      ],
      check=True,
    )
