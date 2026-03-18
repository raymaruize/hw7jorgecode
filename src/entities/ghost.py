from dataclasses import dataclass


@dataclass
class Ghost:
	"""Minimal ghost entity (static in this first playable step)."""

	row: int
	col: int

