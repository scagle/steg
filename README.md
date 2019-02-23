# steg
steg - Store and extract files hidden within images

Inspired by:
  http://www.pythonchallenge.com/
  http://puzzling.stackexchange.com/
and other puzzle websites that commonly use ciphers and steganography to hide clues and 
solutions within images. 

## Description
These tools take files, convert them to raw binary (steg1), or raw octal (steg2) data and insert this data into the least-signficant-digit of an image's pixel rgb-data.

## Tools:
* steg1 - Version 1 (old)
* steg2 - Version 2 (recommended)

Biggest Difference is that steg1 uses binary numbers to store data into the pixels of images, while steg2 uses octal numbers

## Explanation
* ASCII:  "Hi" 
* Binary: 01001000 01101001 
* Octal:  44151

| raw-pixels   | steg1-pixels             | steg2-pixels             |
| ------------ | ------------------------ | ------------------------ |
| (100, 10, 1) | (10**0**, 1**1**, **0**) | (10**4**, 1**4**, **1**) |
| (100, 10, 1) | (10**0**, 1**1**, **0**) | (10**5**, 1**1**, 1)     |
| (100, 10, 1) | (10**0**, 1**0**, **0**) |                          |
| (100, 10, 1) | (10**1**, 1**1**, **0**) |                          |
| (100, 10, 1) | (10**1**, 1**0**, **0**) |                          |
| (100, 10, 1) | (10**0**, 1**1**, 1)     |                          |

## Dependencies
* Both require Pillow (tested with version 5.4.1) 
```pip
pip install pillow
```
* Python 3.0+
* Tested on ArchLinux

## Usage
For steg1 see [README](steg1/README.md)
For steg2 see [README](steg2/README.md)
