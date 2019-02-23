from pathlib import Path
from PIL import Image
import sys
import os
import copy

import encode as enc 
import decode as dec

if len(sys.argv) < 3:
    print('Not enough arguments')
    print('python steg.py [image] [command] [files] ?[args]')
    sys.exit()

try:
    image = sys.argv[1]  # Image.jpg
    with Image.open(image) as img:
        width, height = img.size
except Exception as e:
    print('*** Invalid image')
    raise e

command = sys.argv[2] # encode, decode, etc
args = sys.argv[3:] 

# Tests files to verify integrity, and to verify if they will fit into image

def testfiles(args):
    files = copy.deepcopy(args) # Left over arguments should now just be files
    totalsize = 0  # in bytes
    for filepath in args:  # Test files
        path = Path(filepath)
        name = Path.name
        if path.exists() == False:
            print('*** "%s" does not exist!!!' % filepath)
            sys.exit()
        if path.is_file() == False:
            print('*** "%s" is not a file!!!' % path)
            ignore = input('Ignore and continue? y/n')
            if ignore != 'y': 
                sys.exit()
            files.remove(filepath)
        totalsize += os.path.getsize(filepath) + len(path.name)
    totalsize += len(args)*2  # number of '8' or '9' separators which also require space
    num_octals = (totalsize * 8) / 3  # number of octals required to store bytes
    space = (width * height) * 3  # number of spaces to place octals
    if num_octals > space:
        print('*** Picture isn\'t big enough!!!\nPicture can store %d octals!\nYou supplied %d octals!' % (space, num_octals))
        sys.exit()
    return files


def encode():
    options = {'out':None,
               'noblend':True,
               'show_separations':False}
    if '-o' in args:
        i = args.index('-o')
        try:
            out = args.pop(i+1)  # Takes next argument afterwards which is name of output picture
            args.pop(i)  # Removes option from args, as we are done with it now
            options['out'] = out
            if '.' not in out:
                print('Saving "%s" as PNG' % out)
                options['out'] = out+'.png'
        except Exception as e:
            print('*** Error when interpreting "-o"')
            raise e
    if '-noblend' in args:
        i = args.index('-noblend')
        args.pop(i)  # Removes option from args, as we are done with it now
        options['noblend'] = False
    if '-visible' in args:
        i = args.index('-visible')
        args.pop(i)  # Removes option from args, as we are done with it now
        options['show_separations'] = True
    for arg in args:
        if arg[0] == '-':
            print('*** Invalid option "%s"' % arg)
            sys.exit()

    files = testfiles(args)
    with Image.open(image) as im:
        print('Encoding %s' % image)
        enc.encode(im, files, **options)


def decode():
    options = {'directory':'Output'}
    if '-dir' in args:
        i = args.index('-dir')
        directory = args.pop(i)
        if Path(directory).exists() == False:
            print('*** Directory "%s" does not exist!!!' % directory)
            sys.exit()
        if Path(directory).is_file():
            print('*** "%s" is a file, not a directory!!!' % directory)
            sys.exit()
        options['directory'] = directory 

    with Image.open(image) as im:
        dec.decode(im, **options)

if command == 'encode':
    encode()
elif command == 'decode':
    decode()
else:
    print('***UNKNOWN COMMAND "%s"' % command)
