from .context import Context


class Receiver:
  def receive(self, context: Context):
    if not isinstance(context, Context):
      raise TypeError("context must be a Context instance")

    return context
