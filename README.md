# Pac-Man (Python + pygame)

## Run

From the project root:

```bash
pip install -r requirements.txt
python -m src.main
```

Shows the Level 1 maze. Close the window or press Escape.

## What’s done

- **Maze** (`src/maze.py`): Level as list of strings in code (`LEVEL1_STRINGS`), no file needed. `Maze.from_strings()` and `Maze(path)` for file. Right column is always closed (short rows padded with `#`). Rectilinear layout (no diagonal walls).
- **Rendering** (`src/render/renderer.py`): Draws maze, pellets, spawns in a pygame window.
- **Entry** (`src/main.py`): Runs the maze preview.

## What’s left (for a full game)

| Part | File | To do |
|------|------|--------|
| Pac-Man | `src/entities/pacman.py` | Position, direction, 4-way movement, use `maze.is_wall()` for collision. |
| Pellets | `src/entities/pellet.py` | Track eaten state; game adds score and removes pellet when Pac-Man overlaps. |
| Ghosts | `src/entities/ghost.py` | Position; AI in `src/ai/ghost_ai.py` for chase/scatter/frightened. |
| Game state | `src/game.py` | Hold maze, Pac-Man, ghosts, pellets, score, lives; `update(dt)`, collisions, win/lose. |
| Main loop | `src/main.py` | Replace preview with: init game, loop: events → `game.update()` → render. |

Level files in `levels/*.txt` are optional; use `Maze("levels/level1.txt")` if you add them. Format: `#` wall, `.` pellet, `o` power pellet, `P`/`G` spawns.
