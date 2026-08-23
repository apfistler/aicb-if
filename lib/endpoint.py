from .context import Context


class Endpoint:
  def __init__(self, config, models):
    self.config = config
    self.models = models

  def run(self):
    endpoint_type = self.config.get_endpoint_type()

    if endpoint_type == "client":
      return self.run_client()

    if endpoint_type == "model":
      return self.run_model()

    raise ValueError(
      f"Unsupported endpoint type: "
      f"{endpoint_type!r}"
    )

  def run_client(self):
    raise NotImplementedError(
      "Client endpoint is not implemented yet"
    )

  def run_model(self):
    model = self.models.get(
      name="chatgpt"
    )

    print(
      f"model: "
      f"{model.__class__.__name__}"
    )

    context = model.receive()

    if context is None:
      print("no pending context")
      return None

    print("received context:")
    print(context.content)

    return model.process(context)
