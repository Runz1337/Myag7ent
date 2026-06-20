# Terminal Game: **Star Miner**  

## Architecture  
- **Stack**: Python 3.11, curses (built-in), random, time  
- **Why**: Pure terminal, no external deps, immersive CLI experience  

## Key Decisions  
- **Turn-based grid exploration**: Player moves on a 20x20 grid, mines resources, avoids asteroids  
- **Procedural generation**: Asteroids and ore spawn randomly each game  
- **No save system**: One-session roguelike — death is permanent, replay value in randomness  

## File Map  
- `/main.py` — Core game loop, input handling, rendering  
- `/game.py` — Game state, player, grid, collision logic  

## Environment Variables Required  
- None  

## Known Issues / TODOs  
- [ ] Add high score persistence (next iteration)  
- [ ] Add sound via ASCII音效 (e.g., `print('\a')`)  
