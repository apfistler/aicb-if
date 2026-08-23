import json


class Receiver:
  def __init__(self, transport):
    self.transport = transport

  def receive(self):
    filenames = self.transport.list()

    if not filenames:
      return None

    filename = sorted(filenames)[0]

    content = self.transport.receive(
      filename
    )

    self.transport.remove(filename)

    return json.loads(content)
