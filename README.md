# QuantizeMD

These scripts can be used to limit an RGB image in both colour count and tile count. 
Tiles can be thought of as unique grid contents - ie, a 256x256 image might be divided into 8x8 tiles (32 tiles by 32 tiles, 1024 tiles total), with many of those tiles repeated.
Tiles are NOT exported. The output is an image, but made up of tiles.


## Contents

### Scripts
 - quantize_image.py - just quantizes for tile count. Output is RGB. Use this is you don't want to limit colours, or want to reduce the palette as part of your own post processing
 - quantize_3bp.py - as above, but will also reduce palette, dither the image, and snap the colours to 3 bits per channel. Use this is you want to spit out Mega Drive ready images

### Image Examples

* FG1 IN - an image of forest from above. The image tiles, but there's no tiling within the image.
  * FG1 out - 64 tiles
  * FG1 3bp - 64 tiles, 16 colours all from the Mega Drive palette
* FG4 IN - similar to FG1 but with adjusted levels. Doesn't affect anything here; just the version I was playing with when I made an edit to these scripts
  * FG4 out H - horizontal style dithering
  * FG4 out V - vertical style dithering
  * FG4 out - bayer dithering
  * FG4 out 0 - no dithering. The triangles aren't from the dithering. It's just a pattern than can occur with tile counts
  * FG4 out CD - clistered dot dithering
*  BG1 IN - A top down tiling image of forest floor showing paths and buildings. There are several tiles shown. Those tiles are multiples of 8 in size, so condense efficiently using these scripts
  * Same outputs as previous. Notice how the tiles repeat.
* tin arnold IN - an turnaround image of a 3D figure
  * outputs at 16, 32, 64, 128, 256, 512, and 1024 tiles to show the effect of reducing tile count as an image compression technique. These are all created using quantize_3bp at 16 colours.


## Installation

I use Windows. YMMV

1. Install Python - open CMD and type "Python" and you'll be given a link to install Python through the Windows store. Or go to the Windows store directly
2. Set up environment
   1. Navigate to this folder
   2. `python -m venv myenv`
3. Start environment - `myenv\Scripts\activate`
4. Install libraries - `pip install pillow numpy scikit-learn`
5. Run one of the scripts - they both currently point at an image in this folder
   * `python quantize_image.py`
   * `python quantize_3bp.py`


## Edit The Scripts

* `input_image_path` in main to change the image you want to run the script on
* Look for the `tile_image` call in main
  * `tile_size` with and height of tiles
  * `num_tiles` number of unique tiles
  * `num_colors` (`quantize_3bp.py` only) palette size
  * `dither_type` (`quantize_3bp.py` only) dithering style (see FG4 images)
