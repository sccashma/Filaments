import os
import sys
          
pathname = os.path.dirname(sys.argv[0])        
BASE_DIR = os.path.abspath(pathname)  # Use the directory of the script as the base directory

if not os.path.exists(BASE_DIR):
    print(f"Base directory does not exist: {BASE_DIR}")
    sys.exit(1)

print(f"Base directory set to: {BASE_DIR}")
