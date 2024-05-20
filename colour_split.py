from PIL import Image
from collections import Counter

def count_unique_colors(image):
    """Counts unique colors in an image."""
    pixels = list(image.getdata())
    return Counter(pixels)

def recolor_image(image, color_map):
    """Recolors an image based on a color mapping."""
    pixels = list(image.getdata())
    new_pixels = [color_map.get(pixel, pixel) for pixel in pixels]
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    return new_image

def main(image_path):
    image = Image.open(image_path)
    width, height = image.size

    # Count unique colors
    color_count = count_unique_colors(image)
    unique_colors = list(color_count.keys())
    
    if len(unique_colors) < 17 or len(unique_colors) > 31:
        print("The image needs to have between 17 and 31 unique colors.")
        return

    # Assign each color an index
    color_index = {color: i for i, color in enumerate(unique_colors)}

    # Create two copies of the image
    background_image = image.copy()
    foreground_image = image.copy()

    # Define the new colors for debugging
    background_replacement_color = unique_colors[0]  # Use the color at index 0
    foreground_replacement_color = (255, 0, 255)  # Magenta (0xFF00FF)

    # Create color maps for both images
    background_color_map = {color: (background_replacement_color if i >= 16 else color) for color, i in color_index.items()}
    foreground_color_map = {color: (foreground_replacement_color if i < 16 else color) for color, i in color_index.items()}

    # Recolor the images
    background_image = recolor_image(background_image, background_color_map)
    foreground_image = recolor_image(foreground_image, foreground_color_map)

    # Save the images
    background_image.save("background_image.png")
    foreground_image.save("foreground_image.png")
    print("Images saved successfully.")

# Example usage
main("output_dithered_quantized_image.png")
