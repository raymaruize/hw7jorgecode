"""
Game state and core update logic (minimal, readable baseline).

This keeps Phase 2 changes small while preserving the original maze/render work.
"""

from src.entities.ghost import Ghost
from src.entities.pacman import Pacman
from src.entities.pellet import Pellet
from src.maze import LEVEL1_STRINGS, Maze


class Game:
	"""Minimal playable game wrapper around the existing maze."""

	def __init__(self) -> None:
		self.maze = Maze.from_strings(LEVEL1_STRINGS)

		p_row, p_col = self.maze.get_pacman_spawn()
		self.pacman = Pacman(row=p_row, col=p_col)

		ghost_spawns = self.maze.get_ghost_spawns()
		if ghost_spawns:
			g_row, g_col = ghost_spawns[0]
		else:
			g_row, g_col = p_row, p_col
		self.ghost = Ghost(row=g_row, col=g_col)

		self.pellets: dict[tuple[int, int], Pellet] = {}
		for row, col, ptype in self.maze.get_all_pellet_positions():
			self.pellets[(row, col)] = Pellet(row=row, col=col, pellet_type=ptype)

		self.score = 0
		self.running = True
		self.game_over = False
		self.win = False

		# one key press -> one tile move
		self.pending_move: tuple[int, int] | None = None

	def request_move(self, d_row: int, d_col: int) -> None:
		self.pending_move = (d_row, d_col)

	def _apply_move(self) -> None:
		if self.pending_move is None:
			return

		d_row, d_col = self.pending_move
		target_row = self.pacman.row + d_row
		target_col = self.pacman.col + d_col

		if not self.maze.is_wall(target_row, target_col):
			self.pacman.row = target_row
			self.pacman.col = target_col

		self.pending_move = None

	def _eat_pellet_if_present(self) -> None:
		key = (self.pacman.row, self.pacman.col)
		pellet = self.pellets.get(key)
		if pellet and not pellet.eaten:
			pellet.eaten = True
			self.score += 50 if pellet.pellet_type == "power" else 10

	def _check_end_conditions(self) -> None:
		# Loss: touch ghost
		if self.pacman.row == self.ghost.row and self.pacman.col == self.ghost.col:
			self.game_over = True
			self.win = False
			return

		# Win: all pellets eaten
		pellets_left = sum(1 for p in self.pellets.values() if not p.eaten)
		if pellets_left == 0:
			self.game_over = True
			self.win = True

	def update(self) -> None:
		if self.game_over:
			return

		self._apply_move()
		self._eat_pellet_if_present()
		self._check_end_conditions()

	def pellets_left(self) -> int:
		return sum(1 for p in self.pellets.values() if not p.eaten)

