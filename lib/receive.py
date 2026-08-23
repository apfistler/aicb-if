def send(self, content, filename):
  with tempfile.NamedTemporaryFile(
    mode="w",
    encoding="utf-8",
    suffix=".json",
    delete=False
  ) as f:
    f.write(content)
    source_path = Path(f.name)

  try:
    destination = (
      f"{self.user}@{self.host}:"
      f"{self.context_path}/{filename}"
    )

    subprocess.run(
      [
        "scp",
        "-P",
        str(self.port),
        "-i",
        str(self.identity_file),
        str(source_path),
        destination,
      ],
      check=True,
    )
  finally:
    source_path.unlink(missing_ok=True)
