import sys, subprocess
from converter import Converter


inFile = ""
outFileCpp = ""
outFileExec = ""
platform = ""

try:
    inFile = sys.argv[1]
    outFileCpp = sys.argv[2]
    outFileExec = sys.argv[3]
    platform = sys.argv[4]
    
except Exception:
    print("Use this command with these arguments (without '-'): 'IN_FILE OUT_FILE_CPP OUT_FILE_EXEC PLATFORM'")
    exit(1)

Converter.convert(inFile, outFileCpp, platform)

#Compile the transpiled source code
compilerCommand = ""
okCompilerTxt = ""

if (platform == Converter.allowedPlatforms[0]):#linux
    compilerCommand = f"g++ { outFileCpp } -o { outFileExec }"
    
elif (platform == Converter.allowedPlatforms[1]):#windows
    None
    
elif (platform == Converter.allowedPlatforms[2]):#mac
    None


try: compRes = subprocess.check_output(compilerCommand, shell=True, text=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    print(f"Error: compiler could not compile file:\n\n\n{ e.output }")
    exit(2)

if (compRes != okCompilerTxt):
    print(f"Error: compiler could not compile file:\n\n\n{ compRes }")
    exit(3)
#
    
print("Finished!")