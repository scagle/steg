# hidimg
imghid - Store and extract files hidden within images

Inspired by:
  http://www.pythonchallenge.com/
  http://puzzling.stackexchange.com/
and other puzzle websites that commonly use ciphers and steganography to hide clues and 
solutions within images. 
I also have always wanted to make a command line tool. (Even though the python nature
of this tool has made it quite unorthodox)

NAME

    imghid - Store and extract files hidden within images

DEPENDENCIES

    This requires PIL (Pillow) in order to operate because it opens/reads/writes/saves 
    images.

    Python 3.0+

    Unix based OS / Not Windows. Made and tested on Mac OS X 10.10, will most likely work 
    on Linux based operating systems as well. Won't work on Windows mostly because of 
    the "\" vs "/" conflicts for paths.

SYNOPSIS

    encrypt [-o] [-noblend] [-separator=#]
    decrypt [-dir] [-separator=#]
    details
    help

DESCRIPTION

    This is a steganography tool that can hide files within the color data of an image.
    It converts the supplied files into binary data which is spliced into the least
    significant digit (one's place) of the RED BLUE and GREEN values of each pixel 
    going down each column from left to right

    EX: data is 110, and original rgb of a pixel is (234, 87, 94) 
        after encoding (234, 87, 94) will become (231, 81, 90)

COMMANDS:

    In the following descriptions, * means optional.

    encrypt [image] [file1, *file2, ...]
        Encodes an image with files of various types of files. (.txt, .jpg, .zip, .pdf, ...)
        Will save encrypted image as same image with a pre-pended "e" if no -o is specified.
        -o              :   (out) path/name to save the encoded image as

        -noblend        :   stops the encoder from "blending" the rest of the image after it 
                            is finished with the data. Blending helps camouflage data.
                            Use when you want to see the block of data in the image.

        -separator=#:   :   tells the encoder what 0-8 digit to use to place in the least
                            significant digit of the RGB values when separating the files
                            from one another. Defaults to 2 (Not super useful)

    decrypt [image]
        Decodes an image with hidden data inside. Saves files into your current directory
        if no location is set. (Will overwrite without permission)
        -dir            :   tells the decoder where to store files found inside image
        -separator=#    :   tells the decoder what 0-8 digit to read when it reaches the
                            end of a block of data, so that it can keep files seperated.
                            Defaults to 2

    details [image]
        Provides the data about the image such as how much data (bytes, kilobytes, ...) it
        can store.

    help
        Displays basic unhelpful help page

EXAMPLES 

    From inside imghd-master/ 
    >> python3 bin/hidimg.py encrypt test.jpg *.txt -noblend -o output.png
    >> python3 bin/hidimg.py decrypt test.jpg -dir randomDirectory
    
    Crazy, but still valid example:
    >> python3 bin/hidimg.py encrypt -o output.png test.jpg -separator=6 ../Stuff/*.txt -noblend ../Stuff/*.zip 
