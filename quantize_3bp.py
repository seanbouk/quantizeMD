from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def quantize_to_3bit_palette(image):
    """
    Quantize image colors to use only the 3 most significant bits of each channel.
    """
    img_array = np.array(image)
    
    # Create a mask for the 3 most significant bits (shift right by 5 bits and shift back)
    quantized_array = (img_array >> 5) << 5
    
    return Image.fromarray(quantized_array)

def quantize_tiles_with_3bit_palette(image_path, tile_size=8, num_tiles=2):
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGB')

    # Resize the image to be a multiple of the tile size
    width, height = img.size
    img = img.crop((0, 0, width - width % tile_size, height - height % tile_size))
    width, height = img.size

    # Quantize image to 3-bit per channel palette
    quantized_img = quantize_to_3bit_palette(img)
    quantized_img_array = np.array(quantized_img)

    # Break the image into tiles and flatten each tile
    tiles = []
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            tile = quantized_img_array[y:y + tile_size, x:x + tile_size]
            tiles.append(tile.flatten())

    # Apply KMeans to find the most common tiles
    tile_kmeans = KMeans(n_clusters=num_tiles, random_state=0).fit(tiles)
    unique_tiles = tile_kmeans.cluster_centers_.astype('uint8')

    # Reconstruct the image with the most common tiles
    new_img_array = np.zeros_like(quantized_img_array)
    tile_idx = 0
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            label = tile_kmeans.labels_[tile_idx]
            tile = unique_tiles[label].reshape(tile_size, tile_size, 3)
            new_img_array[y:y + tile_size, x:x + tile_size] = tile
            tile_idx += 1

    # Convert NumPy array back to an image
    new_img = Image.fromarray(new_img_array)
    return new_img

# Define the main function
def main():
    input_image_path = 'in4.png'  # Update with your image path
    output_image_path = 'output_quantized_image_3bit_palette.png'

    # Quantize the tiles with 3-bit palette and save the output image
    quantized_image = quantize_tiles_with_3bit_palette(input_image_path)
    quantized_image.save(output_image_path)
    print(f'Quantized image saved as {output_image_path}')

# Run the main function
if __name__ == '__main__':
    main()
