"""
Pac-Man game entry point.

Run from the project root (or any directory):
  python -m src.main

Shows Level 1 maze (defined in maze.py; no level file required).
Close the window or press Escape to exit.
"""

from src.render.renderer import run_maze_preview

if __name__ == "__main__":
    run_maze_preview(None, cell_size=28)
