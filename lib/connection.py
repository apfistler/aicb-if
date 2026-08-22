from .transport import SCPTransport


class Connection:
  def __init__(self, config):
    self.config = config

  def transport(self, name):
    connection = self.config.get_connection(name)

    connection_type = connection["type"]

    if connection_type == "scp":
      return SCPTransport(connection)

    raise ValueError(
      f"Unsupported connection type: {connection_type}"
    )
