import os
from PIL import Image
import sys
from encrypt import encrypt
from decrypt import decrypt
import traceback
import imghdr

commands = {
        "details :  python3 [this_file] details [image]" : "Display the details of a supplied image, and see how much data it can store",
        "encrypt :  python3 [this_file] encrypt [image] [file1, *file2, ..., *file2] [*-o] [*-noblend] [*-seperator=]" : "Takes a list of files (works with most formats), converts them into bytes and binary, which is then overlayed onto the supplied image's RGB color data",
        "decrypt :  python3 [this_file] decrypt [image] [*-dir]" : "Takes an image and tries its best to extract data from an image who's data has been overlayed in the least significant digit of the RGB data. It saves the files found in ./decrypted",
        "help    :  python3 [this_file] help"    : "Help page"
        }

seperator = 2 # which number will seperate the sets 55of data in the encryption
fileDir = os.path.dirname(os.path.realpath('__file__'))
args = sys.argv # the first element is always the name of this file

def rec():
    return "\n==> Maybe you wanted these?\n  python "+args[0]+" details [image]\n  python "+args[0]+" encrypt [image] [*files]\n  python"+args[0]+" decrypt [image]"

if 'PIL' in sys.modules == False:
    sys.exit("This library requires PIL library in order to operate. Please install it before using this tool.\n    http://www.pythonware.com/products/pil/")
if 'encrypt' in sys.modules == False:
    sys.exit("Missing encrypt.py from source code")
if 'decrypt' in sys.modules == False:
    sys.exit("Missing decrypt.py from source code")

if (len(args) > 2):
    if (args[1] == "details"):
        imgType = imghdr.what(os.path.join(fileDir, args[2])) # returns an image type (IE: tiff, jpeg, png, etc)
        if imgType == None:
            sys.exit("*** "+args[2] + " has an image format not recognized by PIL")
        image = os.path.join(fileDir, args[2])
        try:
            im = Image.open(image)
            b = str((im.size[0]*im.size[1]*3)//8) #bytes
            kb = str(int(b) // 1024)
            mb = str(int(kb) // 1024)
            print("==> Max amount of data that can be stored:\n  " + b + " bytes\n  "+ kb + " kilobytes\n  " + mb + " megabytes")
        except(IOError):
            print("*** '" + image + "' can not be read")
        except:
            traceback.print_exc()
    elif (args[1] == "encrypt"):
        blend = True
        if "-noblend" in args:
            blend = False
            args.remove("-noblend")
            print("^^^ Set blend to false!")
        outFile = ""
        try:
            out = args.index("-o")
        except ValueError:
            pass
        else:
            args.remove("-o")
            if out < len(args):
                outFile = args[out]
                args.remove(outFile)
                print("^^^ Going to save as " + os.path.join(fileDir, outFile))
        for arg in args:
            if "-seperator=" in arg:
                seperator = arg[arg.find("=")+1:] 
                if ((len(seperator) == 1) and (seperator.isdigit()) and (int(seperator) > 1)):
                    if (seperator == "9"):
                        sys.exit("*** Sorry, seperator can't be 9, has to be 0-8 (annoying temporary problem)")
                    args.remove(arg)
                    print("^^^ Set seperator to", seperator)
                else:
                    sys.exit("Invalid seperator")
        if (len(args) > 3):
            filepaths = [os.path.join(fileDir, f) for f in args[3:]]
            image = os.path.join(fileDir, args[2])
            encrypt(image, filepaths, sep=int(seperator), blend=blend, outFile=outFile)
            print("==> Encryption Successful")
        else:
            print("==> Error: not enough arguments"+ rec())
    elif (args[1] == "decrypt"):
        outDir = ""
        try:
            out = args.index("-dir")
        except ValueError:
            pass
        else:
            args.remove("-dir")
            if out < len(args):
                outDir = args[out]
                args.remove(outDir)
                print("^^^ Setting output directory to " + os.path.join(fileDir, outDir))
        for arg in args:
            if "-seperator=" in arg:
                seperator = arg[arg.find("=")+1:] 
                if ((len(seperator) == 1) and (seperator.isdigit()) and (int(seperator) > 1)):
                    if (seperator == "9"):
                        sys.exit("*** Sorry, seperator can't be 9, has to be 0-8 (annoying temporary problem)")
                    args.remove(arg)
                    print("^^^ Set seperator to", seperator)
                else:
                    sys.exit("Invalid seperator")
        if (len(args) > 2):
            image = os.path.join(fileDir, args[2])
            if ((outDir != "") and (outDir[-1] == "/")):
                outDir = outDir[:len(outDir)-1]
            decrypt(image, sep=int(seperator), outDir=outDir)
            print("==> Decryption Successful")
        else:
            print("==> Error: not enough arguments"+ rec())
elif (len(args) > 1):
    if (args[1] == "help"):
        print("\nThis is a steganography tool used to encrypt and decrypt files in images with a very specific pattern.")
        print("Heres a list of the commands:\n  - " + "\n\n  - ".join((c + "\n    - " + commands[c]) for c in sorted(commands)))
        print()
else:
    print("==> Too few arguments" + rec())
