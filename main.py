import time
from game import Game

def main():
    # Fallback: text-only mode if curses fails
    game = Game()
    print("STAR MINER — Use WASD to move, Q to quit")
    print("Terminal curses failed — falling back to text mode.")
    
    while True:
        print("\n" + game.render())
        
        if game.is_won():
            print("\n🎉 VICTORY! You mined all ore!")
            break
            
        if game.player['health'] <= 0:
            print("\n💀 GAME OVER — You were crushed by an asteroid!")
            break
            
        cmd = input("Move (WASD) or Q: ").lower().strip()
        if cmd == 'q':
            break
        elif cmd == 'w':
            result = game.move_player(0, -1)
            if result == 'dead':
                break
        elif cmd == 's':
            result = game.move_player(0, 1)
            if result == 'dead':
                break
        elif cmd == 'a':
            result = game.move_player(-1, 0)
            if result == 'dead':
                break
        elif cmd == 'd':
            result = game.move_player(1, 0)
            if result == 'dead':
                break
                
        time.sleep(0.1)

if __name__ == "__main__":
    main()
