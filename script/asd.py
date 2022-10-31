import sys
from glob import glob



folder = sys.argv[1]
folder = folder+"/*"
All_files = glob(folder)

print(All_files)