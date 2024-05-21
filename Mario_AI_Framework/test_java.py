from utils import run_java_game

if __name__ == "__main__":
    level_path = "./levels/original/lvl-1.txt"  # Adjust as needed
    game_results = run_java_game(level_path, visuals=True)
    print(game_results)
