from .context import Context


class Transport:
  def send(self, context: Context):
    if not isinstance(context, Context):
      raise TypeError("context must be a Context instance")

    raise NotImplementedError
