from utils import run_java_game
import os

if __name__ == "__main__":
    level_path = "./levels/original/"
    # create an empty list to store the game results
    game_results = []
    for level in os.listdir(level_path):
        for i in range(10): 
            level_path = f"./levels/original/{level}"
            game_res = run_java_game(level_path, visuals=False)

            game_results.append((level, game_res))
    print(game_results)
    # Save the game results to a file
    with open("./results/original_levels.txt", "w") as f:
        for level, res in game_results:
            f.write(f"Level: {level}\n")
            f.write(f"Results: {res}\n")
            f.write("\n")