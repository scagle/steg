import traceback
import os
import sys
from PIL import Image

fileDir = os.path.dirname(os.path.realpath('__file__'))
separator = 2
def binary_to_bytes(string):
    bytefiles = []
    lastlocation = 0
    try:
        for by in range(len(string)//8):
            lastlocation = by 
            bytefiles.append(bytes([int(string[by*8 : by*8 + 8], 2)]))
    except IndexError:
        print("Index out of bounds!")
    except ValueError:
#        traceback.print_exc()
        if (lastlocation >= 2):
            sys.exit("*** Got through some of the data, but reached invalid bit.\n  Here are the last two bytes:\n    "+string[lastlocation*8-8 : lastlocation*8+8]+"\n*** Maybe the separator is incorrect?")
        else:
            sys.exit("*** Found no data\n*** Maybe the image doesn't have any stored data?")
    return bytefiles

def decrypt(image, sep=2, outDir=""):
    print("==> Attempting to decrypt", os.path.basename(image))
    separator = sep
    im = Image.open(image)
    px = im.load()
    data = ""
    try:
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                t = px[x, y]
                r = str(t[0])[-1]
                g = str(t[1])[-1]
                b = str(t[2])[-1]
                data += r
                data += g
                data += b
                if ((r == str(separator+1)) or (g == str(separator+1)) or (b == str(separator+1))):
                    data = data[:data.find(str(separator+1))-1]  #because there's a '56' at the very end and we don't want either one
                    raise(Exception)
    except(Exception):
        pass 
    name_and_filedata = data.split(str(separator))
    names = []
    filedata = []
    for i, seg in enumerate(name_and_filedata):
        if (i % 2 == 0): # if even then its a name of a file
            namebytes = binary_to_bytes(seg)
            name = "".join(namebytes[i].decode("utf-8") for i in range(len(namebytes)))
            names.append(name)
        else: # if its odd then it's data
            filedata.append(seg)
    warnings = 0
    try:
        if (len(filedata) == 0):
            raise ValueError
        for i, binary in enumerate(filedata):
            if binary != "":
                if (len(binary) % 8 == 0):
                    bytefiles = binary_to_bytes(binary)
                    filename = os.path.join(fileDir, names[i])
                    if outDir != "":
                        filename = os.path.join(fileDir, outDir)+"/"+names[i]
                    with open(filename, 'wb') as f:
                        for by in bytefiles:
                            f.write(by)
                else:
                    warnings += 1
                    print("*** Warning: Can't read file")
            else:
                warnings += 1
                print("*** Warning: Empty File")
    except ValueError:
        print("Seperator", separator)
        sys.exit("*** Can't find file(s), either no data or incorrect separator")
    except:
        print("*** Decryption Failed")
        traceback.print_exc()
    else:
        print("==> Finished decrypting. Found and saved these files:\n==>   ", "\n==>    ".join(os.path.join(fileDir, outDir+"/"+name) for name in names))
        if (warnings > 0):
            print("==> There was", warnings, "warnings!!!")
