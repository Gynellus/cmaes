import os
from utils.toad_gan_utils import load_trained_pyramid, generate_sample, one_hot_to_ascii_level

# Hardcoded path to the generator
generators_path = "generators"

# Object holding important data about the current level
class LevelObject:
    def __init__(self, ascii_level, oh_level, image, tokens, scales, noises):
        self.ascii_level = ascii_level
        self.oh_level = oh_level  # one-hot encoded
        self.image = image
        self.tokens = tokens
        self.scales = scales
        self.noises = noises

def load_generator(generator_dir):
    """
    Load the TOAD-GAN model from the specified directory.
    """
    loadgan, message = load_trained_pyramid(generator_dir)
    print(message)
    return loadgan


def generate_levels(generator, save_path, num_levels=10):
    """
    Generate multiple levels using the loaded TOAD-GAN model.
    """
    levels = []
    level_obj = LevelObject(None, None, None, None, None, None)
    for i in range(num_levels):
        print(f"Generating level {i+1}/{num_levels}")
        for j in generator.Zs:
            print(type(j), j.shape)
        level, scales, noises = generate_sample(generator.Gs, generator.Zs, generator.reals,
                                                generator.NoiseAmp, generator.num_layers,
                                                generator.token_list, scale_v=1.0, scale_h=1.0)
            
        level_obj.oh_level = level.cpu()
        level_obj.scales = scales
        level_obj.noises = noises

        level_obj.ascii_level = one_hot_to_ascii_level(level, generator.token_list)

        with open(f"{save_path}/level_{i}.txt", "w") as f:
            for line in level_obj.ascii_level:
                f.write(line)

        print(f"Level {i+1} generated successfully")
        levels.append(level)
    return levels

def main():
    try:
        # Load the generator from the specified directory
        generator_list = sorted(os.listdir(generators_path))

        for generator in generator_list:
            print(f"Generaing levels for {generator}")

            generator_path = os.path.join(generators_path, generator)

            # Load the generator
            toadgan_obj = load_generator(generator_path)

            # Path to save the generated levels
            save_path = f"levels/generated/lvl_{generator.split('_')[-1]}"

            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            # Generate levels and save them to the levels/generated directory
            generate_levels(toadgan_obj, save_path, num_levels=10)
        
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
