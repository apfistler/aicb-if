from .transport import SCPTransport


class Connection:
  def __init__(self, config):
    self.config = config

  def transport(
    self,
    name,
    model="chatgpt"
  ):
    connection = self.config.get_connection(
      name
    )

    connection_type = connection["type"]

    context_dir = (
      self.config.get_context_dir(
        model=model
      )
    )

    if connection_type == "scp":
      return SCPTransport(
        connection,
        context_dir
      )

    raise ValueError(
      f"Unsupported connection type: "
      f"{connection_type}"
    )
