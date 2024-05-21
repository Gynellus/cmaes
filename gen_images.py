import os
from utils.level_image_gen import LevelImageGen

# Define paths
level_paths = [
    # "levels/generated",
    # "levels/top_levels",
    # "levels/original",
    "levels/cmaes"
]

# Initialize LevelImageGen with the path to the sprites
sprite_path = "utils/sprites/"
level_image_gen = LevelImageGen(sprite_path)

# Define output directory
output_directory = "output_images"
os.makedirs(output_directory, exist_ok=True)

# Function to read ASCII level from a file
def read_level_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# Function to generate and save the image for a level
def generate_and_save_image(level_file_path, output_dir):
    level = read_level_file(level_file_path)
    level_image = level_image_gen.render(level)
    
    # Create a file name based on the relative path
    relative_path = os.path.relpath(level_file_path, start=os.getcwd())
    image_file_name = relative_path.replace(os.sep, '_').replace('.txt', '.png')
    image_output_path = os.path.join(output_dir, image_file_name)
    
    level_image.save(image_output_path)
    print(f"Generated image saved at {image_output_path}")

# Function to process each directory
def process_directory(directory, output_dir):
    if os.path.exists(directory):
        for root, _, files in sorted(os.walk(directory)):
            sorted_files = sorted(files)
            for file_name in sorted_files:
                if file_name.endswith(".txt"):
                    level_file_path = os.path.join(root, file_name)
                    generate_and_save_image(level_file_path, output_dir)
                    break  # Only process the first level file in each subdirectory
    else:
        print(f"Directory {directory} does not exist.")

# Generate images for levels in each defined path
for level_path in level_paths:
    if "original" in level_path:
        # Handle levels/original which has .txt files
        sorted_files = sorted(os.listdir(level_path))
        for file_name in sorted_files:
            if file_name.endswith(".txt"):
                level_file_path = os.path.join(level_path, file_name)
                generate_and_save_image(level_file_path, output_directory)
    else:
        # Handle subdirectories for generated and top_levels
        process_directory(level_path, output_directory)
