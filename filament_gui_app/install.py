#install script for development and deployment of the Filaments GUI application
import errno, stat, shutil, subprocess, os

DEBUG = False  # Set to True for debugging, False for production

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def cleanup(target : str, msg : str):
    if os.path.exists(target):
        print(f"Removing existing {msg}: {target}")
        try:
            if os.path.isfile(target):
                os.remove(target)
            elif os.path.isdir(target):
                # Use shutil.rmtree to remove directories
                shutil.rmtree(target, ignore_errors=False, onerror=handleRemoveReadonly)
        except Exception as e:
            print(f"Error removing {msg}[{target}]: {e}")
            exit(1)

output_dir = "dist"
tmp_dir = "build"
spec_file = "Filaments.spec"

cleanup(output_dir, "output directory")
cleanup(tmp_dir, "termporary directory")
cleanup(spec_file, "spec file")

PROJECT_NAME = "Filaments"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = f"{BASE_DIR}/assets"
CSS = f"{BASE_DIR}/css"
DB = f"{BASE_DIR}/filament_data_deploy.db"
# DB = f"{BASE_DIR}/filament_data.db"
ICON = f"{ASSETS}/application_icon.ico"

install_command = f"pyinstaller .\src\main.py --clean -i \"{ICON}\" --onefile --noconsole --windowed -n {PROJECT_NAME}"
# install_command = f"pyinstaller .\src\main.py --clean -i \"{ICON}\" --onefile -n {PROJECT_NAME}" # For debugging with console output

if DEBUG:
    print(f"Assets directory: {ASSETS}")
    print(f"CSS directory: {CSS}")
    print(f"Database file: {DB}")
    print(f"Icon file: {ICON}")
    print(f"Install command: {install_command}")

print("Installing Filaments App...")

result = subprocess.run(install_command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("Installation successful!")
    if DEBUG:
        print(result.stdout)
else:
    print(f"Command failed with error code: {result.returncode}")
    print(f"Error message: {result.stderr}")
    exit(1)

if os.path.exists(DB):
    shutil.copyfile(DB, f"{BASE_DIR}/{output_dir}/filament_data.db")
else:
    print(f"Database file not found: {DB}")
    exit(1)

if os.path.exists(ASSETS):
    shutil.copytree(ASSETS, f"{BASE_DIR}/{output_dir}/assets", dirs_exist_ok=True)
else:
    print(f"Assets directory not found: {ASSETS}")
    exit(1)

if os.path.exists(CSS):
    shutil.copytree(CSS, f"{BASE_DIR}/{output_dir}/css", dirs_exist_ok=True)
else:
    print(f"CSS directory not found: {CSS}")
    exit(1)
