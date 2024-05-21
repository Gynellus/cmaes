from PIL import Image

# Paths to the images
image_paths = [
    "output_images/levels_original_lvl-1.png",
    "output_images/levels_top_levels_lvl_1-1_level_0_fitness_121.png",
    "output_images/levels_cmaes_lvl_1-1_best_level_0.png",
    "output_images/levels_generated_lvl_1-1_level_0.png"
]

# Open images and get their sizes
imgs = [Image.open(img) for img in image_paths]
widths, heights = zip(*(i.size for i in imgs))

# Calculate total width and max height
total_width = sum(widths)
max_height = max(heights)

# Create a new blank image with the correct size
new_img = Image.new('RGB', (total_width, max_height))

# Paste images into the new image
x_offset = 0
for img in imgs:
    new_img.paste(img, (x_offset, 0))
    x_offset += img.width

# Save the final merged image
new_img.save('output_images/merged_level_1-1.png')

# Display the image (optional)
new_img.show()
