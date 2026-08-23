class Backend:
  def __init__(
    self,
    queue,
    processor,
    logger
  ):
    self.queue = queue
    self.processor = processor
    self.logger = logger

  def run(self):
    self.logger.info(
      "backend: waiting for requests..."
    )

    while True:
      request = self.queue.wait()

      self.logger.info(
        f"request received: "
        f"{request.get('id')}"
      )

      self.processor.process(
        request
      )
