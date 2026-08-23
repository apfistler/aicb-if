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
    if name == "chatgpt":
      return ChatGPTBrowserModel(
        self.config,
        self.connection
      )

    raise ValueError(
      f"Unsupported model: {name}"
    )
