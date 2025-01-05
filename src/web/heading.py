class Heading:

  def __init__(self, name: str, subs: list[str] | None = None) -> None:
    self.name = name
    if subs is None:
      self.subs = []
    else:
      self.subs = subs
    self.contents: str | None = None

  

  