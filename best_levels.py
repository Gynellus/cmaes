import os
import torch
import numpy as np
from utils.toad_gan_utils import load_trained_pyramid, generate_sample, one_hot_to_ascii_level
from Mario_AI_Framework.utils import run_java_game

# Constants
NUM_LEVELS = 100
TOP_LEVELS_COUNT = 10
GENERATORS_PATH = "generators"

# Load the TOAD-GAN model
def load_generator(generator_dir):
    generator, _ = load_trained_pyramid(generator_dir)
    return generator

# Generate a level and evaluate its fitness
def evaluate_level(generator):
    level, _, _ = generate_sample(generator.Gs, generator.Zs, generator.reals, generator.NoiseAmp, generator.num_layers, generator.token_list)
    ascii_level = one_hot_to_ascii_level(level, generator.token_list)
    # Temporary saving level to disk for game simulation
    level_path = "levels/temp/temp_level.txt"
    with open(level_path, "w") as file:
        for line in ascii_level:
            file.write(line)
    results = run_java_game(level_path, timer=20, mario_state=0, visuals=False)
    # Define fitness function based on game results
    fitness = reward(results)
    print("Fitness:", fitness, "Status:", results.get('gameStatus'))
    return fitness, level

def reward(results):
    behavior_reward = results.get('killsByStomp', 0) + results.get('numJumps', 0) + (100 if results.get('gameStatus', 'LOSE') == 'WIN' else 0)
    return behavior_reward
# Main routine to generate levels for each generator
def main():
    for generator_dir in sorted(os.listdir(GENERATORS_PATH)):
        generator_path = os.path.join(GENERATORS_PATH, generator_dir)
        if os.path.isdir(generator_path):
            generator = load_generator(generator_path)
            top_levels = []

            for _ in range(NUM_LEVELS):
                fitness, level = evaluate_level(generator)
                if len(top_levels) < TOP_LEVELS_COUNT:
                    top_levels.append((fitness, level))
                    top_levels.sort(reverse=True, key=lambda x: x[0])  # Keep sorted by highest fitness
                elif fitness > top_levels[-1][0]:
                    top_levels[-1] = (fitness, level)
                    top_levels.sort(reverse=True, key=lambda x: x[0])

            # Create directory to save top levels for this generator
            top_levels_dir = f"levels/top_levels/lvl_{generator_dir.split('_')[-1]}"
            if not os.path.exists(top_levels_dir):
                os.makedirs(top_levels_dir)

            # Save top levels
            for index, (fitness, level) in enumerate(top_levels):
                level_path = f"{top_levels_dir}/level_{index}_fitness_{fitness}.txt"
                with open(level_path, "w") as file:
                    for line in one_hot_to_ascii_level(level, generator.token_list):
                        file.write(line)

            print(f"Top levels generated and saved successfully for {generator_dir}.")

if __name__ == "__main__":
    main()
