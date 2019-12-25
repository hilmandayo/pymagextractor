from dataclasses import dataclass
from typing import Optional, List

@dataclass(order=True)
class Handler:
    name: str  # Name of the class. Will use as the name of Button if exists.
    ref: str   # Name to be refer internally. Will be used as the name in csv
    button: bool = False
    values: Optional[List[str]] = None
