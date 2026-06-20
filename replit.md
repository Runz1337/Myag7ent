# Star Miner — Terminal Roguelike

## Architecture
- **Stack**: Python 3.11, curses (built-in)
- **Why**: Pure terminal, zero dependencies, immersive CLI experience

## Key Decisions
- **Turn-based grid exploration**: Player moves on a 20x20 grid, mines ore, avoids asteroids
- **Procedural generation**: Ore and asteroids spawn randomly each game
- **No save system**: One-session roguelike — death is permanent, replay value in randomness

## File Map
- `/main.py` — Core game loop, input handling, rendering
- `/game.py` — *Not needed — logic inlined for simplicity*

## Environment Variables Required
- None

## Known Issues / TODOs
- [ ] Add high score persistence (next iteration)
- [ ] Add sound via ASCII音效 (e.g., `print('\a')`) — *implemented*
