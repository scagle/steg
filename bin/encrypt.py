import traceback
import sys
import os
from PIL import Image


class EOF(Exception):
    def __init__(self, start, currentRGB):
        self.start = start
        self.currentRGB = currentRGB

def modifyRGB(px, pos, currentRGB, bit):
    if bit != 'random':  # Two modes: encrypt data, and apply random bits to the rest of the picture for camouflaging purposes
        prev = px[pos[0], pos[1]]
        color = str(prev[currentRGB])
        changedcolor = int( color[:len(color)-1] + str(bit) )
        if currentRGB == 0:
            px[pos[0], pos[1]] = (changedcolor, prev[1], prev[2])
        elif currentRGB == 1:
            px[pos[0], pos[1]] = (prev[0], changedcolor, prev[2])
        elif currentRGB == 2:
            px[pos[0], pos[1]] = (prev[0], prev[1], changedcolor)
    else:
        prev = px[pos[0], pos[1]]
        color = str(prev[currentRGB])
        if ((prev[0]+prev[1]+prev[2]) % 2 == 0):
            changedcolor = int( color[:len(color)-1] + "0")
        else:
            changedcolor = int( color[:len(color)-1] + "1")
        if currentRGB == 0:
            px[pos[0], pos[1]] = (changedcolor, prev[1], prev[2])
        elif currentRGB == 1:
            px[pos[0], pos[1]] = (prev[0], changedcolor, prev[2])
        elif currentRGB == 2:
            px[pos[0], pos[1]] = (prev[0], prev[1], changedcolor)

def get_bits(f, name):
    namebytes = bytearray(name, 'utf-8') # an array of ascii point integer values EX: [94, 80, 102]
    for byte in namebytes:
        for i in reversed(range(8)):
            yield ((byte >> i) & 1)

    yield separator

    byte = f.read(1)
    while (byte != b''):
        decimal = int.from_bytes(byte, byteorder="little") # Requires you to run python 3 or higher
        for i in reversed(range(8)):
            yield ((decimal >> i) & 1)
        byte = f.read(1)
    yield -1

def get_data(data):
    for b in data:
        yield b
    yield ""

def encrypt_file(files, px, end, blend):
    data = "";
    for fil in files:
        print("==> Making binary data for " + os.path.basename(fil) + "...")
        with open(os.path.join(fileDir, fil), 'rb', buffering = 0) as f:
            try:
                bitgen = get_bits(f, os.path.basename(fil))
                b = next(bitgen)
                place = 1
                while (b != -1):
                    data += str(b)
                    b = next(bitgen)
                data += str(separator)
            except Exception as e:
                traceback.print_exc()
    try:
        print("==> Finished making binary data\n==> Starting encryption...")
        data += str(separator+1)
        bitgen = get_data(data)
        b = next(bitgen)
        done = False
        while (b != ""):
            for x in range(end[0]):
                for y in range(end[1]):
                    for rgb in range(3):
                        if b != "":
                            modifyRGB(px, (x, y), rgb, b)
                            b = next(bitgen)
                        else:
                            if (done == False):
                                print("==> Reached the end of encryption!")
                                done = True;
                                if blend: # only prints once
                                    print("==> Blending the rest of the picture...")
                            if blend:
                                modifyRGB(px, (x, y), rgb, 'random')
            if b != "":
                sys.exit("Image is not big enough to fit all the files!!")
            else:
                raise EOF((x, y), rgb) # My own custom exception to stop the process safely
    except:
        raise

def checkSize(pixels, files):
    total = len(files)*2  # starts out with this to account for separators (there's not too many of them but if you have a bunch of files it matters)
    for f in files:
        total += os.path.getsize(f)
    maximum = ((pixels[0] * pixels[1]) * 3) // 8
    if total <= maximum:
        return None
    else:
        return (total, maximum)
separator = 2
fileDir = os.path.dirname(os.path.realpath('__file__'))
def encrypt(image, files, sep = 2, blend=True, outFile=""):
    separator = sep
    im = Image.open(image)
    copy = im.copy()
    px = copy.load()
    valid = checkSize(im.size, files)
    if valid != None:
        sys.exit("*** The files are too big for this image.\n  Your files:  "+ str(valid[0]) + " bytes\n  Image's max: " + str(valid[1]) + " bytes")
    end = (im.size[0], im.size[1])
    try:
        encrypt_file(files, px, end, blend)
    except EOF as e:
        newname = os.path.basename(image)
        newname = "e"+newname[:newname.find('.')] + ".png"
        if outFile != "":
            newname = os.path.join(fileDir, outFile)
        print("==> Saving image as " + newname + " (as PNG)")
        #copy.save(os.path.basename(newname), "TIFF", save_all = True, compression='None')
        copy.save(os.path.basename(newname), "PNG", compress_level=0, optimize=True)

        #if im.format == "TIFF":
        #    copy.save("e"+os.path.basename(image), im.format, save_all = True, compression='None')
        #elif im.format == "JPG":
        #    copy.save("e"+os.path.basename(image), im.format, compression='None', quality = 95, subsampling="keep")
        #else:
        #    print("UNSUPPORTED IMAGE FORMAT")

        start = e.start
        currentRGB = e.currentRGB
    except StopIteration:
        print("*** Stopped Iteration for unknown reason")
        traceback.print_exc()
    except Exception as e:
        print("*** Unknown exception:")
        traceback.print_exc()

