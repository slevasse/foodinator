from dataclasses import dataclass

@dataclass
class ingredient():
    """ A  class representing an ingredient. """
    name: str
    quantity: float
    unit: str
    type: str
    season: str
