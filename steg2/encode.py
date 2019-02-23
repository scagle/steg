from pathlib import Path
from PIL import Image
import os
import sys


# 8 = separator, 9 = end
def get_files_obits(files):
    for fil in files:
        if fil is not files[0]:
            yield 8
        name_bytes = bytearray(Path(fil).name, 'utf-8')
        for byte in name_bytes: 
            octal = [int(x) for x in list('{0:03o}'.format(byte))]
            for obit in octal:
                yield obit
        yield 8
        with open(fil, 'rb') as f:
            byte = f.read(1)
            while byte:
                octal = [int(x) for x in list('{0:03o}'.format(ord(byte)))]
                for obit in octal:
                    yield obit 
                byte = f.read(1)
    yield 9
    yield 'Done'

def get_file_sizes(files):
    total_bytes = 0
    for f in files:
        total_bytes += os.path.getsize(f)
    return total_bytes

def encode(image, files, **options):
    if len(files) == 0:
        print('No files were supplied')
        return
    print('Loading Image!')
    px = image.load()
    print('Converting file to octal bits!')
    bits = get_files_obits(files)

    #octal_size = int(get_file_sizes(files) * 3)  # I use 3 octal numbers for every byte (not 2.6666666) 
    #update_interval = int(octal_size/10)
    #current_interval = 0
    #print('|          |', end='\r')

    try:
        import random
        blending = False
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                rgb = list(px[x, y])
                for i, color in enumerate(rgb):
                    # NOT WORTH 0.3 SEC SLOWDOWN
                    #current_interval += 1
                    #if current_interval % update_interval == 0:
                    #    tenths = int(current_interval/update_interval)
                    #    print('|' + '#'*tenths + ' '*(10-tenths)+'|', end='\r')
                    if blending:  # If done and blending
                        bit = int(random.random()*8)
                    else:
                        bit = next(bits)
                    if not blending and (bit == 8 or bit == 9):
                        rgb[i] = bit
                        continue
                    if bit == 'Done':
                        if options['noblend'] == False:
                            bit = int(random.random()*8)
                            print('Finished encoding, blending rest of picture...')
                            blending = True
                        else:
                            px[x, y] = tuple(rgb)
                            raise StopIteration
                    rgb[i] = color - (color % 10) + bit
                    diff = color - rgb[i]
                    if diff > 5:
                        if rgb[i] > 10:
                            rgb[i] -= 10
                    elif diff < -5:
                        rgb[i] += 10
                    if rgb[i] > 255:
                        rgb[i] -= 10
                px[x, y] = tuple(rgb)
        print('Reached end of file')
    except StopIteration:
        print('                            ', end='\r')  # Flushes progress bar
        print('Done with files')
        print('==> ' + '\n==> '.join(Path(fi).name for fi in files))
    print("Saving encoded image as '%s'" % options['out'])
    image.save(options['out'], 'PNG')
