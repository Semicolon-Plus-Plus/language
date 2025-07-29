import sys, os
from converter import Converter


inFile = ""
outFile = ""
platform = ""

try:
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    platform = sys.argv[3]
    
except Exception:
    print("Use this command with these arguments (without '-'): 'IN_FILE OUT_FILE PLATFORM'")
    exit(1)

Converter.convert(inFile, outFile, platform)

#Compile the transpiled source code
if (platform == Converter.allowedPlatforms[0]):#linux
    os.system(f"g++ { outFile } -o spp_exec")

#
    
print("Finished!")