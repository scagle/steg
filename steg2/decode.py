from pathlib import Path
from PIL import Image
import sys

def get_image_obits(image):
    px = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            rgb = list(px[x, y])
            for i, color in enumerate(rgb):
                if (color % 10) == 9:
                    return
                yield color % 10

def decode(image, **options):
    print('Getting Image Octal Bits!')
    obits = get_image_obits(image)
    data = ''.join(str(s) for s in obits)
    segments = data.split('8')
    names = []
    datas = []
    print('Converting Octal Bits to bytes!')
    # NAMES
    for i in range(0, len(segments), 2):
        name_bytes = octs_to_bytes(segments[i])
        names.append(''.join(chr(byte) for byte in name_bytes))
    # DATAS
    for i in range(1, len(segments), 2):
        datas.append(octs_to_bytes(segments[i]))
    for name, data in zip(names, datas):
        with open(options['directory']+'/'+name, 'wb+') as f:
            f.write(bytes(data))
    print('Found:')
    print('==> '+'\n==> '.join(names))
    print('Saved in %s/' % options['directory'])


def octs_to_bytes(segment):
    data = []
    char_byte = ''
    for c in segment:
        char_byte += c
        if len(char_byte) == 3:
            data.append(int(char_byte, 8))
            char_byte = ''
    assert len(char_byte) == 0, 'Invalid image'
    return data
