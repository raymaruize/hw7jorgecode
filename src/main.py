"""
Pac-Man game entry point.

Run from the project root (or any directory):
  python -m src.main

Phase 2 minimal playable baseline:
- one-tile movement per keypress
- pellet collection and score
- win/lose detection

Close the window or press Escape to exit.
"""

import pygame

from src.game import Game
from src.render.renderer import BACKGROUND, draw_game


def run_game(cell_size: int = 28) -> None:
  game = Game()
  rows = game.maze.get_rows()
  cols = game.maze.get_cols()

  width = cols * cell_size
  height = rows * cell_size

  pygame.init()
  screen = pygame.display.set_mode((width, height))
  clock = pygame.time.Clock()

  while game.running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game.running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          game.running = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
          game.request_move(0, -1)
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
          game.request_move(0, 1)
        elif event.key in (pygame.K_UP, pygame.K_w):
          game.request_move(-1, 0)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
          game.request_move(1, 0)

    game.update()

    status = "RUNNING"
    if game.game_over and game.win:
      status = "YOU WIN"
    elif game.game_over:
      status = "GAME OVER"
    pygame.display.set_caption(
      f"Pac-Man Phase 2 | Score: {game.score} | Pellets Left: {game.pellets_left()} | {status}"
    )

    screen.fill(BACKGROUND)
    draw_game(screen, game, cell_size)
    pygame.display.flip()
    clock.tick(60)

  pygame.quit()

if __name__ == "__main__":
  run_game(cell_size=28)
