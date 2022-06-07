# Procedural-Artist
Use Python Threads to concurrently create a procedural painting. 

# Full Description

Imagine you have several great artists who want to collaborate on a giant painting using an algorithm. 
These artists are particularly picky, and they do not want their great artworks to overlap. 
They also all want to be able to start at a unique position on their painting, and paint as much of the pixel map as possible.

# Constraints

* You will create and load (using PIL) a 512 × 512 image called canvas.jpg filled with white pixels (RGB tuple of 255, 255, 255).
* Each thread (which represents an individual artist) is assigned a unique color for their brush (as an RGB tuple), but no artist is assigned the color white.
