# Cellular_Noise
A shader program to generate images with cellular noise (aso called Worley noise or Voronoi noise). 
Cellular noise is a method of generating a noise texture based on a pixel's distance to randomly placed nodes.
For more information, you can read the [wikipedia article](https://en.wikipedia.org/wiki/Worley_noise) on Worley noise.

## To Run
`python cellular.py <# of nodes> <distance metric>`
or
`python cellular.py list` for the list of distance metrics supported

### Supported metrics for you to try
* manhattan
* canberra
* chebyshev
* euclidean
* third_power
* forth_power
* half_power
* negative_power
* knights
* iron_cross
* octagon
* mod_euclidean
* mod_octagon
* mod_manhattan

## Key Bindings:
* `q` or `Ctrl+C` to exit
* `s` to save image to png. Filename will be a timestamp
* `i` toggle isolines
* `r` change to red channel
* `g` change to green channel
* `b` change to blue channel
* `u` "universal" channel i.e red,green and blue
* `w` reset
* `<` decrease brightness of current channel
* `>` increase brightness of current channel
* `1` change current channel to closest node
* `2` change current channel to second-closest node
* `3` change current channel to third-closest node
