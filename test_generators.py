import numpy as np
import torch
from utils.toad_gan_utils import load_trained_pyramid, generate_sample, one_hot_to_ascii_level

class LevelGenerator:
    def __init__(self, generator_path):
        self.generator = self.load_generator(generator_path)

    def load_generator(self, generator_dir):
        """
        Load the TOAD-GAN model from the specified directory.
        """
        loadgan, message = load_trained_pyramid(generator_dir)  
        print(message)
        return loadgan
    
    def generate_level(self, latent_vector_shape):
        """
        Generate and save a level using the given latent vector shape.
        """
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        latent_vector_shapes = [tuple(x.shape[:-1]) + (x.shape[-1] // 2,) for x in self.generator.Zs]
        latent_vectors = [torch.randn(x).float().to(device) for x in latent_vector_shapes]
        
        # Generate the level
        level, scales, noises = generate_sample(self.generator.Gs, latent_vectors, self.generator.reals,
                                                self.generator.NoiseAmp, self.generator.num_layers,
                                                self.generator.token_list, scale_v=1.0, scale_h=1.0)
        ascii_level = one_hot_to_ascii_level(level, self.generator.token_list)
        
        # Save the level to a file
        with open("levels/generated_level.txt", "w") as f:
            for line in ascii_level:
                f.write(line)
        print("Generated level saved successfully")
    
    def inspect_generator(self):
        """
        Inspect the generator's Zs shapes.
        """
        print("Zs shapes in the generator:")
        for i, z in enumerate(self.generator.Zs):
            print(f"Z[{i}] shape: {z.shape}")

def main():
    generator_path = "generators/TOAD_GAN_1-1"
    latent_vector_shape = (1, 12, 14, 50)  # Adjust this shape to see different outputs

    level_gen = LevelGenerator(generator_path)
    level_gen.inspect_generator()
    level_gen.generate_level(latent_vector_shape)

if __name__ == "__main__":
    main()
