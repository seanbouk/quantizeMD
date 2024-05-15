from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

def tile_image(image_path, tile_size=8, num_tiles=64):
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

    # Convert NumPy array back to an image
    new_img = Image.fromarray(new_img_array)
    return new_img

# Define the main function
def main():
    input_image_path = 'FG1 IN.png'
    output_image_path = 'output_tiled_image.png'

    # Tile the image and save the output image
    tiled_image = tile_image(input_image_path, 8, 64)
    tiled_image.save(output_image_path)
    print(f'Tiled image saved as {output_image_path}')

# Run the main function
if __name__ == '__main__':
    main()
