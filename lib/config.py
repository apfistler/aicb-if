from pathlib import Path

import yaml


class Config:
  def __init__(self, filename=None):
    if filename is None:
      filename = (
        Path(__file__).resolve().parent.parent
        / "etc"
        / "chatgpt.yaml"
      )

    self.filename = Path(filename)

    with self.filename.open("r", encoding="utf-8") as f:
      self.data = yaml.safe_load(f) or {}

  @property
  def default(self):
    return self.data.get("default")

  @property
  def conversations(self):
    return self.data.get("conversations", {})

  def get_conversation(self, name=None):
    if name is None:
      name = self.default

    if name not in self.conversations:
      raise KeyError(f"Unknown conversation: {name}")

    return self.conversations[name]

  @property
  def connections(self):
    return self.data.get("connections", {})

  def get_connection(self, name):
    if name not in self.connections:
      raise KeyError(f"Unknown connection: {name}")

    return self.connections[name]
