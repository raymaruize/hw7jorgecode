# Pac-Man (Python + pygame) — Phase 2

This repository is based on starter code received from:
https://github.com/jorgecastano1/hw7

## Run
1) `source .venv/bin/activate`
2) `python -m src.main`

If needed:
1) `python3 -m venv .venv`
2) `source .venv/bin/activate`
3) `pip install -r requirements.txt`

---

## What I received (baseline)
Initial snapshot commit: `26ef95e`

At baseline, the project mainly had:
- Maze model and parsing (`src/maze.py`)
- Maze preview rendering (`src/render/renderer.py`)
- Entry point showing static preview (`src/main.py`)
- Empty stubs for game/entities/AI modules

---

## What I added on top (my Phase 2 work)

### 1) Minimal playable game loop
Commit: `1751748`

Added:
- Real game loop in `src/main.py` (input → update → render)
- `Game` state manager in `src/game.py`
- Basic entities:
	- `src/entities/pacman.py`
	- `src/entities/ghost.py`
	- `src/entities/pellet.py`
- Game mechanics:
	- one-keypress one-tile movement
	- pellet eating and scoring
	- win/lose detection
- Rendering integration with dynamic game state in `src/render/renderer.py`

### 2) Simple ghost patrol movement
Commit: `4aac6a9`

Added:
- timed ghost movement step
- valid-direction checks against walls
- fallback random direction selection when blocked

### 3) Documentation and repo hygiene
Commit: `2230219`

Added/updated:
- this README to clearly separate baseline vs my contributions
- `.gitignore` for cache/venv/system files

---

## Current feature status
### Working now
- Playable maze
- Pac-Man movement
- Pellet collection + score
- Ghost movement (basic patrol)
- Win/Lose conditions

### Still remaining
- Smarter ghost AI (chase/scatter/frightened)
- Lives and restart flow
- Animation/sprite polish

---

## Quick way to prove my contribution
From repo root:

`git log --oneline`

You should see this progression:
1. `26ef95e` baseline snapshot (received code)
2. `1751748` minimal playable implementation
3. `4aac6a9` ghost patrol movement
4. `2230219` documentation + cleanup
