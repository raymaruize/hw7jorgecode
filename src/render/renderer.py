"""
Draw the maze (walls, pellets, spawns) onto a pygame surface.

Uses a fixed cell size in pixels so the grid maps 1:1 to screen tiles.
Run from project root so level path works: python -m src.main
"""

import pygame
from typing import Optional

# Colors (R, G, B)
BACKGROUND = (15, 15, 35)
WALL = (33, 33, 255)
WALL_BORDER = (20, 20, 140)
PELLET = (255, 220, 100)
POWER_PELLET = (255, 180, 50)
PACMAN_SPAWN = (255, 255, 0)
GHOST_SPAWN = (255, 100, 100)


def draw_maze(
    surface: pygame.Surface,
    maze: "Maze",
    cell_size: int,
    offset_x: int = 0,
    offset_y: int = 0,
) -> None:
    """
    Draw the full maze: walls, pellets, and spawn markers.

    surface: pygame surface to draw on (e.g. screen)
    maze: Maze instance from src.maze
    cell_size: width and height in pixels of one grid cell
    offset_x, offset_y: top-left corner of the maze on the surface (for centering)
    """
    rows = maze.get_rows()
    cols = maze.get_cols()
    grid = maze.get_grid()

    for row in range(rows):
        for col in range(cols):
            x = offset_x + col * cell_size
            y = offset_y + row * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)

            if grid[row][col] == "#":
                pygame.draw.rect(surface, WALL_BORDER, rect)
                inner = pygame.Rect(x + 1, y + 1, cell_size - 2, cell_size - 2)
                pygame.draw.rect(surface, WALL, inner)
            else:
                # Walkable: draw pellet if any
                pellet_type = maze.get_pellet_at(row, col)
                if pellet_type == "normal":
                    center = (x + cell_size // 2, y + cell_size // 2)
                    pygame.draw.circle(surface, PELLET, center, cell_size // 6)
                elif pellet_type == "power":
                    center = (x + cell_size // 2, y + cell_size // 2)
                    pygame.draw.circle(surface, POWER_PELLET, center, cell_size // 4)

    # Spawn markers (so you can see where P and G are)
    py, px = maze.get_pacman_spawn()
    cx = offset_x + px * cell_size + cell_size // 2
    cy = offset_y + py * cell_size + cell_size // 2
    pygame.draw.circle(surface, PACMAN_SPAWN, (cx, cy), cell_size // 3)

    for gy, gx in maze.get_ghost_spawns():
        cx = offset_x + gx * cell_size + cell_size // 2
        cy = offset_y + gy * cell_size + cell_size // 2
        pygame.draw.circle(surface, GHOST_SPAWN, (cx, cy), cell_size // 3)


def run_maze_preview(level_path: Optional[str], cell_size: int = 28) -> None:
    """
    Open a pygame window and draw the maze. Close with the window or Escape.

    level_path: path to level file, e.g. 'levels/level1.txt'
    cell_size: pixels per grid cell
    """
    from src.maze import Maze, LEVEL1_STRINGS

    maze = Maze.from_strings(LEVEL1_STRINGS) if level_path is None else Maze(level_path)
    rows = maze.get_rows()
    cols = maze.get_cols()

    width = cols * cell_size
    height = rows * cell_size

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze preview — close window or press Escape")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill(BACKGROUND)
        draw_maze(screen, maze, cell_size)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Avoid circular import at module load; Maze is only needed when drawing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.maze import Maze
