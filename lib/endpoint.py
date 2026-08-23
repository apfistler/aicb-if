from .protocol import Request


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
    model = self.models.get(
      name="chatgpt"
    )

    print(
      f"model: "
      f"{model.__class__.__name__}"
    )

    content = input("> ")

    if not content:
      return None

    request = Request(
      content={
        "type": "text",
        "mime": "text/plain",
        "data": content
      }
    )

    filename = model.send(
      request
    )

    print(
      f"sent: {filename}"
    )

    response = model.wait_for_response(
      request.id
    )

    print()
    print("=== RESPONSE ===")

    response_content = response.get(
      "content",
      {}
    )

    if response_content.get("type") == "text":
      print(
        response_content.get(
          "data",
          ""
        )
      )
    else:
      print(response_content)

    print("================")

    return response

  def run_model(self):
    model = self.models.get(
      name="chatgpt"
    )

    print(
      f"model: "
      f"{model.__class__.__name__}"
    )

    return model.run()

  def run_daemon(self):
    model = self.models.get(
      name="chatgpt"
    )

    print(
      f"model: "
      f"{model.__class__.__name__}"
    )

    print(
      "daemon: waiting for requests..."
    )

    while True:
      request = model.receive()

      if request is None:
        continue

      model.process(
        request
      )
