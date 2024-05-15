from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def tile_and_quantize_image(image_path, tile_size=8, num_tiles=64, num_colors=16):
    # Open the image
    img = Image.open(image_path)
    img = img.convert('RGB')

    # Resize the image to be a multiple of the tile size
    width, height = img.size
    img = img.crop((0, 0, width - width % tile_size, height - height % tile_size))
    width, height = img.size

    # Convert image to NumPy array
    img_array = np.array(img)

    # Break the image into tiles and flatten each tile
    tiles = []
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            tile = img_array[y:y + tile_size, x:x + tile_size]
            tiles.append(tile.flatten())

    # Apply KMeans to find the most common tiles
    tile_kmeans = KMeans(n_clusters=num_tiles, random_state=0).fit(tiles)
    unique_tiles = tile_kmeans.cluster_centers_.astype('uint8')

    # Reconstruct the image with the most common tiles
    new_img_array = np.zeros_like(img_array)
    tile_idx = 0
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            label = tile_kmeans.labels_[tile_idx]
            tile = unique_tiles[label].reshape(tile_size, tile_size, 3)
            new_img_array[y:y + tile_size, x:x + tile_size] = tile
            tile_idx += 1

    # Dithering matrix for ordered dithering
    bayer_matrix_8x8 = np.array([
        [0, 48, 12, 60, 3, 51, 15, 63],
        [32, 16, 44, 28, 35, 19, 47, 31],
        [8, 56, 4, 52, 11, 59, 7, 55],
        [40, 24, 36, 20, 43, 27, 39, 23],
        [2, 50, 14, 62, 1, 49, 13, 61],
        [34, 18, 46, 30, 33, 17, 45, 29],
        [10, 58, 6, 54, 9, 57, 5, 53],
        [42, 26, 38, 22, 41, 25, 37, 21]
    ]) / 64.0

    def ordered_dither(image_array, dither_matrix):
        height, width, _ = image_array.shape
        dithered_image = np.zeros_like(image_array)
        for y in range(height):
            for x in range(width):
                threshold = dither_matrix[y % 8, x % 8]
                for c in range(3):
                    old_value = image_array[y, x, c] / 255.0
                    new_value = np.floor(old_value * 7 + threshold) / 7
                    dithered_image[y, x, c] = np.round(new_value * 255)
        return dithered_image

    # Apply ordered dithering
    dithered_img_array = ordered_dither(new_img_array, bayer_matrix_8x8)

    # Flatten the dithered image array for color quantization
    pixels = dithered_img_array.reshape(-1, 3)

    # Apply KMeans clustering to limit the number of colors
    color_kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(pixels)
    limited_colors = color_kmeans.cluster_centers_.astype('uint8')
    labels = color_kmeans.labels_

    # Reconstruct the image with the limited colors
    final_img_array = limited_colors[labels].reshape(dithered_img_array.shape)

    # Round each color to the nearest 3 bits per channel color
    def round_to_nearest_3_bits(color):
        return (color // 32) * 32

    final_img_array = np.apply_along_axis(round_to_nearest_3_bits, axis=2, arr=final_img_array)

    # Debug: Check the number of unique colors in the final image
    unique_colors_final = np.unique(final_img_array.reshape(-1, 3), axis=0)
    print(f"Unique colors in final image: {len(unique_colors_final)}")

    # Convert NumPy array back to an image
    final_img = Image.fromarray(final_img_array.astype('uint8'))
    return final_img

# Define the main function
def main():
    input_image_path = 'tiny arnold IN.png'
    output_image_path = 'output_dithered_quantized_image.png'

    # Tile and quantize the image, then save the output image
    quantized_image = tile_and_quantize_image(input_image_path, tile_size=8, num_tiles=1024, num_colors=16)
    quantized_image.save(output_image_path)
    print(f'Dithered and quantized image saved as {output_image_path}')

# Run the main function
if __name__ == '__main__':
    main()
