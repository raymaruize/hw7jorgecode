"""
Game state and core update logic (minimal, readable baseline).

This keeps Phase 2 changes small while preserving the original maze/render work.
"""

import random

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

		# simple ghost patrol settings (small, readable step for Phase 2)
		self.ghost_direction: tuple[int, int] = (0, 1)
		self.ghost_move_interval_frames = 9
		self._ghost_frame_counter = 0

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

	def _get_valid_ghost_directions(self) -> list[tuple[int, int]]:
		"""Return all non-wall directions the ghost can move."""
		options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		valid: list[tuple[int, int]] = []
		for d_row, d_col in options:
			n_row = self.ghost.row + d_row
			n_col = self.ghost.col + d_col
			if not self.maze.is_wall(n_row, n_col):
				valid.append((d_row, d_col))
		return valid

	def _move_ghost(self) -> None:
		"""
		Minimal ghost movement:
		- move one tile every N frames
		- continue direction when possible
		- otherwise pick a random valid direction
		"""
		self._ghost_frame_counter += 1
		if self._ghost_frame_counter < self.ghost_move_interval_frames:
			return
		self._ghost_frame_counter = 0

		valid = self._get_valid_ghost_directions()
		if not valid:
			return

		if self.ghost_direction not in valid:
			self.ghost_direction = random.choice(valid)

		d_row, d_col = self.ghost_direction
		next_row = self.ghost.row + d_row
		next_col = self.ghost.col + d_col

		# Safety check (keeps logic robust if map changes)
		if self.maze.is_wall(next_row, next_col):
			self.ghost_direction = random.choice(valid)
			d_row, d_col = self.ghost_direction
			next_row = self.ghost.row + d_row
			next_col = self.ghost.col + d_col

		self.ghost.row = next_row
		self.ghost.col = next_col

	def update(self) -> None:
		if self.game_over:
			return

		self._apply_move()
		self._eat_pellet_if_present()
		self._move_ghost()
		self._check_end_conditions()

	def pellets_left(self) -> int:
		return sum(1 for p in self.pellets.values() if not p.eaten)

