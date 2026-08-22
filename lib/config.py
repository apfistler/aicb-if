from pathlib import Path

import yaml


class Config:
  def __init__(self, filename=None):
    if filename is None:
      filename = (
        Path(__file__).resolve().parent.parent
        / "etc"
        / "aicb.yaml"
      )

    self.filename = Path(filename)

    with self.filename.open("r", encoding="utf-8") as f:
      self.data = yaml.safe_load(f) or {}

  @property
  def default(self):
    return self.data.get("default")

  @property
  def models(self):
    return self.data.get("models", {})

  def get_model(self, name=None):
    if name is None:
      name = "chatgpt"

    if name not in self.models:
      raise KeyError(f"Unknown model: {name}")

    return self.models[name]

  def get_conversations(self, model=None):
    model_config = self.get_model(model)

    return model_config.get("conversations", {})

  def get_conversation(self, name=None, model=None):
    if name is None:
      name = self.default

    conversations = self.get_conversations(model)

    if name not in conversations:
      raise KeyError(
        f"Unknown conversation: {name}"
      )

    return conversations[name]

  @property
  def connections(self):
    return self.data.get("connections", {})

  def get_connection(self, name):
    if name not in self.connections:
      raise KeyError(
        f"Unknown connection: {name}"
      )

    return self.connections[name]

