from pathlib import Path
import socket

import yaml


class Config:
  def __init__(self, filename=None):
    self.base_filename = (
      Path(__file__).resolve().parent.parent
      / "etc"
      / "aicb.yaml"
    )

    if filename is None:
      hostname = socket.gethostname()

      self.local_filename = (
        self.base_filename.parent
        / f"aicb.{hostname}.yaml"
      )
    else:
      self.local_filename = Path(filename)

    self.data = self._load()

  def _load_yaml(self, filename):
    if not filename.exists():
      return {}

    with filename.open(
      "r",
      encoding="utf-8"
    ) as f:
      return yaml.safe_load(f) or {}

  def _merge(self, base, override):
    result = dict(base)

    for key, value in override.items():
      if (
        key in result
        and isinstance(result[key], dict)
        and isinstance(value, dict)
      ):
        result[key] = self._merge(
          result[key],
          value
        )
      else:
        result[key] = value

    return result

  def _load(self):
    base = self._load_yaml(
      self.base_filename
    )

    local = self._load_yaml(
      self.local_filename
    )

    return self._merge(
      base,
      local
    )

  @property
  def default(self):
    return self.data.get("default")

  @property
  def log_dir(self):
    configured = self.data.get(
      "log_dir"
    )

    if configured:
      return Path(
        configured
      ).expanduser()

    return (
      Path.home()
      / ".local"
      / "state"
      / "aicb"
    )

  @property
  def models(self):
    return self.data.get(
      "models",
      {}
    )

  def get_model(self, name="chatgpt"):
    if name not in self.models:
      raise KeyError(
        f"Unknown model: {name}"
      )

    return self.models[name]

  def get_conversations(
    self,
    model="chatgpt"
  ):
    model_config = self.get_model(
      name=model
    )

    return model_config.get(
      "conversations",
      {}
    )

  def get_conversation(
    self,
    name=None,
    model="chatgpt"
  ):
    if name is None:
      name = self.default

    conversations = self.get_conversations(
      model=model
    )

    if name not in conversations:
      raise KeyError(
        f"Unknown conversation: {name}"
      )

    return conversations[name]

  @property
  def connections(self):
    return self.data.get(
      "connections",
      {}
    )

  def get_connection(self, name):
    if name not in self.connections:
      raise KeyError(
        f"Unknown connection: {name}"
      )

    return self.connections[name]

  @property
  def endpoint(self):
    return self.data.get(
      "endpoint",
      {}
    )

  def get_endpoint(self):
    return self.endpoint

  def get_endpoint_name(self):
    name = self.endpoint.get(
      "name"
    )

    if name is None:
      raise KeyError(
        "Endpoint name is not configured"
      )

    return name

  def get_endpoint_type(self):
    endpoint_type = self.endpoint.get(
      "type"
    )

    if endpoint_type is None:
      raise KeyError(
        "Endpoint type is not configured"
      )

    return endpoint_type
