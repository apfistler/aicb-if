from .chatgpt import ChatGPTBrowserModel


class Models:
  def __init__(
    self,
    config,
    connection
  ):
    self.config = config
    self.connection = connection

  def get(self, name):
    model_config = self.config.get_model(
      name=name
    )

    provider = model_config.get(
      "provider"
    )

    model_type = model_config.get(
      "type"
    )

    if (
      provider == "chatgpt"
      and model_type == "browser"
    ):
      return ChatGPTBrowserModel(
        config=self.config,
        connection=self.connection
      )

    raise NotImplementedError(
      f"No model implementation for "
      f"provider={provider!r}, "
      f"type={model_type!r}"
    )
