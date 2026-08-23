from .context import Context


class Model:
  def send(self, context: Context):
    raise NotImplementedError

  def receive(self):
    raise NotImplementedError

  def process(self):
    raise NotImplementedError
