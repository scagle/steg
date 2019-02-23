# steg1
(Formally known as imghid)
(This is old README for imghid)

imghid - Store and extract files hidden within images

NAME

    imghid - Store and extract files hidden within images

DEPENDENCIES

    Requires Pillow (tested with version 5.4.1) 
```pip
pip install pillow
```
    Python 3.0+
    Tested on ArchLinux

SYNOPSIS

    encrypt [-o file] [-noblend] [-separator=2-8]
    decrypt [-dir directory] [-separator=2-8]
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
        [-o file]       :   (out) path/name to save the encoded image as

        [-noblend]      :   stops the encoder from "blending" the rest of the image after it 
                            is finished with the data. Blending helps camouflage data.
                            Use when you want to see the block of data in the image.

        [-separator=#]  :   tells the encoder what 2-8 digit to use to place in the least
                            significant digit of the RGB values when separating the files
                            from one another. (Defaults to 2)

    decrypt [image]
        Decodes an image with hidden data inside. Saves files into your current directory
        if no location is set. (Will overwrite without permission)
        [-dir directory]  :   tells the decoder where to store files found inside image
        [-separator=#]    :   tells the decoder what 2-8 digit to read when it reaches the
                              end of a block of data, so that it can keep files seperated.
                              (Defaults to 2)

    details [image]
        Provides the data about the image such as how much data (bytes, kilobytes, ...) it
        can store.

    help
        Displays basic help page

EXAMPLES 

    From inside imghd-master/ 
    >> python3 bin/hidimg.py encrypt test.jpg *.txt -noblend -o output.png
    >> python3 bin/hidimg.py decrypt test.jpg -dir randomDirectory
    
    Crazy, but still valid example:
    >> python3 bin/hidimg.py encrypt -o output.png test.jpg -separator=6 ../Stuff/*.txt -noblend ../Stuff/*.zip 
