# steg2
steg2 - Store and extract files hidden within images (with better performance)

## Description
This tool take files, convert them to raw data (octal) and inserts this data into the least-signficant-digit of an image's pixel rgb-data.

## Dependencies
* Requires Pillow (tested with version 5.4.1) 
```pip
pip install pillow
```
* Python 3.0+
* Tested on ArchLinux

## Usage
From help page:
```
Usage: 
    python steg.py [image] [command] [file ..] [arg ..]

Basic Examples:
    python steg.py image.png encode text.txt -o encoded.png
    python steg.py encoded.png decode -dir output

Commands:
    help            Display this help page
    encode          Encode [file ..] into [image] 
    decode          Decode file(s) from [image] 
    details         Show's how much data can fit into [image]
    
Arguments recognised by encode:
    -o [file]       Set output name for encoded image
    -noblend        Encoder will stop when reaching end of files
                      (leaves visible tearing on image)
    -visible        Explicitly show the separator pixel (debugging)

Arguments recognised by decode:
    -dir [file]     Set output directory for decoded files
```
