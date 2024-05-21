import os
import cma
import numpy as np
from utils.toad_gan_utils import load_trained_pyramid, generate_sample, one_hot_to_ascii_level
from Mario_AI_Framework.utils import run_java_game
import pickle
import torch

class CMAMarioOptimizer:
    def __init__(self, generator_path, num_evals=200):
        self.generator = self.load_generator(generator_path)
        self.num_evals = num_evals
        print("Zs shapes in the generator:")
        for i in range(len(self.generator.Zs)):
            print(self.generator.Zs[i].shape)

        # Automatically use half the size of the 0th Zs dimension
        self.input_shape = (self.generator.Zs[0].shape[0], 
                            self.generator.Zs[0].shape[1], 
                            self.generator.Zs[0].shape[2], 
                            self.generator.Zs[0].shape[3] // 2)
        self.es = None

    def save_optimizer_state(self, filename):
        """Save the optimizer state using pickle."""
        if self.es:
            with open(filename, 'wb') as f:
                pickle.dump(self.es, f)

    def load_optimizer_state(self, filename):
        """Load the optimizer state using pickle."""
        with open(filename, 'rb') as f:
            self.es = pickle.load(f)

    def load_generator(self, generator_dir):
        """Load the TOAD-GAN model from the specified directory."""
        loadgan, message = load_trained_pyramid(generator_dir)
        print(message)
        return loadgan

    def fitness(self, x):
        """Evaluate the fitness of a level generated from the latent vector x."""
        try:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            x_tensor = torch.from_numpy(x).float().to(device)
            x_reshaped = x_tensor.reshape(self.input_shape)

            level, scales, noises = generate_sample(self.generator.Gs, x_reshaped, self.generator.reals,
                                                    self.generator.NoiseAmp, self.generator.num_layers,
                                                    self.generator.token_list, scale_v=2.0, scale_h=4.0)
            ascii_level = one_hot_to_ascii_level(level, self.generator.token_list)
            with open(f"levels/temp/level.txt", "w") as f:
                for line in ascii_level:
                    f.write(line)
            results = run_java_game("levels/temp/level.txt", timer=20, mario_state=0, visuals=False)
            game_status = 1 if results.get('gameStatus', 'LOSE') == 'WIN' else 0
            fitness = results.get('completionPercentage', 0) + 0.1 * results.get('numJumps', 0) + game_status
            return -fitness
        except Exception as e:
            print(f"Error in fitness evaluation: {e}")
            raise

    def optimize(self):
        initial_mean_flat = np.zeros(np.prod(self.input_shape))
        sigma = 0.5
        if not self.es:
            opts = {'maxfevals': self.num_evals, 'popsize': 10}
            self.es = cma.CMAEvolutionStrategy(initial_mean_flat, sigma, opts)
        try:
            while not self.es.stop():
                solutions = self.es.ask()
                fitness_values = [self.fitness(x) for x in solutions]
                self.es.tell(solutions, fitness_values)
                self.es.logger.add()
                self.es.disp()
        except Exception as e:
            print("An error occurred:", e)
            raise

        print("Optimization completed")
        return self.es.result[5]  # The best solution

def generate_levels_from_saved_state(best_level, generator, input_shape, output_dir, num_levels=10):
    os.makedirs(output_dir, exist_ok=True)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    best_level_tensor = torch.from_numpy(best_level).float().to(device)
    
    for i in range(num_levels):
        best_level_reshaped = best_level_tensor.reshape(input_shape)
        level, scales, noises = generate_sample(generator.Gs, best_level_reshaped, generator.reals,
                                                generator.NoiseAmp, generator.num_layers,
                                                generator.token_list, scale_v=2.0, scale_h=4.0)
        ascii_level = one_hot_to_ascii_level(level, generator.token_list)
        with open(os.path.join(output_dir, f"best_level_{i}.txt"), "w") as f:
            for line in ascii_level:
                f.write(line)
        print(f"Best level {i} generated and saved successfully in {output_dir}")

def main():
    generator_dir = "generators"
    generator_files = [os.path.join(generator_dir, f) for f in os.listdir(generator_dir) if os.path.isdir(os.path.join(generator_dir, f))]
    optimizer_path = "optimizer_state.pkl"

    for generator_path in generator_files:
        if generator_path in ["generators/TOAD_GAN_1-3", "generators/TOAD_GAN_3-1", "generators/TOAD_GAN_5-3", "generators/TOAD_GAN_4-1", "generators/TOAD_GAN_1-1",
                               "generators/TOAD_GAN_7-1", "generators/TOAD_GAN_2-1", "generators/TOAD_GAN_6-2", "generators/TOAD_GAN_6-3", "generators/TOAD_GAN_1-2",
                               "generators/TOAD_GAN_8-1"]:
            continue
        try:
            level_name = generator_path.split("_")[-1]
            output_dir = f"levels/cmaes/lvl_{level_name}"

            optimizer = CMAMarioOptimizer(generator_path, num_evals=200)
            print(f"Starting optimization for generator: {generator_path}")
            best_level = optimizer.optimize()
            print(f"Best level latent vector for {generator_path}: {best_level}")

            # Save the best vector and optimizer state
            np.save(f"cmaes/best_level_{level_name}.npy", best_level)
            optimizer.save_optimizer_state(f"cmaes/optimizer_state_{level_name}.pkl")

            # Optionally, reload the optimizer to continue later
            # optimizer.load_optimizer_state(optimizer_path)
            # best_level = np.load(f"best_level_{level_name}.npy")

            # Generate 10 levels using the loaded state
            generate_levels_from_saved_state(best_level, optimizer.generator, optimizer.input_shape, output_dir, num_levels=10)
        except Exception as e:
            print(f"Error in optimization for generator {generator_path}: {e}")

if __name__ == "__main__":
    main()
