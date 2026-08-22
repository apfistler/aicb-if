from .transport import Transport


class Receiver:
  def __init__(self, transport: Transport):
    self.transport = transport

  def receive(self):
    filenames = self.transport.list()

    if not filenames:
      return None

    filename = sorted(filenames)[0]

    context = self.transport.receive(filename)

    self.transport.remove(filename)

    return context
