"""
Maze and level layout.

Loads a level from a text file (e.g. levels/level1.txt) and exposes the grid,
spawn positions, and pellet data. Used by game.py for collision and entity placement.

Level file format:
  # = wall
  . = walkable + normal pellet
  o = walkable + power pellet
  (space) = walkable, no pellet
  P = Pac-Man spawn (one)
  G = Ghost spawn (one or more)
"""

from pathlib import Path
from typing import List, Literal, Optional, Union

PelletType = Literal["normal", "power"]

# Built-in Level 1: rectilinear (no diagonals), right column closed in code
LEVEL1_STRINGS = [
    "####################",
    "#..................#",
    "#.####.######.#####",
    "#.#.............#.#",
    "#.#.#####.#####.#.#",
    "#.....#.....#.....#",
    "#.###.#.....#.###.#",
    "#.....#..o..#.....#",
    "#.###.#####.#.###.#",
    "#.......P....G....#",
    "####################",
]


class Maze:
    """
    Represents one level: grid of cells, Pac-Man spawn, ghost spawns, and pellet types.

    After loading, spawn cells (P, G) are treated as walkable; their positions
    are stored separately for entity placement.
    """

    def __init__(self, level_path: Union[str, Path]) -> None:
        self._grid: list[list[str]] = []
        self._rows = 0
        self._cols = 0
        self._pacman_spawn: tuple[int, int] = (0, 0)
        self._ghost_spawns: list[tuple[int, int]] = []
        self._pellets: dict[tuple[int, int], PelletType] = {}
        self.load(level_path)

    @classmethod
    def from_strings(cls, lines: List[str]) -> "Maze":
        """Build a maze from a list of strings (e.g. LEVEL1_STRINGS). No file, no padding bugs."""
        self = cls.__new__(cls)
        self._grid = []
        self._ghost_spawns = []
        self._pellets = {}
        for row_idx, line in enumerate(lines):
            line = line.rstrip()
            row = []
            for col_idx, char in enumerate(line):
                if char == "#":
                    row.append("#")
                elif char == "P":
                    row.append(" ")
                    self._pacman_spawn = (row_idx, col_idx)
                elif char == "G":
                    row.append(" ")
                    self._ghost_spawns.append((row_idx, col_idx))
                elif char == ".":
                    row.append(" ")
                    self._pellets[(row_idx, col_idx)] = "normal"
                elif char == "o":
                    row.append(" ")
                    self._pellets[(row_idx, col_idx)] = "power"
                else:
                    row.append(" ")
            self._grid.append(row)
        self._rows = len(self._grid)
        self._cols = max(len(r) for r in self._grid) if self._grid else 0
        for row in self._grid:
            while len(row) < self._cols:
                row.append("#")
        return self

    def load(self, level_path: Union[str, Path]) -> None:
        """
        Load and parse a level file. Path can be absolute or relative to current working directory.
        """
        path = Path(level_path)
        if not path.exists():
            raise FileNotFoundError(f"Level file not found: {path}")

        self._grid = []
        self._ghost_spawns = []
        self._pellets = {}

        with open(path, "r", encoding="utf-8") as f:
            for row_idx, line in enumerate(f):
                line = line.rstrip()
                row: list[str] = []
                for col_idx, char in enumerate(line):
                    if char == "#":
                        row.append("#")
                    elif char == "P":
                        row.append(" ")
                        self._pacman_spawn = (row_idx, col_idx)
                    elif char == "G":
                        row.append(" ")
                        self._ghost_spawns.append((row_idx, col_idx))
                    elif char == ".":
                        row.append(" ")
                        self._pellets[(row_idx, col_idx)] = "normal"
                    elif char == "o":
                        row.append(" ")
                        self._pellets[(row_idx, col_idx)] = "power"
                    elif char == " ":
                        row.append(" ")
                    else:
                        row.append(" ")
                self._grid.append(row)

        self._rows = len(self._grid)
        self._cols = max(len(r) for r in self._grid) if self._grid else 0

        # Pad short rows with walls so the right column is always closed
        for row in self._grid:
            while len(row) < self._cols:
                row.append("#")

    def is_wall(self, row: int, col: int) -> bool:
        """Return True if (row, col) is out of bounds or a wall."""
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return True
        return self._grid[row][col] == "#"

    def is_walkable(self, row: int, col: int) -> bool:
        """Return True if (row, col) is within bounds and not a wall."""
        return not self.is_wall(row, col)

    def get_pacman_spawn(self) -> tuple[int, int]:
        """Return (row, col) where Pac-Man should start."""
        return self._pacman_spawn

    def get_ghost_spawns(self) -> list[tuple[int, int]]:
        """Return list of (row, col) where each ghost should start."""
        return self._ghost_spawns.copy()

    def get_pellet_at(self, row: int, col: int) -> Optional[PelletType]:
        """
        Return the pellet type at (row, col), or None if there is no pellet.
        Used for initial setup and collision; game state tracks which pellets are eaten.
        """
        return self._pellets.get((row, col))

    def get_all_pellet_positions(self) -> list[tuple[int, int, PelletType]]:
        """Return [(row, col, type), ...] for every pellet in the level. Used to init game state."""
        return [(*pos, ptype) for pos, ptype in self._pellets.items()]

    def get_rows(self) -> int:
        """Number of rows in the grid."""
        return self._rows

    def get_cols(self) -> int:
        """Number of columns in the grid."""
        return self._cols

    def get_grid(self) -> list[list[str]]:
        """Raw grid: each cell is '#' or ' '. For rendering or debugging."""
        return [row[:] for row in self._grid]
