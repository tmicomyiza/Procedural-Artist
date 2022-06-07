# Procedural-Artist
Use Python Threads to concurrently create a procedural painting. 

# Full Description

Imagine you have several great artists who want to collaborate on a giant painting using an algorithm. 
These artists are particularly picky, and they do not want their great artworks to overlap. 
They also all want to be able to start at a unique position on their painting, and paint as much of the pixel map as possible.

# Constraints

* We create and load (using PIL) a 512 × 512 image called canvas.jpg filled with white pixels (RGB tuple of 255, 255, 255).
* Each thread (which represents an individual artist) is assigned a unique color for their brush (as an RGB tuple), 
    but no artist is assigned the color white.
    
* Each thread starts painting at a unique position in on the canvas, i. e., each artist (thread) gets a unique starting position and paints that pixel.
* NO two artists can paint a pixel at the same time
* If a pixel has been painted a non white color, it cannot be changed. i.e. artist cannot overwrite other artists work

# How to Run the program
procedural_artist.py -M number-of-threads -S number-of-steps

* number-of-threads = number of artists
* number-of-steps  = number of simulations to be run or number brush strokes each artist have
