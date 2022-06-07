#!/usr/bin/env python

'''
    Author: Mico Theogene Micomyiza
    Date: Feb 23rd 2022
    Course: CS 21, Concurrent programming

    There's synchronization among the threads. This is because
    after each thread is completed, we will wait for all
    other to completed in order to save the results to
    output file.

'''


from ast import Num
from concurrent.futures import thread
import sys
from turtle import width
from PIL import Image
import threading

from numpy import imag

PIX_MAP = []
MAX_THREADS = 1000
IMAGE_LOC    = threading.Lock()


def switch_r_b(rgb):
    '''
        Switches r and b in the tuple which turns image to blue

        Parameters
        ----------
        (r,g,b): tuple

        Return:
        (b,g,r): tuple
    '''
    return (rgb[2], rgb[1], rgb[0])
    

def gray(rgb):
    '''
        Grayscale the pixel, turns image to gray

        scale = (0.299 * r) + (0.587 * g) + (0.114 * b)

        Parameters
        ----------
        (r,g,b): tuple

        Return:
        (scale,scale, scale): tuple
    '''
    scale = int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
    return (scale, scale, scale)


def switch_r_g(rgb):
    '''
        Switches r and g in the tuple
        which turns image to green

        Parameters
        ----------
        (r,g,b): tuple

        Return:
        (g,r,b): tuple
    '''
    return (rgb[1], rgb[0], rgb[2])


def brightness(rgb):
    '''
        increase brightness of image
        by 85%

        Parameters
        ----------
        (r,g,b): tuple

        Return:
        (r,g,b): tuple
    '''
    r = min(255, rgb[0] *1.85)
    g = min(255, rgb[1] *1.85)
    b = min(255, rgb[2] *1.85)

    return (r,g,b)

def transformer(transform, row_start, row_end, col_start, col_end):
    '''
        Transform pixels in a subimage

        Parameters:
        ----------
        transform: str (transformation to perform)
        row_start: int (row index to start on )
        row_end : int (row index to end on )
        col_start : int (col index to start on )
        col_end : int (col index to end on )

        Side effect:
        -----------
        updates the original image
    '''
    global PIX_MAP
    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            IMAGE_LOC.acquire()
            try:
                curr_rgb = PIX_MAP[i, j]
                PIX_MAP[i, j] = transform(curr_rgb)
                IMAGE_LOC.release()
            except:
                # print("problem: {} {}".format(i, j))
                IMAGE_LOC.release()
    

def controller(image,output_file, transform, rows, cols):
    '''
        creates and runs the threads to transform the image

        Parameters:
        -------------
        image: Image (image to transform)
        output_file: str (file name to write the results)
        transform: accepted values [switch-r-b, switch-r-g, gray] 
        rows: int 
        cols: int

        it will generate cols x rows threads to handle cols x rows subimages
        where each thread handles 1 subimage

    '''
    global PIX_MAP
    # initiate PIX_MAP to the input image
    PIX_MAP = image.load()

    width, height = image.size
    row_partition = int(width / rows) + (width % rows)
    col_partition = int(height / cols) + (height % rows)
    
    # generate the threads
    threads = []
    for i in range(rows):
        row_start = i * row_partition
        row_end = (row_partition * (i + 1))
        for j in range(cols):
            col_start = j * col_partition
            col_end = (col_partition * (j + 1))
            curr_thread = threading.Thread(target=transformer, 
                    args=[transform,row_start, row_end, col_start, col_end])

            threads.append(curr_thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # write results to output file
    image.save(output_file)


def verify_argument(args):
    '''
        Verifys that the command line arguments match the expectation
        
        Parameters:
        -----------
        args: list (of arguments)

        Return:
        ----------
        input_image: Image
        output_file: str
        transform: str
        rows: int [default 2]
        cols: int [default 2]
    '''
    rows = 2
    cols = 2
    num_args = len(args) - 1
    if num_args < 3 or num_args == 4 or num_args > 5:
        print("Incorrect number of arguments")
        print("use: python transform_image.py inputfile outputfile " +
         "transform [optionals: x y]")
        exit(1)

    if num_args == 5:
        rows = int(args[-2])
        cols = int(args[-1])


    input_image = Image.open(args[1])
    output_file = args[2]
    transform_command = args[3]

    return input_image, output_file, transform_command, rows, cols


def main(args):
    '''
        Main function, takes in the arguments from command line
        and executes the transformation on image after
        verifying input
    '''
    # maps transform names to transform functions.
    transform_map = {
        "switch-r-b": switch_r_b,
        "switch-r-g": switch_r_g,
        "gray"      : gray,
        "brightness"  : brightness
    }

    # get verified arguments
    in_image, output_file, command, rows, cols = verify_argument(args)

    # check max threads variant isn't violated
    if (rows * cols) > MAX_THREADS:
        print("rows X cols = {} should not exceed {}".format(rows * cols,
            MAX_THREADS))
        exit(1) 

    # identify the transform to perform on the image
    if command in transform_map.keys():
        controller(in_image, output_file, transform_map[command], rows,
            cols)
    else:
        print("Unknown transform: ", command)
        exit(1)


if __name__ == '__main__':
    main(sys.argv)