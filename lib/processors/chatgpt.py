from ..protocol import Response


class ChatGPTProcessor:
  def __init__(
    self,
    model
  ):
    self.model = model

  def process(
    self,
    request
  ):
    print()
    print("=== REQUEST RECEIVED ===")
    print(
      f"id: {request['id']}"
    )
    print(
      f"model: {request['model']}"
    )
    print(
      f"conversation: "
      f"{request['conversation']}"
    )
    print(
      f"content type: "
      f"{request['content']['type']}"
    )
    print(
      f"mime: "
      f"{request['content']['mime']}"
    )
    print(
      f"content: "
      f"{request['content']['data']}"
    )
    print("========================")
    print()

    response = Response(
      request_id=request["id"],
      content={
        "type": "text",
        "mime": "text/plain",
        "data": (
          "HELLO FROM THE CHROMEBOOK MODEL"
        )
      }
    )

    filename = self.model.send(
      response
    )

    print(
      f"response sent: {filename}"
    )

    return response
