import sys

from .logger import Logger
from .protocol import Request


class Endpoint:
  def __init__(self, config, models):
    self.config = config
    self.models = models
    self.logger = Logger(
      config.log_dir
    )

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

    self.logger.info(
      f"model: "
      f"{model.__class__.__name__}"
    )

    content = self.get_input()

    if not content:
      return None

    self.logger.info(
      f"input: {len(content)} bytes"
    )

    request = Request(
      content={
        "type": "text",
        "mime": "text/plain",
        "data": content
      }
    )

    self.logger.info(
      f"request: {request.id}"
    )

    filename = model.send(
      request
    )

    self.logger.info(
      f"sent: {filename}"
    )

    response = model.wait_for_response(
      request.id
    )

    self.logger.info(
      f"received response: "
      f"{response.get('id')}"
    )

    response_content = response.get(
      "content",
      {}
    )

    if response_content.get("type") == "text":
      output = response_content.get(
        "data",
        ""
      )

      print(output)

      self.logger.info(
        f"response: {len(output)} bytes"
      )
    else:
      print(response_content)

      self.logger.info(
        "response: non-text content"
      )

    return response

  def get_input(self):
    if len(sys.argv) > 1:
      return " ".join(
        sys.argv[1:]
      )

    if not sys.stdin.isatty():
      return sys.stdin.read()

    return input("> ")

  def run_model(self):
    model = self.models.get(
      name="chatgpt"
    )

    self.logger.info(
      f"model: "
      f"{model.__class__.__name__}"
    )

    return model.run()

  def run_daemon(self):
    model = self.models.get(
      name="chatgpt"
    )

    self.logger.info(
      f"model: "
      f"{model.__class__.__name__}"
    )

    self.logger.info(
      "daemon: waiting for requests..."
    )

    while True:
      request = model.receive()

      if request is None:
        continue

      self.logger.info(
        f"request received: "
        f"{request.get('id')}"
      )

      model.process(
        request
      )
