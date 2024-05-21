import os
import csv
from collections import defaultdict
from utils import run_java_game

def main():
    level_dir = "./levels/original"
    level_list = os.listdir(level_dir)

    # Dictionary to track results by level and by run
    all_results = defaultdict(list)

    # Set of keys we're interested in tracking, sorted for consistent column order
    keys_of_interest = sorted(['totalKills', 'gameStatus', 'killsByStomp', 'remainingTime', 'maxJumpAirTime', 'numJumps', 'maxXJump', 'completionPercentage', 'currentCoins'])

    # Process each level
    for level in level_list:
        level_path = os.path.join(level_dir, level)
        print(f"Processing level: {level_path}")
        
        # Run each level 10 times
        for run in range(10):
            print(f"Run {run + 1}/10")
            game_results = run_java_game(level_path, timer=20, mario_state=0, visuals=False)
            
            # Store only the useful results
            result_entry = {key: game_results.get(key, None) for key in keys_of_interest}
            result_entry['level'] = level
            result_entry['run'] = run + 1
            all_results[level].append(result_entry)

    if os.path.exists('./baselines'):
        os.makedirs('./baselines')

    # Write results to a CSV file
    with open('./baselines/original_levels.csv', 'w', newline='') as csvfile:
        fieldnames = ['level', 'run'] + keys_of_interest
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for results in all_results.values():
            for data in results:
                writer.writerow(data)

    print("Results have been saved to game_results.csv")

if __name__ == "__main__":
    main()
