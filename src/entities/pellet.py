from dataclasses import dataclass
from typing import Literal

PelletType = Literal["normal", "power"]


@dataclass
class Pellet:
	"""Tracks one pellet and whether it has been eaten."""

	row: int
	col: int
	pellet_type: PelletType
	eaten: bool = False

