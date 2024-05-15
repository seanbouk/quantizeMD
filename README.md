# QuantizeMD

These scripts can be used to limit an RGB image in both colour count and tile count. 
Tiles can be thought of as unique grid contents - ie, a 256x256 image might be divided into 8x8 tiles (32 tiles by 32 tiles, 1024 tiles total), with many of those tiles repeated.
Tiles are not exported. The output is an image, but made up of tiles.

## Contents

### Scripts
 - quantize_image.py - reduces palette size and quantizes to a limited number of tiles. You can difine palette size, tile size, and number of unique tiles
 - quantize_3bp.py - as above, but will snap all colours to a 3 bit per channel RGB palette

### Image Examples
* FG1 IN.png - a tiling image of forest from above. Input for the images created below
  * FG1 64 16.png - 64 8x8 tiles, 16 colours
  *  FG1 64 16 3BP.png - as above, but to a 3bit RGB palette
*  BG1 IN - A top down tiling image of forest floor showing paths and buildings. There are several tiles shown. Those tiles are multiples of 8 in size, so condense efficiently using these scripts
  * Same outputs as previous
* red fruit IN.png - an AI generated bowl of red fruit. When using the 3bit script, colours will clash
