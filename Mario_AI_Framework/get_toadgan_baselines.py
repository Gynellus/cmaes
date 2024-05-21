import os
import csv
from collections import defaultdict
from utils import run_java_game

def main():
    level_dir = "./levels/cmaes/"
    generated_list = os.listdir(level_dir)

    # Dictionary to track results by level and by run
    all_results = defaultdict(list)

    # Set of keys we're interested in tracking, sorted for consistent column order
    keys_of_interest = sorted(['totalKills', 'gameStatus', 'killsByStomp', 'remainingTime', 'maxJumpAirTime', 'numJumps', 'maxXJump', 'completionPercentage', 'currentCoins'])
    
    # Ensure the output directory exists
    output_dir = './baselines'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file_path = os.path.join(output_dir, 'lve_toadgan_results.csv')
    # Open CSV file once and write headers
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['generator', 'level', 'run'] + keys_of_interest
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for generator in generated_list:
            level_list = os.listdir(os.path.join(level_dir, generator))

            # Process each level
            for level in level_list:
                level_name = f"{generator}_{level}"  # Append generator name to level name
                level_path = os.path.join(level_dir, generator, level)
                print(f"Processing level: {level_path}")

                # Run each level 10 times
                for run in range(10):
                    print(f"Run {run + 1}/10 for level {level_name}")
                    game_results = run_java_game(level_path, timer=20, mario_state=0, visuals=False)

                    # Store only the useful results and add generator and level info
                    result_entry = {key: game_results.get(key, None) for key in keys_of_interest}
                    result_entry['generator'] = generator
                    result_entry['level'] = level_name
                    result_entry['run'] = run + 1

                    writer.writerow(result_entry)

if __name__ == "__main__":
    main()
