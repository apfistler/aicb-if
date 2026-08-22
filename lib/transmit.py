from .context import Context


class Transmitter:
  def transmit(self, context: Context):
    if not isinstance(context, Context):
      raise TypeError("context must be a Context instance")

    return context
